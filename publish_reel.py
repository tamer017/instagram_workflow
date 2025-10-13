# publish_reel.py
import time
import requests
import os
import sys
import base64
import json

try:
    from nacl import public, encoding
    HAS_PYNACL = True
except Exception:
    HAS_PYNACL = False

IG_USER_ID = os.environ.get("IG_USER_ID")
LONG_LIVED_TOKEN = os.environ.get("LONG_LIVED_TOKEN")
CAPTION = os.environ.get("CAPTION", "Automated post")
MAX_WAIT_SECONDS = int(os.environ.get("MAX_POLL_SECONDS", "1500"))
INTERVAL_SECONDS = int(os.environ.get("POLL_INTERVAL", "10"))
DEFAULT_VIDEO_URL = "https://interactive-examples.mdn.mozilla.net/media/cc0-videos/flower.mp4"

GITHUB_REPOSITORY = os.environ.get("GITHUB_REPOSITORY")
GH_PAT = os.environ.get("GH_PAT")

def refresh_long_lived_token(token):
    try:
        url = "https://graph.instagram.com/refresh_access_token"
        params = {"grant_type": "ig_refresh_token", "access_token": token}
        r = requests.get(url, params=params, timeout=20)
        r.raise_for_status()
        data = r.json()
        new_token = data.get("access_token")
        if new_token and new_token != token:
            print("Token refreshed successfully (not printing token).")
            return new_token
        print("Refresh endpoint responded but no new token returned; continuing with existing token.")
        return token
    except Exception as e:
        print("Token refresh failed or token expired:", e)
        return token

def github_encrypt_and_put_secret(repo, pat, secret_name, secret_value):
    if not HAS_PYNACL:
        print("PyNaCl not installed; cannot update GitHub secret automatically.")
        return False
    headers = {"Authorization": f"token {pat}", "Accept": "application/vnd.github+json"}
    url_key = f"https://api.github.com/repos/{repo}/actions/secrets/public-key"
    r = requests.get(url_key, headers=headers, timeout=20)
    if r.status_code != 200:
        print(f"Failed to fetch public key from GitHub: {r.status_code} {r.text}")
        return False
    j = r.json()
    key_id = j.get("key_id")
    key = j.get("key")
    if not key_id or not key:
        print("Invalid public key response from GitHub:", j)
        return False
    try:
        public_key = public.PublicKey(base64.b64decode(key), encoder=encoding.RawEncoder())
        sealed_box = public.SealedBox(public_key)
        encrypted = sealed_box.encrypt(secret_value.encode("utf-8"))
        encrypted_value = base64.b64encode(encrypted).decode("utf-8")
    except Exception as e:
        print("Encryption failed:", e)
        return False
    put_url = f"https://api.github.com/repos/{repo}/actions/secrets/{secret_name}"
    payload = {"encrypted_value": encrypted_value, "key_id": key_id}
    r2 = requests.put(put_url, headers=headers, data=json.dumps(payload), timeout=20)
    if r2.status_code in (201, 204):
        print(f"Successfully updated GitHub secret '{secret_name}'.")
        return True
    else:
        print(f"Failed to update GitHub secret: {r2.status_code} {r2.text}")
        return False

def create_video_container(ig_user_id, token, video_url, caption, thumbnail_url=None):
    url = f"https://graph.facebook.com/v17.0/{ig_user_id}/media"
    payload = {
        "media_type": "REELS",
        "video_url": video_url,
        "caption": caption,
        "access_token": token
    }
    if thumbnail_url:
        payload["thumbnail_url"] = thumbnail_url
    r = requests.post(url, params=payload, timeout=30)
    r.raise_for_status()
    data = r.json()
    print("create response:", data)
    creation_id = data.get("id")
    if not creation_id:
        raise RuntimeError(f"Failed to create media container: {data}")
    return creation_id

def publish_media(ig_user_id, token, creation_id):
    url = f"https://graph.facebook.com/v17.0/{ig_user_id}/media_publish"
    payload = {
        "creation_id": creation_id,
        "access_token": token
    }
    r = requests.post(url, params=payload, timeout=30)
    r.raise_for_status()
    data = r.json()
    print("publish response:", data)
    media_id = data.get("id")
    if not media_id:
        raise RuntimeError(f"Failed to publish media: {data}")
    return media_id

def main():
    video_url = None
    thumb_url = None
    if len(sys.argv) >= 2:
        video_url = sys.argv[1].strip()
    else:
        video_url = os.environ.get("VIDEO_URL", DEFAULT_VIDEO_URL).strip()
    if len(sys.argv) >= 3:
        thumb_url = sys.argv[2].strip()
    else:
        thumb_url = os.environ.get("THUMBNAIL_URL")

    if not IG_USER_ID or not LONG_LIVED_TOKEN:
        print("ERROR: IG_USER_ID and LONG_LIVED_TOKEN must be set as environment variables.")
        sys.exit(2)

    new_token = refresh_long_lived_token(LONG_LIVED_TOKEN)
    token_in_use = new_token or LONG_LIVED_TOKEN

    if GITHUB_REPOSITORY and GH_PAT:
        if new_token and new_token != LONG_LIVED_TOKEN:
            print("Attempting to update repository secret with the refreshed token (won't print token).")
            ok = github_encrypt_and_put_secret(GITHUB_REPOSITORY, GH_PAT, "LONG_LIVED_TOKEN", new_token)
            if ok:
                token_in_use = new_token
            else:
                print("Failed to update repository secret automatically. You may need to update LONG_LIVED_TOKEN manually.")
        else:
            print("No new token to update (refresh returned same token).")
    else:
        if new_token and new_token != LONG_LIVED_TOKEN:
            print("Token refreshed locally. You should update LONG_LIVED_TOKEN secret in Actions with the new token.")
        else:
            print("Token refresh skipped or not needed.")

    print("Using video URL:", video_url)
    if thumb_url:
        print("Using thumbnail URL:", thumb_url)
    creation_id = create_video_container(IG_USER_ID, token_in_use, video_url, CAPTION, thumbnail_url=thumb_url)

    poll_url = f"https://graph.facebook.com/v17.0/{creation_id}"
    poll_params = {"fields": "status_code", "access_token": token_in_use}

    elapsed = 0
    while True:
        r = requests.get(poll_url, params=poll_params, timeout=30)
        r.raise_for_status()
        status_resp = r.json()
        status = status_resp.get("status_code")
        print("container status:", status_resp)

        if status == "FINISHED":
            break
        if status == "ERROR":
            raise RuntimeError(f"Container processing failed: {status_resp}")

        time.sleep(INTERVAL_SECONDS)
        elapsed += INTERVAL_SECONDS
        if elapsed >= MAX_WAIT_SECONDS:
            raise RuntimeError(f"Timed out waiting for container to finish (waited {elapsed}s).")

    media_id = publish_media(IG_USER_ID, token_in_use, creation_id)
    print("Published media id:", media_id)

if __name__ == "__main__":
    main()

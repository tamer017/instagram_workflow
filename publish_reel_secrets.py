# publish_reel_secrets.py
"""Publish to Instagram using env vars (reads secrets from GitHub Actions environment).
Optional: if GH_PAT and GITHUB_REPOSITORY are provided, and a token is refreshed,
this script will update the repository secret named LONG_LIVED_TOKEN with the new token.
"""
import os, sys, time, requests, json, base64

IG_USER_ID = os.environ.get("IG_USER_ID")
LONG_LIVED_TOKEN = os.environ.get("LONG_LIVED_TOKEN")
GH_PAT = os.environ.get("GH_PAT")  # optional: used to write refreshed token back to repo secrets
GITHUB_REPOSITORY = os.environ.get("GITHUB_REPOSITORY")  # owner/repo required for updating secrets via API
CAPTION = os.environ.get("CAPTION", "Automated reel via workflow")
MAX_WAIT_SECONDS = int(os.environ.get("MAX_POLL_SECONDS", "1500"))
INTERVAL_SECONDS = int(os.environ.get("POLL_INTERVAL", "10"))

DEFAULT_VIDEO_URL = "https://interactive-examples.mdn.mozilla.net/media/cc0-videos/flower.mp4"

def http_get(url, params=None, timeout=20):
    r = requests.get(url, params=params, timeout=timeout)
    return r

def http_post(url, params=None, timeout=30):
    r = requests.post(url, params=params, timeout=timeout)
    return r

def check_token(token):
    r = http_get("https://graph.instagram.com/me", params={"fields":"id,username", "access_token":token})
    return r

def refresh_long_lived_token(token):
    r = http_get("https://graph.instagram.com/refresh_access_token", params={"grant_type":"ig_refresh_token","access_token":token})
    if r.status_code == 200:
        j = r.json()
        return j.get("access_token")
    else:
        print("Refresh failed status:", r.status_code, "body:", r.text)
        return None

def create_video_container(ig_user_id, token, video_url, caption, thumbnail_url=None):
    url = f"https://graph.facebook.com/v17.0/{ig_user_id}/media"
    params = {"media_type":"REELS","video_url":video_url,"caption":caption,"access_token":token}
    if thumbnail_url:
        params["thumbnail_url"]=thumbnail_url
    r = http_post(url, params=params, timeout=30)
    return r

def poll_until_finished(creation_id, token, max_wait=MAX_WAIT_SECONDS, interval=INTERVAL_SECONDS):
    poll_url = f"https://graph.facebook.com/v17.0/{creation_id}"
    params = {"fields":"status_code,processing_progress,errors","access_token":token}
    waited = 0
    while waited <= max_wait:
        r = http_get(poll_url, params=params, timeout=30)
        print("poll:", r.status_code, r.text)
        if r.status_code != 200:
            raise RuntimeError(f"Polling error: {r.status_code} {r.text}")
        j = r.json()
        status = j.get("status_code")
        if status == "FINISHED":
            return j
        if status == "ERROR":
            raise RuntimeError(f"Container error: {json.dumps(j, indent=2)}")
        time.sleep(interval)
        waited += interval
    raise RuntimeError("Timed out waiting for container")

def publish_media(ig_user_id, token, creation_id):
    url = f"https://graph.facebook.com/v17.0/{ig_user_id}/media_publish"
    params = {"creation_id":creation_id,"access_token":token}
    r = http_post(url, params=params, timeout=30)
    return r

# GitHub secret update helpers
def encrypt_secret(public_key_b64, secret_value):
    try:
        from nacl import public, encoding
    except Exception as e:
        raise RuntimeError("pynacl required to encrypt secrets: " + str(e))
    public_key = public.PublicKey(base64.b64decode(public_key_b64))
    sealed_box = public.SealedBox(public_key)
    encrypted = sealed_box.encrypt(secret_value.encode('utf-8'))
    return base64.b64encode(encrypted).decode('utf-8')

def update_github_secret(repo, secret_name, secret_value, gh_pat):
    # repo = "owner/repo"
    headers = {"Authorization": f"token {gh_pat}", "Accept":"application/vnd.github+json"}
    url = f"https://api.github.com/repos/{repo}/actions/secrets/public-key"
    r = requests.get(url, headers=headers, timeout=15)
    r.raise_for_status()
    j = r.json()
    key = j["key"]
    key_id = j["key_id"]
    encrypted_value = encrypt_secret(key, secret_value)
    put_url = f"https://api.github.com/repos/{repo}/actions/secrets/{secret_name}"
    payload = {"encrypted_value": encrypted_value, "key_id": key_id}
    pr = requests.put(put_url, headers=headers, json=payload, timeout=15)
    pr.raise_for_status()
    return pr.status_code in (201,204)

def main():
    video_url = sys.argv[1] if len(sys.argv) >= 2 else os.environ.get("VIDEO_URL", DEFAULT_VIDEO_URL)
    thumb_url = sys.argv[2] if len(sys.argv) >= 3 else os.environ.get("THUMBNAIL_URL")

    if not IG_USER_ID or not LONG_LIVED_TOKEN:
        print("IG_USER_ID and LONG_LIVED_TOKEN must be set as environment variables (GitHub Actions secrets).")
        sys.exit(2)

    print("Checking token /me ...")
    r = check_token(LONG_LIVED_TOKEN)
    if r.status_code != 200:
        print("Token appears invalid, attempting refresh...")
        new_token = refresh_long_lived_token(LONG_LIVED_TOKEN)
        if new_token:
            print("Received refreshed token. Will validate and optionally update repository secret (if GH_PAT provided).")
            # validate new token
            rr = check_token(new_token)
            if rr.status_code == 200:
                print("Refreshed token valid for:", rr.json())
                # update github secret if GH_PAT present
                if GH_PAT and GITHUB_REPOSITORY:
                    try:
                        ok = update_github_secret(GITHUB_REPOSITORY, "LONG_LIVED_TOKEN", new_token, GH_PAT)
                        print("Updated repository secret LONG_LIVED_TOKEN:", ok)
                    except Exception as e:
                        print("Failed to update GitHub secret:", e)
                token = new_token
            else:
                print("Refreshed token did not validate:", rr.status_code, rr.text)
                print("Aborting to avoid API errors.")
                sys.exit(3)
        else:
            print("Refresh returned no token. Aborting.")
            sys.exit(3)
    else:
        print("Token valid:", r.json())
        token = LONG_LIVED_TOKEN

    # create container
    print("Creating media container with video_url:", video_url)
    cr = create_video_container(IG_USER_ID, token, video_url, CAPTION, thumbnail_url=thumb_url)
    if cr.status_code != 200:
        print("Create container failed:", cr.status_code, cr.text)
        sys.exit(4)
    cid = cr.json().get("id")
    print("Created container id:", cid)
    poll_info = poll_until_finished(cid, token)
    print("Poll info:", json.dumps(poll_info, indent=2))
    pub = publish_media(IG_USER_ID, token, cid)
    if pub.status_code != 200:
        print("Publish failed:", pub.status_code, pub.text)
        sys.exit(5)
    print("Published media:", pub.json())

if __name__ == '__main__':
    main()

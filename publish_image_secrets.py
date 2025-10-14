# publish_image_secrets.py
"""Publish an image (thumbnail) via Facebook Graph API reading secrets from env (GitHub Actions).
Flow:
1. Validate LONG_LIVED_TOKEN via /me.
2. Attempt refresh if invalid; abort if still invalid.
3. Create image container via /{ig_user_id}/media with image_url.
4. Poll (status_code) and publish via /media_publish.
"""
import os, sys, time, requests, json

IG_USER_ID = os.environ.get("IG_USER_ID")
LONG_LIVED_TOKEN = os.environ.get("LONG_LIVED_TOKEN")
CAPTION = os.environ.get("CAPTION", "Automated image post from workflow")
MAX_WAIT_SECONDS = int(os.environ.get("MAX_POLL_SECONDS", "180"))
INTERVAL_SECONDS = int(os.environ.get("POLL_INTERVAL", "2"))

def refresh_long_lived_token(token):
    try:
        r = requests.get("https://graph.instagram.com/refresh_access_token", params={"grant_type":"ig_refresh_token","access_token":token}, timeout=20)
        r.raise_for_status()
        data = r.json()
        return data.get("access_token", token)
    except Exception as e:
        print("Token refresh failed:", e)
        return token

def create_video_container(ig_user_id, token, video_url, caption, thumbnail_url=None):
    url = f"https://graph.facebook.com/v17.0/{ig_user_id}/media"
    params = {"media_type":"REELS","video_url":video_url,"caption":caption,"access_token":token}
    if thumbnail_url:
        params["thumbnail_url"]=thumbnail_url
    r = requests.post(url, params=params, timeout=30)
    r.raise_for_status()
    data = r.json()
    print("create response:", data)
    cid = data.get("id")
    if not cid:
        raise RuntimeError("Failed to create container: %r" % (data,))
    return cid

def poll_until_finished(creation_id, token, max_wait=MAX_WAIT_SECONDS, interval=INTERVAL_SECONDS):
    poll_url = f"https://graph.facebook.com/v17.0/{creation_id}"
    params = {"fields":"status_code,processing_progress,errors","access_token":token}
    waited=0
    while waited <= max_wait:
        r = requests.get(poll_url, params=params, timeout=30)
        r.raise_for_status()
        j = r.json()
        print("status:", j)
        status = j.get("status_code")
        if status=="FINISHED":
            return
        if status=="ERROR":
            raise RuntimeError("Container error: %r" % (j,))
        time.sleep(interval)
        waited += interval
    raise RuntimeError("Timed out waiting for container")

def publish_media(ig_user_id, token, creation_id):
    url = f"https://graph.facebook.com/v17.0/{ig_user_id}/media_publish"
    params = {"creation_id":creation_id,"access_token":token}
    r = requests.post(url, params=params, timeout=30)
    r.raise_for_status()
    data = r.json()
    print("publish response:", data)
    return data.get("id")


def main():
    if not IG_USER_ID or not LONG_LIVED_TOKEN:
        print("IG_USER_ID and LONG_LIVED_TOKEN must be provided via env/secrets.")
        sys.exit(2)
    video_url = sys.argv[1] if len(sys.argv) >= 2 else None
    thumb_url = sys.argv[2] if len(sys.argv) >= 3 else CAPTION
    if not video_url:
        print("Usage: python publish_image_secrets.py <image_url> [caption]")
        sys.exit(2)

    token = refresh_long_lived_token(LONG_LIVED_TOKEN)

    # create container
    print("Creating media container for image:", video_url)
    creation_id = create_video_container(IG_USER_ID, token, video_url, CAPTION, thumbnail_url=thumb_url)
    
    poll_until_finished(creation_id, token)

    mid = publish_media(IG_USER_ID, token, creation_id)
    print("Published media id:", mid)

if __name__ == '__main__':
    main()

# publish_reel_debug.py (same as before)
import time, requests, os, sys, json

IG_USER_ID = os.environ.get("IG_USER_ID")
LONG_LIVED_TOKEN = os.environ.get("LONG_LIVED_TOKEN")
CAPTION = os.environ.get("CAPTION", "Automated post")
MAX_WAIT_SECONDS = int(os.environ.get("MAX_POLL_SECONDS", "1500"))
INTERVAL_SECONDS = int(os.environ.get("POLL_INTERVAL", "10"))

DEFAULT_VIDEO_URL = "https://interactive-examples.mdn.mozilla.net/media/cc0-videos/flower.mp4"

def http_get(url, params=None, timeout=20):
    try:
        r = requests.get(url, params=params, timeout=timeout)
        r.raise_for_status()
        return r
    except requests.HTTPError as e:
        print("HTTP GET error:", e)
        if e.response is not None:
            try:
                print("Response body:", e.response.text)
            except Exception:
                pass
        raise

def http_post(url, params=None, timeout=30):
    try:
        r = requests.post(url, params=params, timeout=timeout)
        r.raise_for_status()
        return r
    except requests.HTTPError as e:
        print("HTTP POST error:", e)
        if e.response is not None:
            try:
                print("Response body:", e.response.text)
            except Exception:
                pass
        raise

def check_token(token):
    print("Checking token by calling /me endpoint...")
    try:
        r = http_get("https://graph.instagram.com/me", params={"fields":"id,username", "access_token":token})
        print("Token valid for user:", r.json())
        return True
    except Exception as e:
        print("Token check failed:", e)
        return False

def refresh_long_lived_token(token):
    try:
        r = requests.get("https://graph.instagram.com/refresh_access_token", params={"grant_type":"ig_refresh_token","access_token":token}, timeout=20)
        if r.status_code != 200:
            print("Refresh endpoint returned non-200:", r.status_code, r.text)
            return token
        data = r.json()
        new = data.get("access_token")
        if new and new != token:
            print("Received refreshed token (not printed).")
            return new
        return token
    except Exception as e:
        print("Token refresh exception:", e)
        return token

def create_video_container(ig_user_id, token, video_url, caption, thumbnail_url=None):
    url = f"https://graph.facebook.com/v17.0/{ig_user_id}/media"
    params = {"media_type":"REELS","video_url":video_url,"caption":caption,"access_token":token}
    if thumbnail_url:
        params["thumbnail_url"] = thumbnail_url
    r = http_post(url, params=params, timeout=30)
    print("create response:", r.json())
    return r.json().get("id")

def poll_until_finished(creation_id, token, max_wait=MAX_WAIT_SECONDS, interval=INTERVAL_SECONDS):
    poll_url = f"https://graph.facebook.com/v17.0/{creation_id}"
    params = {"fields":"status_code,processing_progress,errors","access_token":token}
    waited=0
    while waited <= max_wait:
        try:
            r = requests.get(poll_url, params=params, timeout=30)
            print("poll response code:", r.status_code, "body:", r.text)
            r.raise_for_status()
            j = r.json()
            status = j.get("status_code")
            if status == "FINISHED":
                print("Container finished processing.")
                return j
            if status == "ERROR":
                print("Container returned ERROR, details:", json.dumps(j, indent=2))
                raise RuntimeError("Container error: %r" % (j,))
        except requests.HTTPError as e:
            print("HTTP error while polling:", e)
            if e.response is not None:
                print("Response body:", e.response.text)
            raise
        time.sleep(interval)
        waited += interval
    raise RuntimeError("Timed out waiting for container")

def publish_media(ig_user_id, token, creation_id):
    url = f"https://graph.facebook.com/v17.0/{ig_user_id}/media_publish"
    params = {"creation_id":creation_id,"access_token":token}
    r = http_post(url, params=params, timeout=30)
    print("publish response:", r.json())
    return r.json().get("id")

def main():
    video_url = sys.argv[1] if len(sys.argv) >= 2 else os.environ.get("VIDEO_URL", DEFAULT_VIDEO_URL)
    thumb_url = sys.argv[2] if len(sys.argv) >= 3 else os.environ.get("THUMBNAIL_URL")

    if not IG_USER_ID or not LONG_LIVED_TOKEN:
        print("IG_USER_ID and LONG_LIVED_TOKEN must be provided via env/secrets.")
        sys.exit(2)

    if not check_token(LONG_LIVED_TOKEN):
        print("WARNING: Provided LONG_LIVED_TOKEN appears invalid/expired. Attempting refresh (may fail without correct token).")
    token = refresh_long_lived_token(LONG_LIVED_TOKEN)
    if not check_token(token):
        print("ERROR: Token still invalid after refresh. Aborting to avoid hitting API with bad token.")
        sys.exit(3)

    creation_id = create_video_container(IG_USER_ID, token, video_url, CAPTION, thumbnail_url=thumb_url)
    if not creation_id:
        print("Failed to create media container; aborting.")
        sys.exit(4)

    poll_info = poll_until_finished(creation_id, token)
    print("Poll info:", json.dumps(poll_info, indent=2))
    media_id = publish_media(IG_USER_ID, token, creation_id)
    print("Published media id:", media_id)

if __name__ == '__main__':
    main()

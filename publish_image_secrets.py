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

def check_token(token):
    r = requests.get("https://graph.instagram.com/me", params={"fields":"id,username","access_token":token}, timeout=20)
    return r

def refresh_long_lived_token(token):
    r = requests.get("https://graph.instagram.com/refresh_access_token", params={"grant_type":"ig_refresh_token","access_token":token}, timeout=20)
    return r

def create_container(ig_user_id, token, image_url, caption):
    url = f"https://graph.facebook.com/v17.0/{ig_user_id}/media"
    payload = {'image_url': image_url, 'caption': caption, 'access_token': token}
    r = requests.post(url, params=payload, timeout=30)
    return r

def poll_container(creation_id, token, timeout_s=MAX_WAIT_SECONDS, interval=INTERVAL_SECONDS):
    url = f"https://graph.facebook.com/v17.0/{creation_id}"
    elapsed = 0
    while elapsed < timeout_s:
        r = requests.get(url, params={"fields":"status_code,errors,processing_progress","access_token":token}, timeout=30)
        try:
            j = r.json()
        except ValueError:
            raise RuntimeError(f"Invalid JSON while polling: {r.text}")
        print("poll:", r.status_code, j)
        status = j.get("status_code")
        if status is None:
            # image uploads often don't return status_code; treat as ready
            print("No status_code returned — proceeding to publish.")
            return j
        if str(status).upper() in ("FINISHED","SUCCEEDED","COMPLETED","SUCCESS"):
            return j
        if str(status).upper() in ("ERROR","ERR","FAILED"):
            raise RuntimeError(f"Container reported error: {j}")
        time.sleep(interval)
        elapsed += interval
    raise TimeoutError(f"Timed out waiting for container {creation_id} after {timeout_s}s")

def publish_media(ig_user_id, token, creation_id):
    url = f"https://graph.facebook.com/v17.0/{ig_user_id}/media_publish"
    r = requests.post(url, params={"creation_id": creation_id, "access_token": token}, timeout=30)
    return r

def main():
    if not IG_USER_ID or not LONG_LIVED_TOKEN:
        print("IG_USER_ID and LONG_LIVED_TOKEN must be provided via env/secrets.")
        sys.exit(2)
    image_url = sys.argv[1] if len(sys.argv) >= 2 else None
    caption = sys.argv[2] if len(sys.argv) >= 3 else CAPTION
    if not image_url:
        print("Usage: python publish_image_secrets.py <image_url> [caption]")
        sys.exit(2)

    # validate token
    print("Checking token with /me ...")
    r = check_token(LONG_LIVED_TOKEN)
    if r.status_code != 200:
        print("Token invalid/expired, attempting refresh...")
        rr = refresh_long_lived_token(LONG_LIVED_TOKEN)
        if rr.status_code != 200:
            print("Refresh failed:", rr.status_code, rr.text)
            sys.exit(3)
        new_token = rr.json().get("access_token")
        if not new_token:
            print("No access_token in refresh response:", rr.text)
            sys.exit(3)
        print("Refresh successful; using refreshed token (not stored).")
        token = new_token
        # validate new token
        r2 = check_token(token)
        if r2.status_code != 200:
            print("Refreshed token validation failed:", r2.status_code, r2.text)
            sys.exit(3)
    else:
        token = LONG_LIVED_TOKEN
        print("Token valid for:", r.json())

    # create container
    print("Creating media container for image:", image_url)
    cr = create_container(IG_USER_ID, token, image_url, caption)
    try:
        cr.raise_for_status()
    except requests.HTTPError:
        print("Create container failed:", cr.status_code, cr.text)
        sys.exit(4)
    cid = cr.json().get("id")
    print("create response:", cr.json())

    # poll
    poll_info = poll_container(cid, token)
    print("poll info:", poll_info)

    # publish
    pub = publish_media(IG_USER_ID, token, cid)
    try:
        pub.raise_for_status()
    except requests.HTTPError:
        print("Publish failed:", pub.status_code, pub.text)
        sys.exit(5)
    print("publish response:", pub.json())
    print("Final media id:", pub.json().get("id"))

if __name__ == '__main__':
    main()

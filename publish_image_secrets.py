#!/usr/bin/env python3
# publish_image_secrets.py
"""
Publish an image (thumbnail) via Facebook Graph API reading secrets from env (GitHub Actions).
Improvements:
- Validate LONG_LIVED_TOKEN with /me before doing anything.
- If refresh is attempted, only use the refreshed token if it returns and validates.
- Print full response bodies on any HTTP error for debugging.
- Treat missing status_code on image containers as ready.
"""
import os, sys, time, requests, json

IG_USER_ID = os.environ.get("IG_USER_ID")
LONG_LIVED_TOKEN = os.environ.get("LONG_LIVED_TOKEN")
CAPTION = os.environ.get("CAPTION", "Automated image post from workflow")
MAX_WAIT_SECONDS = int(os.environ.get("MAX_POLL_SECONDS", "180"))
INTERVAL_SECONDS = int(os.environ.get("POLL_INTERVAL", "2"))

def debug_print_resp(r, label="response"):
    try:
        print(f"{label} status: {r.status_code}")
        print("body:", r.text)
    except Exception:
        print(f"{label}: <no body available>")

def check_token(token):
    try:
        r = requests.get("https://graph.instagram.com/me",
                         params={"fields":"id,username", "access_token":token},
                         timeout=15)
    except Exception as e:
        print("Token /me call failed:", e)
        return None, None
    return r.status_code, r

def refresh_long_lived_token(token):
    try:
        r = requests.get("https://graph.instagram.com/refresh_access_token",
                         params={"grant_type":"ig_refresh_token","access_token":token},
                         timeout=15)
    except Exception as e:
        print("Token refresh request exception:", e)
        return None, None
    return r.status_code, r

def create_container(ig_user_id, token, image_url, caption):
    url = f"https://graph.facebook.com/v17.0/{ig_user_id}/media"
    payload = {'image_url': image_url, 'caption': caption, 'access_token': token}
    try:
        r = requests.post(url, params=payload, timeout=30)
    except Exception as e:
        print("Create container request failed:", e)
        raise
    return r

def poll_container(creation_id, token, timeout_s=MAX_WAIT_SECONDS, interval=INTERVAL_SECONDS):
    url = f"https://graph.facebook.com/v17.0/{creation_id}"
    elapsed = 0
    while elapsed < timeout_s:
        try:
            r = requests.get(url, params={"fields":"status_code,errors,processing_progress","access_token":token}, timeout=30)
        except Exception as e:
            print("Polling request failed:", e)
            raise
        # always print debug info for visibility
        print("poll raw:", r.status_code, r.text)
        if r.status_code != 200:
            # print body and raise with context
            print("Polling returned non-200:")
            debug_print_resp(r, "poll")
            raise RuntimeError(f"Polling HTTP error {r.status_code}: {r.text}")
        try:
            j = r.json()
        except ValueError:
            raise RuntimeError(f"Invalid JSON while polling: {r.text}")
        status = j.get("status_code")
        if status is None:
            # images often don't include status_code -> treat as ready
            print("No status_code returned — proceeding to publish.")
            return j
        if str(status).upper() in ("FINISHED","SUCCEEDED","COMPLETED","SUCCESS"):
            print("Container ready:", j)
            return j
        if str(status).upper() in ("ERROR","ERR","FAILED"):
            print("Container returned error detail:", json.dumps(j, indent=2))
            raise RuntimeError(f"Container reported error: {j}")
        time.sleep(interval)
        elapsed += interval
    raise TimeoutError(f"Timed out waiting for container {creation_id} after {timeout_s}s")

def publish_media(ig_user_id, token, creation_id):
    url = f"https://graph.facebook.com/v17.0/{ig_user_id}/media_publish"
    try:
        r = requests.post(url, params={"creation_id": creation_id, "access_token": token}, timeout=30)
    except Exception as e:
        print("Publish request failed:", e)
        raise
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

    # 1) validate the provided token
    print("Checking initial LONG_LIVED_TOKEN with /me ...")
    code, resp = check_token(LONG_LIVED_TOKEN)
    if code == 200:
        print("Token valid for:", resp.json())
        token = LONG_LIVED_TOKEN
    else:
        print("Initial token invalid or check failed (status:", code, ")")
        if resp is not None:
            debug_print_resp(resp, "initial /me response")
        # try refresh
        print("Attempting to refresh long-lived token...")
        rc, rr = refresh_long_lived_token(LONG_LIVED_TOKEN)
        if rc != 200:
            print("Refresh failed:", rc)
            if rr is not None:
                debug_print_resp(rr, "refresh response")
            print("Aborting because token is invalid and refresh failed.")
            sys.exit(3)
        new_token = rr.json().get("access_token")
        if not new_token:
            print("Refresh returned no access_token. Response body:")
            debug_print_resp(rr, "refresh")
            sys.exit(3)
        print("Received refreshed token — validating /me on refreshed token...")
        code2, resp2 = check_token(new_token)
        if code2 != 200:
            print("Refreshed token failed validation:", code2)
            debug_print_resp(resp2, "refreshed /me response")
            sys.exit(3)
        print("Refreshed token valid for:", resp2.json())
        token = new_token

    # 2) create container
    print("Creating media container for image:", image_url)
    cr = create_container(IG_USER_ID, token, image_url, caption)
    debug_print_resp(cr, "create response")
    if cr.status_code != 200:
        print("Create container failed, aborting.")
        sys.exit(4)
    creation_id = cr.json().get("id")
    if not creation_id:
        print("No creation id returned in create response:", cr.text)
        sys.exit(4)

    # 3) poll container
    poll_info = poll_container(creation_id, token)
    print("Poll info:", poll_info)

    # 4) publish
    pub = publish_media(IG_USER_ID, token, creation_id)
    debug_print_resp(pub, "publish response")
    if pub.status_code != 200:
        print("Publish failed:", pub.status_code, pub.text)
        sys.exit(5)
    print("Published successfully:", pub.json())
    print("Final media id:", pub.json().get("id"))

if __name__ == '__main__':
    main()

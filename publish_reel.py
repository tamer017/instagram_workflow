# publish_reel.py (concise)
import time, requests, os, sys, json

IG_USER_ID = os.environ.get("IG_USER_ID")
LONG_LIVED_TOKEN = os.environ.get("LONG_LIVED_TOKEN")
APP_ID = os.environ.get("APP_ID")
APP_SECRET = os.environ.get("APP_SECRET")
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")  # For updating secrets
GITHUB_REPOSITORY = os.environ.get("GITHUB_REPOSITORY")  # owner/repo
CAPTION = os.environ.get("CAPTION", "Automated post")
MAX_WAIT_SECONDS = int(os.environ.get("MAX_POLL_SECONDS", "1500"))
INTERVAL_SECONDS = int(os.environ.get("POLL_INTERVAL", "10"))
DEFAULT_VIDEO_URL = "https://interactive-examples.mdn.mozilla.net/media/cc0-videos/flower.mp4"

def refresh_long_lived_token(token, app_id=None, app_secret=None):
    """
    Refresh long-lived Facebook Page token to extend expiration by 60 days.
    If APP_ID and APP_SECRET are provided, attempts to refresh.
    Otherwise, uses the existing token.
    """
    if not app_id or not app_secret:
        print("ℹ Using existing token (APP_ID or APP_SECRET not provided for refresh)")
        return token
    
    try:
        print("🔄 Attempting to refresh token...")
        url = f"https://graph.facebook.com/v17.0/oauth/access_token"
        params = {
            "grant_type": "fb_exchange_token",
            "client_id": app_id,
            "client_secret": app_secret,
            "fb_exchange_token": token
        }
        
        r = requests.get(url, params=params, timeout=20)
        r.raise_for_status()
        data = r.json()
        
        new_token = data.get("access_token")
        expires_in = data.get("expires_in", 0)
        
        if new_token and new_token != token:
            print(f"✓ Token refreshed! New expiration: ~{expires_in // 86400} days")
            return new_token
        else:
            print("ℹ Token refresh returned same token, using it")
            return token
            
    except Exception as e:
        print(f"⚠ Token refresh failed: {e}")
        print(f"  Using existing token (it may still be valid)")
        return token

def update_github_secret(secret_name, secret_value, github_token, repository):
    """
    Update a GitHub repository secret.
    Requires GITHUB_TOKEN with repo scope and pynacl library.
    """
    try:
        from nacl import public, encoding
        import base64
    except ImportError:
        print("⚠ pynacl not installed, skipping GitHub secret update")
        print("  Install with: pip install pynacl")
        return False
    
    try:
        print(f"🔐 Updating GitHub secret: {secret_name}")
        
        # Get repository public key
        headers = {
            "Authorization": f"Bearer {github_token}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28"
        }
        
        key_url = f"https://api.github.com/repos/{repository}/actions/secrets/public-key"
        r = requests.get(key_url, headers=headers, timeout=15)
        r.raise_for_status()
        key_data = r.json()
        
        public_key = key_data["key"]
        key_id = key_data["key_id"]
        
        # Encrypt the secret
        public_key_bytes = base64.b64decode(public_key)
        public_key_obj = public.PublicKey(public_key_bytes)
        sealed_box = public.SealedBox(public_key_obj)
        encrypted = sealed_box.encrypt(secret_value.encode('utf-8'))
        encrypted_value = base64.b64encode(encrypted).decode('utf-8')
        
        # Update the secret
        secret_url = f"https://api.github.com/repos/{repository}/actions/secrets/{secret_name}"
        payload = {
            "encrypted_value": encrypted_value,
            "key_id": key_id
        }
        
        r = requests.put(secret_url, headers=headers, json=payload, timeout=15)
        r.raise_for_status()
        
        print(f"  ✓ GitHub secret '{secret_name}' updated successfully")
        return True
        
    except Exception as e:
        print(f"  ⚠ Failed to update GitHub secret: {e}")
        return False

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

def poll_until_finished(creation_id, token, max_wait=MAX_WAIT_SECONDS, initial_interval=INTERVAL_SECONDS):
    """Poll container status with exponential backoff until finished"""
    poll_url = f"https://graph.facebook.com/v17.0/{creation_id}"
    elapsed = 0.0
    interval = initial_interval
    max_interval = 30  # Cap exponential backoff
    
    print(f"\nPolling container status (timeout: {max_wait}s)...")
    
    while elapsed < max_wait:
        # Try with just status_code field first (some containers don't support all fields)
        params = {
            "fields": "status_code",
            "access_token": token
        }
        
        try:
            r = requests.get(poll_url, params=params, timeout=30)
            print(f"  Poll attempt: status={r.status_code}")
            r.raise_for_status()
            j = r.json()
        except requests.HTTPError as e:
            print(f"✗ HTTP error during polling: {e}")
            if e.response is not None:
                try:
                    error_data = e.response.json()
                    print(f"Error details: {json.dumps(error_data, indent=2)}")
                    
                    # Check if it's a field error - try without fields parameter
                    error = error_data.get('error', {})
                    if 'field' in error.get('message', '').lower():
                        print("  Retrying without fields parameter...")
                        params = {"access_token": token}
                        r = requests.get(poll_url, params=params, timeout=30)
                        r.raise_for_status()
                        j = r.json()
                    else:
                        raise
                except Exception as retry_error:
                    print(f"  Retry also failed: {retry_error}")
                    if hasattr(retry_error, 'response') and retry_error.response:
                        print(f"  Response: {retry_error.response.text}")
                    raise
            else:
                raise
        except ValueError:
            print(f"✗ Invalid JSON response: {r.text}")
            raise RuntimeError(f"Invalid JSON while checking container: {r.text}")
        
        status = j.get("status_code")
        progress = j.get("processing_progress", "N/A")
        print(f"poll: elapsed={elapsed:.1f}s, status={status}, progress={progress}")
        
        # Handle missing status (common for images)
        if status is None:
            print("No status_code returned — container may be ready immediately")
            return True
        
        # Check for completion
        if status.upper() in ("FINISHED", "SUCCEEDED", "COMPLETED", "SUCCESS"):
            print("✓ Container finished processing")
            return True
        
        # Check for errors
        if status.upper() in ("ERROR", "ERR", "FAILED"):
            errors = j.get("errors", [])
            raise RuntimeError(f"Container processing failed: status={status}, errors={errors}")
        
        # Still processing
        time.sleep(interval)
        elapsed += interval
        
        # Exponential backoff (capped)
        interval = min(max_interval, interval * 1.5)
    
    raise RuntimeError(f"Timed out waiting for container {creation_id} after {max_wait} seconds")

def publish_media(ig_user_id, token, creation_id):
    url = f"https://graph.facebook.com/v17.0/{ig_user_id}/media_publish"
    params = {"creation_id":creation_id,"access_token":token}
    r = requests.post(url, params=params, timeout=30)
    r.raise_for_status()
    data = r.json()
    print("publish response:", data)
    return data.get("id")

def main():
    video_url = sys.argv[1] if len(sys.argv) >= 2 else os.environ.get("VIDEO_URL", DEFAULT_VIDEO_URL)
    thumb_url = sys.argv[2] if len(sys.argv) >= 3 else os.environ.get("THUMBNAIL_URL")
    
    if not IG_USER_ID or not LONG_LIVED_TOKEN:
        print("Missing IG_USER_ID or LONG_LIVED_TOKEN")
        sys.exit(2)
    
    # Refresh token if APP_ID and APP_SECRET are available
    token = refresh_long_lived_token(LONG_LIVED_TOKEN, APP_ID, APP_SECRET)
    
    # If token was refreshed and we're in GitHub Actions, update the secret
    if token != LONG_LIVED_TOKEN and GITHUB_TOKEN and GITHUB_REPOSITORY:
        update_github_secret("LONG_LIVED_TOKEN", token, GITHUB_TOKEN, GITHUB_REPOSITORY)
    
    # Publish the reel
    creation_id = create_video_container(IG_USER_ID, token, video_url, CAPTION, thumbnail_url=thumb_url)
    poll_until_finished(creation_id, token)
    mid = publish_media(IG_USER_ID, token, creation_id)
    
    print("\n" + "=" * 70)
    print("✓ SUCCESS!")
    print("=" * 70)
    print(f"Published media id: {mid}")
    print("=" * 70)

if __name__ == '__main__':
    main()

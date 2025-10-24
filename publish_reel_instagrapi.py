#!/usr/bin/env python3
"""
Publish video to Instagram as a Reel using instagrapi.
Uses INSTAGRAM_USERNAME and INSTAGRAM_PASSWORD from:
1. Environment variables (GitHub Secrets)
2. .env file (local development)
"""

import os
import sys
import argparse
from pathlib import Path

def load_credentials():
    """
    Load Instagram credentials from environment variables or .env file.
    Supports both:
    1. Personal account: INSTAGRAM_USERNAME + INSTAGRAM_PASSWORD (instagrapi)
    2. Business account: IG_USER_ID + LONG_LIVED_TOKEN (Graph API)
    
    Priority: Environment variables > .env file
    
    Returns:
        dict: Credentials with 'method', 'username', 'password', 'user_id', 'token'
    """
    # First, try to load from .env file if it exists (local development)
    env_file = Path(".env")
    if env_file.exists():
        print("📂 Loading credentials from .env file...")
        try:
            with open(env_file, 'r') as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith('#'):
                        continue
                    if '=' in line:
                        key, value = line.split('=', 1)
                        key = key.strip()
                        value = value.strip().strip('"').strip("'")
                        # Only set if not already in environment
                        if key not in os.environ:
                            os.environ[key] = value
        except Exception as e:
            print(f"⚠️  Error reading .env file: {e}")
    
    # Get credentials from environment (GitHub Secrets or .env)
    creds = {
        'username': os.environ.get("INSTAGRAM_USERNAME"),
        'password': os.environ.get("INSTAGRAM_PASSWORD"),
        'user_id': os.environ.get("IG_USER_ID"),
        'token': os.environ.get("LONG_LIVED_TOKEN"),
        'method': None
    }
    
    # Determine which method to use
    if creds['user_id'] and creds['token']:
        creds['method'] = 'graph_api'
        print("🔑 Using Instagram Graph API (Business Account)")
    elif creds['username'] and creds['password']:
        creds['method'] = 'instagrapi'
        print("🔑 Using instagrapi (Personal Account)")
    
    return creds

def publish_reel(video_path, caption=""):
    """
    Publish a video to Instagram as a Reel.
    Supports both instagrapi and Instagram Graph API.
    
    Args:
        video_path: Path to the MP4 video file
        caption: Caption for the reel
    
    Returns:
        bool: True if successful, False otherwise
    """
    # Load credentials
    creds = load_credentials()
    
    if not creds['method']:
        print("❌ Error: Missing Instagram credentials")
        print("Required (choose one method):")
        print("  Method 1 - Personal Account (instagrapi):")
        print("    - INSTAGRAM_USERNAME")
        print("    - INSTAGRAM_PASSWORD")
        print("  Method 2 - Business Account (Graph API):")
        print("    - IG_USER_ID")
        print("    - LONG_LIVED_TOKEN")
        return False
    
    # Verify video file exists
    video_file = Path(video_path)
    if not video_file.exists():
        print(f"❌ Error: Video file not found: {video_path}")
        return False
    
    if not video_file.suffix.lower() in ['.mp4', '.mov']:
        print(f"❌ Error: Video must be MP4 or MOV format: {video_path}")
        return False
    
    print(f"📹 Video file: {video_file}")
    print(f"📏 File size: {video_file.stat().st_size / (1024*1024):.2f} MB")
    
    # Use appropriate publishing method
    if creds['method'] == 'graph_api':
        return publish_with_graph_api(video_file, caption, creds['user_id'], creds['token'])
    else:
        return publish_with_instagrapi(video_file, caption, creds['username'], creds['password'])


def publish_with_graph_api(video_file, caption, user_id, access_token):
    """
    Publish video using Instagram Graph API (Business accounts).
    """
    import requests
    import time
    
    try:
        print(f"📤 Uploading reel via Graph API...")
        print(f"👤 User ID: {user_id}")
        
        # Step 1: Initialize upload
        init_url = f"https://graph.facebook.com/v18.0/{user_id}/media"
        init_params = {
            'media_type': 'REELS',
            'video_url': f"file://{video_file.absolute()}",  # This won't work for remote API
            'caption': caption,
            'access_token': access_token
        }
        
        print("⚠️  Note: Graph API requires video to be publicly accessible via URL")
        print("⚠️  Local file upload not supported. You need to:")
        print("    1. Upload video to a public server/CDN")
        print("    2. Provide video_url instead of local file")
        print("    3. Or use instagrapi method (personal account)")
        
        return False
        
    except Exception as e:
        print(f"❌ Graph API upload failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def publish_with_instagrapi(video_file, caption, username, password):
    """
    Publish video using instagrapi (Personal accounts).
    """
    try:
        from instagrapi import Client
        from instagrapi.exceptions import LoginRequired, ChallengeRequired
    except ImportError:
        print("❌ Error: instagrapi not installed")
        print("Install with: pip install instagrapi")
        return False
    
    # Initialize Instagram client
    print(f"🔐 Logging in as: {username}")
    cl = Client()
    
    # Try to load session if available
    session_file = Path("instagram_session.json")
    logged_in = False
    
    if session_file.exists():
        try:
            print("📂 Loading saved session...")
            cl.load_settings(session_file)
            cl.login(username, password)
            
            # Verify session is valid
            cl.get_timeline_feed()
            print("✅ Session restored successfully")
            logged_in = True
        except Exception as e:
            print(f"⚠️  Saved session invalid: {e}")
            print("🔄 Will create new session...")
    
    if not logged_in:
        try:
            print("🔐 Logging in with credentials...")
            cl.login(username, password)
            
            # Save session for future use
            cl.dump_settings(session_file)
            print("✅ Login successful, session saved")
            logged_in = True
            
        except ChallengeRequired as e:
            print("❌ Instagram requires verification (Challenge)")
            print("Please:")
            print("  1. Log in to Instagram on your phone/browser")
            print("  2. Complete any verification challenges")
            print("  3. Try running this script again")
            return False
        except LoginRequired as e:
            print(f"❌ Login failed: {e}")
            return False
        except Exception as e:
            print(f"❌ Login error: {e}")
            return False
    
    # Upload reel
    try:
        print("📤 Uploading reel to Instagram...")
        print(f"📝 Caption: {caption[:50]}..." if len(caption) > 50 else f"📝 Caption: {caption}")
        
        media = cl.clip_upload(
            path=str(video_file),
            caption=caption
        )
        
        print(f"✅ Reel published successfully!")
        print(f"🔗 Media ID: {media.pk}")
        print(f"🔗 URL: https://www.instagram.com/reel/{media.code}/")
        
        return True
        
    except Exception as e:
        print(f"❌ Upload failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    parser = argparse.ArgumentParser(description="Publish video to Instagram as Reel")
    parser.add_argument(
        "--video",
        required=True,
        help="Path to video file (MP4)"
    )
    parser.add_argument(
        "--caption",
        default="",
        help="Caption for the reel"
    )
    
    args = parser.parse_args()
    
    success = publish_reel(args.video, args.caption)
    
    if success:
        print("\n✅ Publishing completed successfully")
        sys.exit(0)
    else:
        print("\n❌ Publishing failed")
        sys.exit(1)

if __name__ == "__main__":
    main()

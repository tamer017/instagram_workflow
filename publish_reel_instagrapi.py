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
    Priority: Environment variables > .env file
    
    Returns:
        tuple: (username, password) or (None, None) if not found
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
    username = os.environ.get("INSTAGRAM_USERNAME")
    password = os.environ.get("INSTAGRAM_PASSWORD")
    
    return username, password

def publish_reel(video_path, caption=""):
    """
    Publish a video to Instagram as a Reel.
    
    Args:
        video_path: Path to the MP4 video file
        caption: Caption for the reel
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        from instagrapi import Client
        from instagrapi.exceptions import LoginRequired, ChallengeRequired
    except ImportError:
        print("❌ Error: instagrapi not installed")
        print("Install with: pip install instagrapi")
        return False
    
    # Load credentials
    username, password = load_credentials()
    
    if not username or not password:
        print("❌ Error: Missing Instagram credentials")
        print("Required environment variables:")
        print("  - INSTAGRAM_USERNAME")
        print("  - INSTAGRAM_PASSWORD")
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

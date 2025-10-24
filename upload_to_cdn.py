#!/usr/bin/env python3
"""
Upload video to temporary CDN/file hosting to get public URL.
Supports multiple services:
- file.io (free, 1 download only, expires in 14 days)
- tmpfiles.org (free, temporary)
- 0x0.st (free, temporary)
"""

import sys
import argparse
import requests
from pathlib import Path


def upload_to_fileio(video_path):
    """
    Upload to file.io (free, simple, 1-download limit).
    Returns: Public URL or None
    """
    try:
        print("📤 Uploading to file.io...")
        
        with open(video_path, 'rb') as f:
            files = {'file': f}
            response = requests.post(
                'https://file.io',
                files=files,
                data={'expires': '1d'}  # Expire in 1 day
            )
        
        response.raise_for_status()
        data = response.json()
        
        if data.get('success'):
            url = data.get('link')
            print(f"✅ Uploaded to file.io: {url}")
            print("⚠️  Note: This link expires after 1 download or 1 day")
            return url
        else:
            print(f"❌ file.io upload failed: {data}")
            return None
            
    except Exception as e:
        print(f"❌ file.io upload error: {e}")
        return None


def upload_to_0x0(video_path):
    """
    Upload to 0x0.st (free, longer retention).
    Returns: Public URL or None
    """
    try:
        print("📤 Uploading to 0x0.st...")
        
        with open(video_path, 'rb') as f:
            files = {'file': f}
            response = requests.post(
                'https://0x0.st',
                files=files
            )
        
        response.raise_for_status()
        url = response.text.strip()
        
        if url.startswith('http'):
            print(f"✅ Uploaded to 0x0.st: {url}")
            return url
        else:
            print(f"❌ 0x0.st upload failed: {url}")
            return None
            
    except Exception as e:
        print(f"❌ 0x0.st upload error: {e}")
        return None


def upload_to_tmpfiles(video_path):
    """
    Upload to tmpfiles.org (free temporary hosting).
    Returns: Public URL or None
    """
    try:
        print("📤 Uploading to tmpfiles.org...")
        
        with open(video_path, 'rb') as f:
            files = {'file': f}
            response = requests.post(
                'https://tmpfiles.org/api/v1/upload',
                files=files
            )
        
        response.raise_for_status()
        data = response.json()
        
        if data.get('status') == 'success':
            # tmpfiles.org returns URL like https://tmpfiles.org/123456
            # But actual file is at https://tmpfiles.org/dl/123456
            url = data['data']['url']
            # Convert to direct download URL
            if '/dl/' not in url:
                url = url.replace('tmpfiles.org/', 'tmpfiles.org/dl/')
            
            print(f"✅ Uploaded to tmpfiles.org: {url}")
            return url
        else:
            print(f"❌ tmpfiles.org upload failed: {data}")
            return None
            
    except Exception as e:
        print(f"❌ tmpfiles.org upload error: {e}")
        return None


def upload_video(video_path, service='fileio'):
    """
    Upload video to temporary CDN service.
    
    Args:
        video_path: Path to video file
        service: Service to use ('fileio', '0x0', 'tmpfiles')
    
    Returns:
        str: Public URL or None if failed
    """
    video_file = Path(video_path)
    
    if not video_file.exists():
        print(f"❌ Error: Video file not found: {video_path}")
        return None
    
    file_size_mb = video_file.stat().st_size / (1024 * 1024)
    print(f"📹 Video: {video_file.name}")
    print(f"📏 Size: {file_size_mb:.2f} MB")
    
    if file_size_mb > 100:
        print("⚠️  Warning: File is quite large. Upload may be slow or fail.")
    
    # Try selected service
    services = {
        'fileio': upload_to_fileio,
        '0x0': upload_to_0x0,
        'tmpfiles': upload_to_tmpfiles
    }
    
    upload_func = services.get(service.lower(), upload_to_fileio)
    url = upload_func(video_path)
    
    # If primary service fails, try fallback
    if not url:
        print("⚠️  Primary service failed, trying fallback...")
        for fallback_service, fallback_func in services.items():
            if fallback_service != service.lower():
                url = fallback_func(video_path)
                if url:
                    break
    
    return url


def main():
    parser = argparse.ArgumentParser(
        description="Upload video to temporary CDN for Instagram Graph API"
    )
    parser.add_argument(
        '--video',
        required=True,
        help='Path to video file'
    )
    parser.add_argument(
        '--service',
        default='0x0',
        choices=['fileio', '0x0', 'tmpfiles'],
        help='CDN service to use (default: 0x0)'
    )
    
    args = parser.parse_args()
    
    url = upload_video(args.video, args.service)
    
    if url:
        print(f"\n✅ Success! Public URL:")
        print(url)
        
        # Output for GitHub Actions
        with open('video_url.txt', 'w') as f:
            f.write(url)
        print(f"\n📄 URL saved to: video_url.txt")
        
        sys.exit(0)
    else:
        print(f"\n❌ Failed to upload video")
        sys.exit(1)


if __name__ == '__main__':
    main()

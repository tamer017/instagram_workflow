# ngrok-only repo (no localtunnel)

This repo runs a GitHub Actions workflow that:
- Generates a short color-changing vertical video using Pillow + ffmpeg
- Serves it on the runner and exposes it via ngrok v3 (requires NGROK_AUTHTOKEN)
- Publishes the video to Instagram Reels via the Instagram Graph API
- Uploads the generated ZIP as an artifact and tears down ngrok

Important: this workflow **requires** NGROK_AUTHTOKEN to be set in the repo secrets (no fallback).

Files included:
- generate_video_ffmpeg.py
- publish_reel_debug.py
- .github/workflows/ngrok_only.yml
- token_help.md (how to get LONG_LIVED_TOKEN)
- requirements.txt

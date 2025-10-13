# Instagram auto-publish with Pillow + ffmpeg generator and ngrok

This repo generates a color-changing vertical video using Pillow-generated frames and ffmpeg (no moviepy).
It exposes the video temporarily via ngrok, publishes it to Instagram Reels, uploads a zipped artifact, then tears down the tunnel.

Files:
- generate_video_ffmpeg.py  -- generates frames, builds mp4 with ffmpeg, extracts thumbnails, zips outputs
- publish_reel.py           -- posts to Instagram (refreshes token)
- .github/workflows/ngrok_publish_with_generate.yml  -- workflow scheduled every 5 minutes (or run manually)
- README.md, .env.sample

Setup: add repo secrets IG_USER_ID, LONG_LIVED_TOKEN, NGROK_AUTHTOKEN (optional GH_PAT).

# ngrok with localtunnel fallback

This repo contains a workflow that attempts to use ngrok (with NGROK_AUTHTOKEN). If ngrok fails due to agent version or auth (ERR_NGROK_121), the workflow falls back to localtunnel (no account required).
- generate_video_ffmpeg.py: creates a temporary video and thumbnails using Pillow + ffmpeg
- publish_reel.py: posts to Instagram using the IG Graph API
- workflow: attempts ngrok then localtunnel fallback; serves files temporarily; publishes; tears down

If you prefer to keep using ngrok, update the download URL in the workflow to a current ngrok v3 binary from the official ngrok download page, or use a paid ngrok account that doesn't enforce minimum agent version.

Secrets: IG_USER_ID, LONG_LIVED_TOKEN, NGROK_AUTHTOKEN (optional)

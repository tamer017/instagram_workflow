# ngrok v3 upgrade + virtualenv + localtunnel fallback

This repository updates the workflow to:
- download a known ngrok v3 tarball (explicit link used),
- extract and run the v3 binary (avoids ERR_NGROK_121 caused by old v2 agent),
- create a Python virtualenv (.venv) and install dependencies into it (faster, isolated),
- generate a short (3s) vertical color-changing video to speed runs,
- fallback to localtunnel if ngrok fails,
- verify the public URL before publishing to Instagram.

Files:
- generate_video_ffmpeg.py
- publish_reel.py
- .github/workflows/ngrok_upgrade_with_venv.yml

Secrets required: IG_USER_ID, LONG_LIVED_TOKEN, NGROK_AUTHTOKEN (optional)

Notes:
- If your NGROK_AUTHTOKEN still fails, try visiting https://ngrok.com/download and copying the v3 download link for Linux x86_64, then update `NGROK_DOWNLOAD_URL` in the workflow.
- Running every 5 minutes may hit IG rate limits; use workflow_dispatch for safer testing.

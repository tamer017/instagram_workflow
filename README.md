# Instagram auto-publish with on-demand ngrok hosting and generated videos (fixed)

This repo fixes the previous moviepy import error by installing moviepy and imageio-ffmpeg and avoiding ImageMagick/TextClip in the generator.

## What changed
- `generate_video.py` no longer uses TextClip (no ImageMagick dependency).
- Workflow installs `moviepy`, `imageio`, `imageio-ffmpeg` via pip and `ffmpeg` via apt, and sets `IMAGEIO_FFMPEG_BINARY` when generating video.

## Files included
- `generate_video.py` — generates `video.mp4`, `thumb_1.jpg`, `thumb_2.jpg`, ... and `video_and_thumbs.zip`.
- `publish_reel.py` — publishes to IG, refreshes token and can auto-update LONG_LIVED_TOKEN secret if GH_PAT is provided.
- `.github/workflows/ngrok_publish_with_generate.yml` — scheduled every 5 minutes (cron `*/5 * * * *`) and runs the full flow.
- `.env.sample` — local testing variables.

## Setup
Add repository secrets: `IG_USER_ID`, `LONG_LIVED_TOKEN`, `NGROK_AUTHTOKEN`. Optionally add `GH_PAT`.


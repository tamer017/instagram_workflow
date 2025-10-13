# Instagram auto-publish with on-demand ngrok hosting and generated videos

This repo contains an automated GitHub Actions workflow that:
1. Generates a short vertical color-changing video and multiple thumbnails using Python (moviepy).
2. Starts a local HTTP server and an ngrok tunnel to expose the generated files via HTTPS.
3. Calls the Instagram Graph API to create a REELS media container (passes thumbnail_url if available), polls for processing, and publishes the Reel.
4. Uploads a zip artifact containing the generated video and thumbnails for download.
5. Tears down ngrok and the server so the files are no longer public until the next run.

## Files
- `generate_video.py` — generates `video.mp4`, `thumb_1.jpg`, `thumb_2.jpg`, ... and `video_and_thumbs.zip` inside the output directory.
- `publish_reel.py` — publishes to IG, refreshes token and can auto-update LONG_LIVED_TOKEN secret if GH_PAT is provided.
- `.github/workflows/ngrok_publish_with_generate.yml` — scheduled every 5 minutes (cron `*/5 * * * *`) and runs the full flow.
- `.env.sample` — local testing variables.

## Setup
1. Add repository secrets: `IG_USER_ID`, `LONG_LIVED_TOKEN`, `NGROK_AUTHTOKEN`. Optionally add `GH_PAT`.
2. Ensure Actions allowed and workflow is enabled. For testing, use `workflow_dispatch` to run manually.
3. Be careful with the 5-minute schedule — Instagram rate limits may apply. Use a test IG Business account.


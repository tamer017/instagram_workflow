# Final repo: Publish thumbnail IMAGE via Facebook Graph API (ngrok v3, secrets)

This final ZIP contains a full GitHub Actions-based workflow to:
- generate a short vertical color-changing video and thumbnails,
- serve them via a local HTTP server on the runner,
- expose the runner via ngrok v3 (requires NGROK_AUTHTOKEN secret),
- publish the thumbnail (thumb_1.jpg) as an IMAGE post to Instagram using the Facebook Graph API endpoints:
  - POST /{ig_user_id}/media with image_url
  - poll the container and POST /{ig_user_id}/media_publish
- reads `IG_USER_ID` and `LONG_LIVED_TOKEN` from GitHub Actions secrets (workflow injects them into env)

Usage:
1. Extract and push this repo to your GitHub repository root.
2. Add repository secrets: `IG_USER_ID`, `LONG_LIVED_TOKEN`, `NGROK_AUTHTOKEN`.
3. Run the workflow "Publish thumbnail IMAGE via Facebook Graph (ngrok v3, secrets)" manually (Actions -> Run workflow).
4. Inspect logs for create/poll/publish responses. The publish step prints the responses.

Notes:
- Make sure LONG_LIVED_TOKEN is a valid Instagram long-lived token (test with /me).
- IG_USER_ID must be the Instagram Business Account numeric ID.

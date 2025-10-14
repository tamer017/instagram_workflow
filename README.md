# Final fix: debug publish + pip cache + ngrok v3 + venv

This repo improves reliability and speed:
- uses Python venv (.venv) to isolate installs and speed up repeated runs
- caches pip (~/.cache/pip) across runs with actions/cache to avoid reinstalling packages each time
- downloads an explicit ngrok v3 tarball and runs it (avoids ERR_NGROK_121)
- falls back to localtunnel if ngrok fails
- publish_reel_debug.py checks token validity, prints full API responses on error, and aborts safely if token invalid
- generates a very short 2s video to speed up runs (adjustable)

**Before running**: add GitHub secrets `IG_USER_ID` and `LONG_LIVED_TOKEN`. Optionally add `NGROK_AUTHTOKEN` to use ngrok.

**Testing**: use workflow_dispatch to run manually; inspect logs. If publish fails due to token, the workflow will print detailed responses so you can see why (common cause: expired/invalid token).

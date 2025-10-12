# Instagram Hourly Reel Publisher (GitHub Actions) - Updated

This repository contains a minimal setup to publish the *same* public video to Instagram Reels every hour using GitHub Actions.
The script now automatically refreshes the Instagram long-lived token and (optionally) updates the repository secret `LONG_LIVED_TOKEN`
using a GitHub Personal Access Token (PAT).

## Files included
- `publish_reel.py` — Python script that refreshes the token, creates a REELS media container, polls for completion, publishes, and
  optionally updates the GitHub Actions secret with the refreshed token.
- `.github/workflows/hourly_publish.yml` — A workflow that runs hourly (cron) and calls the script using a public VIDEO_URL (defaults to an MDN sample video).
- `.env.sample` — example environment file for local testing.

## Required repository secrets (add these in Settings → Secrets and variables → Actions)
- `IG_USER_ID` — your Instagram Business User ID
- `LONG_LIVED_TOKEN` — your current long-lived Instagram access token (approx. 60-day validity)
- `GH_PAT` — (optional) a GitHub Personal Access Token used by the script to automatically update the LONG_LIVED_TOKEN secret. If you want auto-update, add this secret.

## How to use
1. Create a **new public** GitHub repository (or use an existing one).
2. Upload these files (or extract the ZIP) to the repo root.
3. In the repository Settings → Secrets and variables → Actions, add `IG_USER_ID` and `LONG_LIVED_TOKEN` (and optionally `GH_PAT`).
4. Ensure Actions are enabled. The workflow runs hourly. You can also run it manually via "Run workflow".

## Create a GitHub PAT (if you want auto-update)
1. Go to GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic) → Generate new token.
2. Give it a name and expiration (choose reasonable expiry).
3. For scopes: grant `repo` (or `public_repo` for public-only access if you prefer). `repo` is more exhaustive and works for both public and private repos.
4. Generate token and copy it. Add it to your repository secrets as `GH_PAT`.

## Local testing
1. Install dependencies:
   ```
   python -m pip install requests pynacl
   ```
2. Create a local `.env` or export env vars:
   ```
   export IG_USER_ID=1234567890
   export LONG_LIVED_TOKEN="EAAB..."
   export VIDEO_URL="https://interactive-examples.mdn.mozilla.net/media/cc0-videos/flower.mp4"
   export GH_PAT="ghp_..."  # optional, for testing secret update
   export GITHUB_REPOSITORY="your-username/your-repo"  # needed if testing secret update locally
   ```
3. Run:
   ```
   python publish_reel.py
   ```

## Notes & security
- Do NOT commit real tokens to the repository. Use GitHub Secrets.
- The script avoids printing token values to logs.
- If the token refresh fails (expired or revoked), the workflow will show auth errors — update LONG_LIVED_TOKEN manually in that case.
- Auto-updating secrets requires a PAT — treat the PAT like a password and rotate it if compromised.

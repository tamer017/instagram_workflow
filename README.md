# ngrok-only repo (reads LONG_LIVED_TOKEN from GitHub Secrets, optional auto-update)

This version reads `LONG_LIVED_TOKEN` and `IG_USER_ID` directly from GitHub Actions secrets (in the workflow), and the publish script can optionally write a refreshed token back to the repository secrets if you provide `GH_PAT` as a secret (a personal access token with `repo` scope).

How it works:
- Workflow injects secrets into the job environment and calls publish_reel_secrets.py.
- publish_reel_secrets.py validates the token via /me, attempts a refresh if needed, and if refresh succeeds and `GH_PAT` + `GITHUB_REPOSITORY` are present, it encrypts and updates the repository secret `LONG_LIVED_TOKEN` using the GitHub Secrets API.

Security note: Only provide `GH_PAT` if you understand the security implications — treat it as a high-privilege secret.

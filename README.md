# ngrok with localtunnel fallback (fixed URL handling)

This version fixes a bug where the public URL file contained a prefix like 'LT_URL=...' which caused malformed VIDEO_URL values being sent to Instagram.
Fixes included:
- write only the raw public URL into /tmp/public_url.txt (no prefixes)
- on publish step, strip whitespace and perform a quick HEAD request to verify the video is reachable before calling the Instagram API
- if the URL check fails, the workflow prints http/ngrok/localtunnel logs to help debug

As before, secrets required: IG_USER_ID, LONG_LIVED_TOKEN, NGROK_AUTHTOKEN (optional)

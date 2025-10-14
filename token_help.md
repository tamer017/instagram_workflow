# token_help.md

Steps to obtain a valid LONG_LIVED_TOKEN for Instagram Graph API (Business Account)

1. Make sure you have:
   - A Facebook App (App ID and App Secret).
   - An Instagram Business Account linked to a Facebook Page.
   - The Facebook App is in development mode or live and has the required permissions for testing:
     - instagram_basic, instagram_content_publish, pages_read_engagement, pages_manage_posts, pages_show_list, etc.

2. Get a short-lived user access token:
   - Use the Facebook Login flow for your app (OAuth) or use the Graph API Explorer:
     - Graph API Explorer -> Get User Access Token -> select permissions (instagram_basic, instagram_content_publish, pages_show_list)
     - Copy the short-lived token (valid ~1-2 hours).

3. Exchange the short-lived token for a long-lived Instagram token:
   - Call (replace placeholders):
     ```
     GET https://graph.instagram.com/access_token
       ?grant_type=ig_exchange_token
       &client_secret={app-secret}
       &access_token={short-lived-token}
     ```
     - Response contains `access_token` (long-lived) and `expires_in` (seconds, ~60 days).

4. Test the long-lived token:
   - Call:
     ```
     GET https://graph.instagram.com/me?fields=id,username&access_token={LONG_LIVED_TOKEN}
     ```
     - You should get `id` and `username` for your Instagram Business account.

5. (Optional) Refresh the long-lived token regularly:
   - Call:
     ```
     GET https://graph.instagram.com/refresh_access_token
       ?grant_type=ig_refresh_token
       &access_token={LONG_LIVED_TOKEN}
     ```
     - This returns a renewed token valid for ~60 days.

6. Put the final LONG_LIVED_TOKEN into your GitHub repository Secrets (`Settings -> Secrets & variables -> Actions -> New repository secret`).

Common issues:
- "Invalid OAuth access token - Cannot parse access token": you likely pasted a malformed token or the wrong token type (e.g., a Facebook App token instead of an Instagram user token). Ensure you follow the steps to get the Instagram long-lived token.
- Ensure IG_USER_ID is the Instagram Business Account numeric ID (not a Facebook Page ID). You can get this via the `/me` token check above when token is valid.

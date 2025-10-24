# 🎬 Complete Setup Guide - Business Account (Graph API)

## ✅ Your Workflow is Ready!

The workflow now uses **GitHub Pages** to host videos publicly, then publishes them to Instagram using your **Business Account** credentials.

---

## 📋 Required Setup Steps

### Step 1: Add Instagram Secrets

Go to: https://github.com/tamer017/instagram_workflow/settings/secrets/actions

Click **"New repository secret"** and add these **4 secrets**:

1. **IG_USER_ID**
   - Your Instagram Business Account User ID
   - Value: `your_instagram_user_id`

2. **LONG_LIVED_TOKEN**
   - Your Facebook Page Access Token (60-day token)
   - Value: `your_long_lived_token`

3. **APP_ID** (Optional but recommended)
   - Your Facebook App ID (for token refresh)
   - Value: `your_app_id`

4. **APP_SECRET** (Optional but recommended)
   - Your Facebook App Secret (for token refresh)
   - Value: `your_app_secret`

---

### Step 2: Enable GitHub Pages

1. Go to: https://github.com/tamer017/instagram_workflow/settings/pages
2. Under **"Source"**, select:
   - Branch: `gh-pages`
   - Folder: `/ (root)`
3. Click **Save**
4. Wait 1-2 minutes for deployment
5. Your site URL will be: `https://tamer017.github.io/instagram_workflow/`

**Important:** The workflow deploys videos to GitHub Pages automatically. You just need to enable it once!

---

### Step 3: Enable Workflow Permissions

1. Go to: https://github.com/tamer017/instagram_workflow/settings/actions
2. Scroll to **"Workflow permissions"**
3. Select **"Read and write permissions"**
4. ✅ Check **"Allow GitHub Actions to create and approve pull requests"**
5. Click **Save**

This allows the workflow to:
- Deploy to GitHub Pages
- Commit tracking file updates
- Update refreshed tokens automatically

---

## 🚀 How It Works

### Workflow Process:

1. **Generate Video** 📹
   - Selects next unpublished Quran group
   - Downloads audio from Quran API
   - Merges audio files
   - Downloads random background video
   - Generates final video with text overlays

2. **Deploy to GitHub Pages** 🌐
   - Uploads video to `gh-pages` branch
   - Video becomes publicly accessible at:
     `https://tamer017.github.io/instagram_workflow/quran-video.mp4`

3. **Verify URL** ✅
   - Waits 30 seconds for deployment
   - Checks if video URL is accessible
   - Retries up to 10 times with 5-second intervals

4. **Publish to Instagram** 📱
   - Uses Instagram Graph API
   - Creates media container with video URL
   - Polls until processing complete
   - Publishes as Instagram Reel

5. **Track Progress** 📊
   - Marks group as published
   - Updates `published_groups.json`
   - Commits tracking file back to repo

---

## 🧪 Test the Workflow

### Manual Test (Recommended First Time):

1. Go to: https://github.com/tamer017/instagram_workflow/actions
2. Click **"Generate and Publish Quran Video"**
3. Click **"Run workflow"** (green button on right)
4. Select branch: **main**
5. Click **"Run workflow"**
6. Watch it run (takes ~5-8 minutes)

### Expected Timeline:

- **0:00** - Start
- **0:30** - Python setup complete
- **1:00** - FFmpeg and fonts installed
- **2:00** - Video generation starts
- **4:00** - Video generated, deploying to GitHub Pages
- **4:30** - Verifying URL accessibility
- **5:00** - Publishing to Instagram via Graph API
- **6:00** - Polling Instagram processing status
- **7:00** - ✅ Complete! Reel published

---

## 📊 Monitor Progress

### Check Workflow Logs:
https://github.com/tamer017/instagram_workflow/actions

### Check Published Groups:
https://github.com/tamer017/instagram_workflow/blob/main/published_groups.json

### Check GitHub Pages:
https://tamer017.github.io/instagram_workflow/quran-video.mp4

### Check Instagram:
Your Instagram profile → Reels tab

---

## ⏰ Automated Schedule

Currently runs **every 15 minutes**:
- Schedule: `*/15 * * * *`
- Runs per day: **96**
- Estimated time per run: **~7 minutes**
- Total daily usage: **~672 minutes/day**

### ⚠️ GitHub Actions Limits

**Free Tier:**
- 2,000 minutes/month
- Your current usage: ~672 min/day × 30 days = **~20,160 min/month** ❌

**Recommendation:** Change schedule to avoid exceeding limits!

### Suggested Schedules:

**Every 30 minutes** (48 runs/day):
```yaml
- cron: '*/30 * * * *'  # ~336 min/day = ~10,080/month ❌ Still over
```

**Every hour** (24 runs/day):
```yaml
- cron: '0 * * * *'  # ~168 min/day = ~5,040/month ⚠️ Better
```

**Every 2 hours** (12 runs/day):
```yaml
- cron: '0 */2 * * *'  # ~84 min/day = ~2,520/month ✅ Safe
```

**Every 3 hours** (8 runs/day):
```yaml
- cron: '0 */3 * * *'  # ~56 min/day = ~1,680/month ✅ Recommended
```

To change schedule:
1. Edit `.github/workflows/generate-video.yml`
2. Update the `cron:` line
3. Commit and push

---

## 🔧 Troubleshooting

### Issue: "GitHub Pages not enabled"

**Solution:**
1. Go to Settings → Pages
2. Select `gh-pages` branch
3. Save and wait 1-2 minutes

### Issue: "Video URL not accessible"

**Possible causes:**
- GitHub Pages not enabled ☝️
- Still deploying (wait longer)
- Workflow permission issues

**Check:**
```bash
curl -I https://tamer017.github.io/instagram_workflow/quran-video.mp4
```
Should return `HTTP/2 200` with `content-type: video/mp4`

### Issue: "Missing IG_USER_ID or LONG_LIVED_TOKEN"

**Solution:**
- Add all 4 secrets in Settings → Secrets → Actions
- Ensure secret names match exactly (case-sensitive)

### Issue: "Instagram API error"

**Common errors:**
- Invalid token → Regenerate long-lived token
- Token expired → Add APP_ID + APP_SECRET for auto-refresh
- Video too long → Instagram Reels: max 90 seconds
- Invalid video format → Must be MP4, H.264

### Issue: "Token expired"

**Solution:**
If you added `APP_ID` and `APP_SECRET`:
- Workflow automatically refreshes token
- Updated token saved back to GitHub Secrets

If no APP_ID/SECRET:
- Manually regenerate token every 60 days
- Update `LONG_LIVED_TOKEN` secret

---

## 📝 What Gets Published

Each run publishes **one Quran group**:
- **Sequential order**: Reciter 1 → 12, Surah 1 → 114
- **~7 verses per group** (optimal audio length)
- **Caption**: "Quran Recitation - reciter{X}_s{YYY}_{start}-{end}"
- **Format**: 1080x1920 MP4 (Instagram Reels)
- **Audio**: High-quality Quran recitation
- **Video**: Random Islamic background + text overlays
- **Text**: Surah name, Ayah numbers, Reciter name (Arabic + English)

---

## 🎯 Sequential Publishing

The workflow uses `group_tracker.py` to ensure:

✅ **No duplicates** - Each group published only once  
✅ **Sequential order** - Maintains logical progression  
✅ **Progress tracking** - Updates `published_groups.json`  
✅ **Auto-restart** - Loops back to beginning when all published  
✅ **Statistics** - Success/failure counts, timestamps  

### Check Progress:

```json
{
  "last_published": "reciter1_s001_001-007",
  "published_groups": ["reciter1_s001_001-007"],
  "statistics": {
    "total_published": 1,
    "success_count": 1,
    "failure_count": 0,
    "last_run": "2025-10-24T14:30:00Z"
  }
}
```

---

## 🔐 Security Notes

### Secrets Safety:
- ✅ Never commit secrets to git
- ✅ Secrets encrypted by GitHub
- ✅ Only accessible during workflow runs
- ✅ Not visible in logs or artifacts

### GitHub Pages:
- ⚠️ Videos are **publicly accessible**
- ⚠️ Anyone with URL can view
- ✅ Old videos overwritten each run
- ✅ Only latest video available

### Token Refresh:
- ✅ Automatic if APP_ID/SECRET provided
- ✅ Updated token saved to secrets
- ✅ No manual intervention needed

---

## ✅ Final Checklist

Before leaving as automated:

- [ ] All 4 secrets added (IG_USER_ID, LONG_LIVED_TOKEN, APP_ID, APP_SECRET)
- [ ] GitHub Pages enabled (gh-pages branch)
- [ ] Workflow permissions: Read and write
- [ ] Manual test run completed successfully
- [ ] Video appeared on Instagram
- [ ] `published_groups.json` updated
- [ ] Schedule adjusted (if needed to stay within limits)
- [ ] Monitoring plan in place

---

## 🎉 You're All Set!

Your automated Quran video publishing system is ready to go!

**Next steps:**
1. ✅ Add the 4 secrets
2. ✅ Enable GitHub Pages  
3. ✅ Run manual test
4. ✅ Check Instagram for published Reel
5. ✅ Adjust schedule if needed
6. 🎬 Enjoy automated publishing!

---

## 📞 Quick Links

- **Add Secrets**: https://github.com/tamer017/instagram_workflow/settings/secrets/actions
- **Enable Pages**: https://github.com/tamer017/instagram_workflow/settings/pages
- **Workflow Runs**: https://github.com/tamer017/instagram_workflow/actions
- **Published Groups**: https://github.com/tamer017/instagram_workflow/blob/main/published_groups.json

**Happy Publishing! 🎥📿**

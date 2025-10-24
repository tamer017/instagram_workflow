# GitHub Actions Workflow Setup

This guide explains how to set up the automated video generation and publishing workflow on GitHub Actions.

## Overview

The workflow automatically:
1. ✅ Runs every 15 minutes (or manually)
2. ✅ Installs FFmpeg and required fonts
3. ✅ Selects a random Quran group
4. ✅ Generates a video with Arabic text
5. ✅ Publishes to Instagram as a Reel
6. ✅ Uploads video as an artifact (backup)

## Setup Instructions

### 1. Push Code to GitHub

```bash
git add .
git commit -m "Add automated video generation workflow"
git push origin main
```

### 2. Add Instagram Credentials as Secrets

1. Go to your GitHub repository
2. Click **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret**
4. Add the following secrets:

| Secret Name | Description | Example |
|------------|-------------|---------|
| `INSTAGRAM_USERNAME` | Your Instagram username | `your_username` |
| `INSTAGRAM_PASSWORD` | Your Instagram password | `your_password` |

⚠️ **Security Note**: Never commit credentials directly to your repository!

### 3. Enable GitHub Actions

1. Go to the **Actions** tab in your repository
2. If workflows are disabled, click **Enable workflows**
3. You should see "Generate and Publish Quran Video" workflow

### 4. Run the Workflow

**Option A: Wait for Schedule** (Automatic)
- Workflow runs every 15 minutes automatically

**Option B: Manual Trigger**
1. Go to **Actions** tab
2. Click **Generate and Publish Quran Video**
3. Click **Run workflow**
4. Select branch (usually `main`)
5. Click **Run workflow**

## Workflow Features

### Automatic Installation
The workflow automatically installs:
- ✅ Python 3.10
- ✅ FFmpeg (latest from Ubuntu repos)
- ✅ Arabic fonts (DejaVu Sans, Noto Sans, Liberation)
- ✅ Python dependencies from `requirements.txt`

### Cross-Platform Font Support
The code now automatically detects and uses the correct font path:
- **Windows**: `C:/Windows/Fonts/arial.ttf`
- **Linux**: `/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf`
- **macOS**: `/Library/Fonts/Arial.ttf`

### Random Group Selection
Each run selects a random Quran reciter and verse range from your `quran_groups/` folder.

### Video Artifacts
Generated videos are uploaded as GitHub artifacts:
- **Retention**: 7 days
- **Download**: From the workflow run summary
- **Naming**: `quran-video-{GROUP_ID}`

## Workflow Schedule

```yaml
schedule:
  - cron: '*/15 * * * *'  # Every 15 minutes
```

### Cron Schedule Examples

| Schedule | Cron Expression | Description |
|----------|----------------|-------------|
| Every 15 minutes | `*/15 * * * *` | Current setting |
| Every 30 minutes | `*/30 * * * *` | Twice per hour |
| Every hour | `0 * * * *` | At minute 0 |
| Every 6 hours | `0 */6 * * *` | 4 times per day |
| Daily at 12pm | `0 12 * * *` | Once per day |

To change the schedule, edit `.github/workflows/generate-video.yml` line 5.

## Monitoring

### View Workflow Runs
1. Go to **Actions** tab
2. Click on a workflow run to see:
   - ✅ Execution logs
   - ✅ Selected group ID
   - ✅ Video size
   - ✅ Success/failure status

### Workflow Summary
Each run creates a summary showing:
- **Group ID**: Which Quran verses were used
- **Status**: Success ✅ or Failed ❌
- **Video Size**: File size of generated video
- **Video File**: Path to generated file

## Troubleshooting

### Issue: Workflow doesn't run on schedule

**Solution**: 
- GitHub Actions in free repos may have delays
- Scheduled workflows may be disabled if repo is inactive
- Check the **Actions** tab for any disabled workflows

### Issue: Instagram publishing fails

**Possible causes**:
1. Incorrect credentials in secrets
2. Instagram rate limiting
3. Two-factor authentication enabled

**Solutions**:
- Verify secrets are correct
- Check workflow logs for specific errors
- Consider disabling 2FA or using app-specific password

### Issue: Font not found on Linux

**Solution**:
- The workflow installs multiple font packages
- Code falls back to available fonts automatically
- Check workflow logs for "Using font:" message

### Issue: FFmpeg errors

**Solution**:
- View the FFmpeg error in workflow logs
- Check that all input files are valid
- Verify approved_videos.json has valid URLs

## Cost Considerations

### GitHub Actions Limits

| Plan | Minutes/month | Storage |
|------|--------------|---------|
| Free | 2,000 | 500 MB |
| Pro | 3,000 | 1 GB |
| Team | 10,000 | 2 GB |

### Usage Estimation

Running every 15 minutes:
- **Runs per day**: 96
- **Runs per month**: ~2,880
- **Minutes per run**: ~2-5 minutes
- **Monthly usage**: ~5,760-14,400 minutes

⚠️ **This will exceed free tier limits!**

### Recommendations

For free tier:
1. Run less frequently (every hour: `0 * * * *`)
2. Run only during specific hours
3. Use manual triggers only
4. Consider GitHub Pro ($4/month)

## Customization

### Change Video Settings

Edit `generate_simple_video.py`:

```python
# Video dimensions
VIDEO_WIDTH = 1080
VIDEO_HEIGHT = 1920

# Text overlays (top of file)
ARABIC_TEXT = [
    ("Your custom Arabic text", 5),
    ("More text", 8)
]

ENGLISH_TEXT = [
    ("Your custom English text", 5),
    ("More text", 8)
]
```

### Disable Text Overlays

The workflow currently uses `--no-arabic-text --no-english-text` flags.

To enable them:
1. Edit `.github/workflows/generate-video.yml`
2. Remove the flags from the generate step

### Change Video Selection

To use specific groups instead of random:

Edit workflow file, replace:
```yaml
- name: Select random group to generate
```

With your specific group ID:
```yaml
- name: Set specific group
  id: select_group
  run: echo "GROUP_ID=reciter1_s001_001-007" >> $GITHUB_OUTPUT
```

## Files Structure

```
.github/
  workflows/
    generate-video.yml      # Main workflow file
generate_simple_video.py    # Video generation script
publish_reel.py             # Instagram publishing script
requirements.txt            # Python dependencies
quran_groups/              # Group data files
approved_videos.json       # Background videos
surah_names.json           # Surah metadata
reciter_names.json         # Reciter metadata
```

## Next Steps

1. ✅ Push code to GitHub
2. ✅ Add Instagram secrets
3. ✅ Enable GitHub Actions
4. ✅ Run workflow manually to test
5. ✅ Monitor first few runs
6. ✅ Adjust schedule if needed
7. ✅ Enjoy automated Quran videos! 🎉

## Support

If you encounter issues:
1. Check workflow logs in Actions tab
2. Review this documentation
3. Verify all secrets are set correctly
4. Test the script locally first

# 🎬 Quran Video Generator for Instagram Reels# 🎬 Quran Video Generator for Instagram Reels# Instagram Auto-Publisher# Instagram Auto-Publisher# Instagram Publisher# Instagram Publisher# Instagram Publisher# Instagram Publisher# Auto-publish random-color reels every 5 minutes (Graph API + ngrok)



Automated system to create beautiful Quran recitation videos with nature backgrounds for Instagram Reels.



---Automated system to create beautiful Quran recitation videos with nature backgrounds for Instagram Reels.



## ✨ Features



- 🎥 **Video Backgrounds**: Nature scenes (water, clouds, fire, flowers, etc.) from Pixabay API---Automated Instagram publishing with random color images and reels using GitHub Actions and GitHub Pages.

- 📱 **Instagram Reels Optimized**: 1080x1920 (9:16 portrait format)

- 🎙️ **Audio Sync**: Word-level highlighting synchronized with reciter

- 📝 **Arabic & English**: Beautiful typography with RTL support

- ✅ **Auto-Verification**: Automated people-free video filtering## ✨ Features

- ⏱️ **40+ Second Videos**: Longer backgrounds, fewer loops

- 🔄 **Batch Generation**: Create multiple videos at once



---- 🎥 **Video Backgrounds**: Nature scenes (water, clouds, fire, flowers, etc.) from Pixabay API## FeaturesAutomated Instagram publishing with random color images and reels using GitHub Actions and GitHub Pages.



## 🚀 Quick Start- 📱 **Instagram Reels Optimized**: 1080x1920 (9:16 portrait format)



### 1. Install Dependencies- 🎙️ **Audio Sync**: Word-level highlighting synchronized with reciter



```powershell- 📝 **Arabic & English**: Beautiful typography with RTL support

pip install -r requirements.txt

```- ✅ **Auto-Verification**: Automated people-free video filtering- 🎨 **Random Color Content**: Generates vibrant images and videos



### 2. Get API Keys (FREE)- 🔄 **Batch Generation**: Create multiple videos at once



#### Quran Foundation API- 📤 **Auto-Publishing**: Alternates between images and reels every 5 minutes

1. Visit: https://quran.foundation/api/docs

2. Sign up and get your `CLIENT_SECRET`---



#### Pixabay API- 🌐 **GitHub Pages**: Free, permanent URLs (Instagram-friendly)## FeaturesAutomated Instagram publishing with random color images and reels via Graph API.

1. Visit: https://pixabay.com/api/docs/

2. Sign up (free account)## 🚀 Quick Start

3. Get your API key from the docs page

- 🔄 **Token Auto-Refresh**: Automatically extends token expiration (60 days)

### 3. Create `.env` File

### 1. Install Dependencies

Create a file named `.env` in the root directory:

- ⚡ **GitHub Actions**: Fully automated scheduled workflows

```

QURAN_CLIENT_SECRET=your_quran_secret_here```powershell

PIXABAY_API_KEY=your_pixabay_key_here

```pip install -r requirements.txt- ✅ **Zero Server Costs**: Everything runs on GitHub's free tier



### 4. Populate Video Pool (Auto-Verified)```



```powershell- 🎨 Generate random color images (1080x1920, 9:16)

python populate_video_pool.py

```### 2. Get API Keys (FREE)



This will:## How It Works

- Search Pixabay for 200+ nature videos (40+ seconds each)

- **Automatically filter out people** using:#### Quran Foundation API

  - People-free search terms (macro/closeup/abstract)

  - Tag scanning for people keywords1. Visit: https://quran.foundation/api/docs- 🎥 Generate random color videos (1080x1920, 9:16)

  - **Duration filter: 40+ seconds minimum**

  - View count validation (100+ views)2. Sign up and get your `CLIENT_SECRET`

  - Quality checks (like ratio, editor's choice)

- Add verified videos to `approved_videos.json`1. **Every 5 minutes**, a GitHub Action workflow runs

- **No manual verification needed!**

#### Pixabay API

### 5. Generate Your First Video

1. Visit: https://pixabay.com/api/docs/2. **Alternates content**: Even minutes = Image, Odd minutes = Reel- 📤 Auto-publish to Instagram every 5 minutes## FeaturesSimple scripts to publish images and reels to Instagram via Graph API.

```powershell

python generate_quran_video_with_background.py --group "reciter2_s002_001-005" --output "outputs/my_first_video.mp4"2. Sign up (free account)

```

3. Get your API key from the docs page3. **Generates** random color content (1080x1920, 9:16 aspect ratio)

---



## 📋 Main Scripts

### 3. Create `.env` File4. **Deploys** to GitHub Pages for permanent hosting- 🌐 GitHub Pages hosting (Instagram-friendly!)

| Script | Purpose |

|--------|---------|

| `populate_video_pool.py` | Fetch and auto-verify nature videos from Pixabay |

| `generate_quran_video_with_background.py` | Create Quran video with background |Create a file named `.env` in the root directory:5. **Publishes** to Instagram via Graph API

| `test_batch_generation.py` | Generate multiple test videos |

| `fetch_quran_reciters.py` | Get list of available reciters |

| `publish_reel.py` | Publish video to Instagram |

```6. **Auto-refreshes** your access token to prevent expiration- 🔄 Auto token refresh (60-day extension)

---

QURAN_CLIENT_SECRET=your_quran_secret_here

## 🎨 Video Features

PIXABAY_API_KEY=your_pixabay_key_here

### Visual Design

- **Font Sizes**: Arabic 90pt, Header 48pt, English 56pt```

- **Colors**: Gold verse markers (255,200,100), White text

- **Layout**: 150px padding from edges, proper RTL support## Quick Setup- ✅ No ngrok required!

- **Verse Markers**: Positioned on left side (Arabic RTL start)

### 4. Populate Video Pool (Auto-Verified)

### Background Videos

- **Portrait Format**: Height > Width for Instagram Reels

- **Duration**: 40+ seconds minimum (fewer loops)

- **People-Free**: Automated filtering of videos with people```powershell

- **Categories**: Water, Sky, Fire, Sand, Leaves, Rocks, Snow, Flowers, Abstract, Grass

- **Quality**: Popular videos with high view counts, editor's choicepython populate_video_pool.py### 1. Fork This Repository- 🎨 Generate random color images (1080x1920, 9:16)



### Audio & Timing```

- **Word-Level Sync**: Each word highlights as reciter speaks

- **Segment Extraction**: Precise audio cutting for verse ranges

- **Multiple Reciters**: Support for different recitation styles

This will:

---

- Search Pixabay for 200+ nature videosClick the "Fork" button at the top of this page.## Quick Start

## 🔧 Advanced Usage

- **Automatically filter out people** using:

### Batch Generation (20 Videos)

  - People-free search terms (macro/closeup/abstract)

```powershell

python test_batch_generation.py --count 20 --short-only  - Tag scanning for people keywords

```

  - View count validation### 2. Generate Instagram Access Token- 🎥 Generate random color videos (1080x1920, 9:16)

### Custom Background Category

  - Quality checks

```powershell

python generate_quran_video_with_background.py --group "reciter2_s002_001-005" --background "water" --output "outputs/water_theme.mp4"- Add verified videos to `approved_videos.json`

```

- **No manual verification needed!**

Available categories: `water`, `sky`, `fire`, `sand`, `leaves`, `rocks`, `snow`, `flowers`, `abstract`, `grass`

```bash### 1. Enable GitHub Pages

### List Available Reciters

### 5. Generate Your First Video

```powershell

python fetch_quran_reciters.pypython generate_token.py

```

```powershell

---

python generate_quran_video_with_background.py --group "reciter2_s002_001-005" --output "outputs/my_first_video.mp4"```- 📤 Publish to Instagram automatically## FilesSimple scripts to publish images and reels to Instagram via Graph API.

## 📁 Project Structure

```

```

instagram_workflow/

├── generate_quran_video_with_background.py  # Main video generator

├── populate_video_pool.py                   # Auto-verify video fetcher---

├── test_batch_generation.py                 # Batch testing tool

├── approved_videos.json                     # Auto-verified video poolFollow the prompts to:**📖 See [GITHUB_PAGES_SETUP.md](GITHUB_PAGES_SETUP.md) for detailed instructions**

├── requirements.txt                         # Python dependencies

├── .env                                     # API keys (create this)## 📋 Main Scripts

├── outputs/                                 # Generated videos

└── quran_reciters/                         # Reciter data- Authorize your Facebook App

```

| Script | Purpose |

---

|--------|---------|- Get your Instagram Business Account ID- ⏰ GitHub Actions workflows (every 5 minutes)

## 🎯 Auto-Verification Details

| `populate_video_pool.py` | Fetch and auto-verify nature videos from Pixabay |

The system automatically filters videos to ensure **no people appear** and videos are **40+ seconds**:

| `generate_quran_video_with_background.py` | Create Quran video with background |- Generate a long-lived access token (60 days)

### 1. **Duration Filter** ⏱️

```| `test_batch_generation.py` | Generate multiple test videos |

✅ 40+ seconds (fewer loops, smoother playback)

❌ < 40 seconds (rejected automatically)| `fetch_quran_reciters.py` | Get list of available reciters |1. Go to **Settings** → **Pages**

```

| `publish_reel.py` | Publish video to Instagram |

### 2. **People-Free Search Terms**

```The script will save credentials to `instagram_token.json`.

✅ "water drops macro"

✅ "clouds timelapse"---

✅ "fire flames"

✅ "sand texture"2. Source: **Deploy from a branch**- 🔄 Auto token refresh (60-day extension)

✅ "leaves swaying"

✅ "snowflakes closeup"## 🎨 Video Features

❌ "beach vacation"

❌ "mountain hiking"### 3. Add GitHub Secrets

```

### Visual Design

### 3. **Tag Scanning**

Rejects videos with tags containing:- **Font Sizes**: Arabic 90pt, Header 48pt, English 56pt3. Branch: **gh-pages** → **/ (root)**

- people, person, man, woman, human, face

- walking, running, hiking, climbing- **Colors**: Gold verse markers (255,200,100), White text

- tourist, traveler, adventure

- **Layout**: 150px padding from edges, proper RTL supportGo to your repository settings: `Settings → Secrets and variables → Actions → New repository secret`

### 4. **Quality Filters**

- Minimum 100 views (community vetted)- **Verse Markers**: Positioned on left side (Arabic RTL start)

- Like-to-view ratio > 1%

- Editor's Choice preference4. Click **Save**- 🌐 ngrok integration for public URLs

- Popular videos first

### Background Videos

### 5. **Portrait Priority**

- Prefers videos where height > width- **Portrait Format**: Height > Width for Instagram ReelsAdd these secrets:

- Falls back to cropping landscape videos

- **People-Free**: Automated filtering of videos with people

---

- **Categories**: Water, Sky, Fire, Sand, Leaves, Rocks, Snow, Flowers, Abstract, Grass

## 🔍 Troubleshooting

- **Quality**: Popular videos with high view counts

### "PIXABAY_API_KEY not found"

- Ensure `.env` file exists in root directory- `IG_USER_ID` - Your Instagram Business Account ID

- Check for typos in key name

- Restart VS Code after editing `.env`### Audio & Timing



### "No verified videos in pool"- **Word-Level Sync**: Each word highlights as reciter speaks- `LONG_LIVED_TOKEN` - Your access token### 2. Add GitHub Secrets- **`generate_token.py`** - Generate Instagram long-lived access token (60-day expiration)

- Run `python populate_video_pool.py` first

- Check internet connection- **Segment Extraction**: Precise audio cutting for verse ranges

- Verify Pixabay API key is correct

- Note: Fewer videos due to 40+ second filter- **Multiple Reciters**: Support for different recitation styles- `APP_ID` - Your Facebook App ID (optional, for token refresh)



### Video generation fails

- Ensure FFmpeg is installed and in PATH

- Check `quran_reciters/access_token.json` exists---- `APP_SECRET` - Your Facebook App Secret (optional, for token refresh)

- Verify audio URLs are accessible



### Audio not syncing

- Update to latest version (audio extraction fixed)## 🔧 Advanced Usage

- Check reciter timing data is available

- Try different verse groups



### Not enough 40+ second videos found### Batch Generation (20 Videos)### 4. Enable GitHub PagesGo to **Settings** → **Secrets and variables** → **Actions** → **New repository secret**## Files

- Some categories may have fewer long videos

- Script will still add available videos

- Consider running multiple times

- Check Pixabay for category availability```powershell



---python test_batch_generation.py --count 20 --short-only



## 📝 Example Commands```**⚠️ CRITICAL STEP - Required before workflows will work!**



```powershell

# Populate video pool (200+ auto-verified 40+ second videos)

python populate_video_pool.py### Custom Background Category



# Generate single video

python generate_quran_video_with_background.py --group "reciter2_s002_001-005" --output "outputs/test.mp4"

```powershell1. Go to: `Settings → Pages`| Secret | Value | Required |- **`generate_and_publish.py`** - ⭐ All-in-one: Generate & publish (image, reel, or both)

# Generate 5 short test videos

python test_batch_generation.py --count 5 --short-onlypython generate_quran_video_with_background.py --group "reciter2_s002_001-005" --background "water" --output "outputs/water_theme.mp4"



# Publish to Instagram```2. **Source**: Deploy from a branch

python publish_reel.py --video "outputs/test.mp4" --caption "Surah Al-Baqarah"

```



---Available categories: `water`, `sky`, `fire`, `sand`, `leaves`, `rocks`, `snow`, `flowers`, `abstract`, `grass`3. **Branch**: Select `gh-pages` → `/ (root)`|--------|-------|----------|



## 🌟 Credits



- **Quran API**: [Quran Foundation](https://quran.foundation)### List Available Reciters4. Click **Save**

- **Background Videos**: [Pixabay](https://pixabay.com)

- **Arabic Reshaping**: arabic-reshaper library

- **Video Processing**: FFmpeg, OpenCV, MoviePy

```powershell5. Wait 1-2 minutes for GitHub Pages to activate| `IG_USER_ID` | Your Instagram Business Account ID | ✅ Yes |- **`generate_token.py`** - Generate Instagram long-lived access token

---

python fetch_quran_reciters.py

## 📄 License

```

MIT License - See LICENSE file for details



---

---### 5. Verify Setup| `LONG_LIVED_TOKEN` | Long-lived access token (60 days) | ✅ Yes |

## 🤝 Contributing



Issues and pull requests welcome! Please ensure videos remain people-free and content appropriate for Islamic content.

## 📁 Project Structure

---



**Made with ❤️ for spreading Quran recitation**

```1. Wait for the workflow to run (every 5 minutes)| `APP_ID` | Facebook App ID | ⚠️ Recommended (for auto-refresh) |- **`generate_and_publish.py`** - ⭐ All-in-one: Generate & publish (image, reel, or both)- **`publish_image.py`** - Publish single images to Instagram## FilesSimple scripts to publish images and reels to Instagram via Graph API.This repo contains a scheduled GitHub Actions workflow that every 5 minutes:

instagram_workflow/

├── generate_quran_video_with_background.py  # Main video generator2. Check workflow status: `Actions` tab

├── populate_video_pool.py                   # Auto-verify video fetcher

├── test_batch_generation.py                 # Batch testing tool3. Verify your content is accessible:| `APP_SECRET` | Facebook App Secret | ⚠️ Recommended (for auto-refresh) |

├── approved_videos.json                     # Auto-verified video pool

├── requirements.txt                         # Python dependencies   - Image: `https://YOUR_USERNAME.github.io/instagram_workflow/image.jpg`

├── .env                                     # API keys (create this)

├── outputs/                                 # Generated videos   - Video: `https://YOUR_USERNAME.github.io/instagram_workflow/reel.mp4`- **`publish_image.py`** - Publish single images

└── quran_reciters/                         # Reciter data

```4. Check your Instagram profile for new posts!



---**Note:** `NGROK_AUTHTOKEN` is NO LONGER NEEDED! 🎉



## 🎯 Auto-Verification Details## Project Structure



The system automatically filters videos to ensure **no people appear**:- **`publish_reel.py`** - Publish video reels- **`publish_reel.py`** - Publish video reels to Instagram



### 1. **People-Free Search Terms**```

```

✅ "water drops macro"instagram_workflow/### 3. Generate Tokens

✅ "clouds timelapse"

✅ "fire flames"├── .github/workflows/

✅ "sand texture"

✅ "leaves swaying"│   └── publish-content-every-5m.yml  # Main workflow (alternates image/reel)- **`generate_video_ffmpeg.py`** - Generate random color videos

❌ "beach vacation"

❌ "mountain hiking"├── generate_token.py          # Interactive token generation

```

├── generate_video_ffmpeg.py   # Video generation with ffmpeg```bash

### 2. **Tag Scanning**

Rejects videos with tags containing:├── publish_image.py           # Image publisher with token refresh

- people, person, man, woman, human, face

- walking, running, hiking, climbing├── publish_reel.py            # Reel publisher with token refreshpython generate_token.py- **`generate_video_ffmpeg.py`** - Generate random color frame videos (9:16 aspect ratio)

- tourist, traveler, adventure

├── requirements.txt           # Python dependencies

### 3. **Quality Filters**

- Minimum 100 views (community vetted)├── README.md                  # This file```

- Like-to-view ratio > 1%

- Editor's Choice preference├── GITHUB_PAGES_SETUP.md      # Detailed GitHub Pages setup



### 4. **Portrait Priority**├── SETUP_CHECKLIST.md         # Step-by-step setup guide## Quick Start (Local)

- Prefers videos where height > width

- Falls back to cropping landscape videos└── ENABLE_GITHUB_PAGES.md     # Important setup notice



---```Follow the prompts to get your credentials.



## 🔍 Troubleshooting



### "PIXABAY_API_KEY not found"## Manual Publishing (Optional)

- Ensure `.env` file exists in root directory

- Check for typos in key name

- Restart VS Code after editing `.env`

You can also publish content manually:### 4. Done! ✨

### "No verified videos in pool"

- Run `python populate_video_pool.py` first

- Check internet connection

- Verify Pixabay API key is correct### Publish an Image```powershell



### Video generation fails

- Ensure FFmpeg is installed and in PATH

- Check `quran_reciters/access_token.json` exists```bashWorkflows will run automatically every 5 minutes!

- Verify audio URLs are accessible

python publish_image.py https://example.com/your-image.jpg

### Audio not syncing

- Update to latest version (audio extraction fixed)```# 1. Generate token## Setup- **`generate_token.py`** - Generate Instagram long-lived access token (60-day expiration)- generates a short vertical (9:16) random color-frames MP4 and thumbnails,

- Check reciter timing data is available

- Try different verse groups



---### Publish a Reel## Workflows



## 📝 Example Commands



```powershell```bashpython generate_token.py

# Populate video pool (200+ auto-verified videos)

python populate_video_pool.pypython publish_reel.py https://example.com/your-video.mp4



# Generate single video```### 📸 Image Workflow (`publish-image-every-5m.yml`)

python generate_quran_video_with_background.py --group "reciter2_s002_001-005" --output "outputs/test.mp4"



# Generate 5 short test videos

python test_batch_generation.py --count 5 --short-only## Requirements- Generates random color image



# Publish to Instagram

python publish_reel.py --video "outputs/test.mp4" --caption "Surah Al-Baqarah"

```### Python Dependencies- Deploys to GitHub Pages



---



## 🌟 Credits```bash- Publishes to Instagram# 2. Set environment variables



- **Quran API**: [Quran Foundation](https://quran.foundation)pip install requests pillow

- **Background Videos**: [Pixabay](https://pixabay.com)

- **Arabic Reshaping**: arabic-reshaper library```- **URL**: `https://tamer017.github.io/instagram_workflow/image.jpg`

- **Video Processing**: FFmpeg, OpenCV, MoviePy



---

### System Dependencies$env:IG_USER_ID="your_instagram_business_account_id"1. **Generate Token**:- **`generate_and_publish.py`** - ⭐ All-in-one: Generate image & video, serve via ngrok, publish both

## 📄 License



MIT License - See LICENSE file for details

- **ffmpeg** (for video generation)### 🎥 Reel Workflow (`publish-reel-every-5m.yml`)

---

  - Windows: `choco install ffmpeg`

## 🤝 Contributing

  - Mac: `brew install ffmpeg`- Generates random color video$env:LONG_LIVED_TOKEN="your_long_lived_token"

Issues and pull requests welcome! Please ensure videos remain people-free and content appropriate for Islamic content.

  - Linux: `sudo apt install ffmpeg`

---

- Deploys to GitHub Pages

**Made with ❤️ for spreading Quran recitation**

## How the Workflow Works

- Publishes to Instagram$env:APP_ID="your_facebook_app_id"   ```bash

```yaml

Schedule: Every 5 minutes (*/5 * * * *)- **URL**: `https://tamer017.github.io/instagram_workflow/reel.mp4`



Even Minutes (0, 2, 4, 6, 8...):$env:APP_SECRET="your_facebook_app_secret"

  1. Generate random color image (1080x1080 JPEG)

  2. Deploy to GitHub Pages (gh-pages branch)## How It Works

  3. Wait 30 seconds for deployment

  4. Verify URL is accessible (10 retries)   python generate_token.py- **`publish_image.py`** - Publish single images to Instagram## Files- serves the `outputs/` directory via a local HTTP server on the runner,

  5. Publish to Instagram

```

Odd Minutes (1, 3, 5, 7, 9...):

  1. Generate random color video (1080x1920 MP4, 2 seconds)┌─────────────────────────────────────┐# 3. Publish

  2. Deploy to GitHub Pages (gh-pages branch)

  3. Wait 30 seconds for deployment│ 1. GitHub Actions triggers         │

  4. Verify URL is accessible (10 retries)

  5. Publish to Instagram│    (every 5 minutes)                │python generate_and_publish.py image  # Image only   ```

```

├─────────────────────────────────────┤

## Token Management

│ 2. Generate random color content   │python generate_and_publish.py reel   # Reel only

### Token Lifespan

│    • Image: 1080x1920 JPEG          │

- **Short-lived token**: 1 hour

- **Long-lived token**: 60 days│    • Video: 1080x1920 MP4 H.264     │python generate_and_publish.py both   # Both   Follow the prompts to get your credentials.- **`publish_reel.py`** - Publish video reels to Instagram

- **Auto-refresh**: Extends by 60 days on each publish

├─────────────────────────────────────┤

### Manual Token Refresh

│ 3. Deploy to GitHub Pages          │```

To manually refresh your token:

│    • Branch: gh-pages               │

```bash

python generate_token.py│    • URL: github.io/repo/file.jpg   │

```

├─────────────────────────────────────┤

Or update the `LONG_LIVED_TOKEN` secret in GitHub.

│ 4. Publish to Instagram            │## GitHub Actions Setup (Automated Every 5 Minutes)

## Troubleshooting

│    • Uses GitHub Pages URL          │

### Workflow Fails with "404 Not Found"

│    • Auto-refreshes token           │2. **Set Environment Variables**:- **`generate_video_ffmpeg.py`** - Generate random color frame videos (9:16 aspect ratio)- exposes the server via ngrok v3, and

**Cause**: GitHub Pages is not enabled.

│    • Posts appear on your profile   │

**Solution**: 

1. Go to `Settings → Pages`└─────────────────────────────────────┘### Step 1: Add Repository Secrets

2. Set Source to `gh-pages` branch

3. Save and wait 1-2 minutes```



### "Media download has failed" Error   ```powershell



**Cause**: URL is not accessible or GitHub Pages is still deploying.## Manual Usage



**Solution**: The workflow has built-in retry logic (10 attempts). If it still fails:Go to: **Repository Settings** → **Secrets and variables** → **Actions** → **New repository secret**

1. Verify GitHub Pages is enabled

2. Check the URL manually in a browser### Generate Token

3. Wait a few minutes for GitHub Pages to activate

```bash   # PowerShell

### Token Expired

python generate_token.py

**Cause**: Token hasn't been refreshed in 60 days (workflows stopped running).

```| Secret Name | Description | Required |

**Solution**: 

1. Run `python generate_token.py` to get a new token

2. Update the `LONG_LIVED_TOKEN` secret

3. Workflows will auto-refresh it from now on### Publish Image (Manual)|-------------|-------------|----------|   $env:IG_USER_ID="your_instagram_business_account_id"



### No Posts Appearing```bash



**Checklist**:# Set credentials| `IG_USER_ID` | Instagram Business Account ID | ✅ Yes |

- ✅ GitHub Pages enabled in repository settings

- ✅ Secrets configured correctly (IG_USER_ID, LONG_LIVED_TOKEN)$env:IG_USER_ID="your_id"

- ✅ Workflow running successfully (green checkmarks in Actions tab)

- ✅ Instagram account is a Business or Creator account$env:LONG_LIVED_TOKEN="your_token"| `LONG_LIVED_TOKEN` | Long-lived access token (60 days) | ✅ Yes |   $env:LONG_LIVED_TOKEN="your_long_lived_token"## Setup- **`generate_token.py`** - Generate Instagram long-lived access token (60-day expiration)- publishes the video as a REEL to Instagram using the Facebook Graph API.

- ✅ Facebook Page connected to Instagram account



## Cost

# Publish with custom URL| `APP_ID` | Facebook App ID | ⚠️ Recommended |

**100% FREE!**

python publish_image.py https://example.com/image.jpg "Caption"

- GitHub Actions: 2,000 minutes/month (free tier)

- GitHub Pages: Free for public repositories| `APP_SECRET` | Facebook App Secret | ⚠️ Recommended |   $env:APP_ID="your_facebook_app_id"

- No server costs, no hosting fees

# Or use default random image

This workflow uses ~1 minute per run = ~300 minutes/month (well within free tier).

python publish_image.py| `NGROK_AUTHTOKEN` | ngrok auth token (from https://dashboard.ngrok.com/get-started/your-authtoken) | ⚠️ Recommended |

## Instagram API Requirements

```

Your Instagram account must be:

- **Business** or **Creator** account (not personal)   $env:APP_SECRET="your_facebook_app_secret"

- Connected to a **Facebook Page**

- Have a **Facebook App** with Instagram Graph API access### Publish Reel (Manual)



See `generate_token.py` for the complete setup process.```bash### Step 2: Enable Workflows



## Securitypython publish_reel.py https://example.com/video.mp4 "Caption"



- Never commit `instagram_token.json` (already in `.gitignore`)```   ```

- Keep your secrets secure in GitHub repository settings

- Don't share your access tokens

- Tokens auto-refresh to stay valid

### Generate Video1. Go to **Actions** tab

## Contributing

```bash

Feel free to:

- Open issues for bugs or feature requestspython generate_video_ffmpeg.py2. Enable GitHub Actions if prompted1. **Generate Token**:- **`publish_image.py`** - Publish single images to Instagram

- Submit pull requests for improvements

- Share your creative modifications!# Creates: outputs/video.mp4



## License```3. Two workflows will run automatically:



This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.



## Acknowledgments## Files   - **Publish Image** - Every 5 minutes3. **Install ngrok** (for all-in-one script):



- Instagram Graph API documentation

- GitHub Actions for automation

- GitHub Pages for free hosting- `generate_token.py` - Generate Instagram credentials   - **Publish Reel** - Every 5 minutes

- ffmpeg for video processing

- `publish_image.py` - Publish images to Instagram

## Need Help?

- `publish_reel.py` - Publish reels to Instagram   ```bash   ```bash

1. Check the [SETUP_CHECKLIST.md](SETUP_CHECKLIST.md) for step-by-step instructions

2. Read [GITHUB_PAGES_SETUP.md](GITHUB_PAGES_SETUP.md) for detailed GitHub Pages setup- `generate_video_ffmpeg.py` - Generate random color videos

3. See [ENABLE_GITHUB_PAGES.md](ENABLE_GITHUB_PAGES.md) if workflows are failing

4. Open an issue on GitHub if you need assistance- `generate_and_publish.py` - All-in-one script (legacy, for local use with ngrok)### Step 3: Test (Optional)



---



Made with ❤️ for automated Instagram content creation## Requirements   # Download from https://ngrok.com/download




```bashManual trigger:

pip install -r requirements.txt

```1. Go to **Actions** tab   # Or via chocolatey:   python generate_token.py- **`publish_reel.py`** - Publish video reels to Instagram📖 **New to Instagram API?** Read [`INSTAGRAM_API_GUIDE.md`](INSTAGRAM_API_GUIDE.md) for a complete explanation of how the workflow works, token management, and troubleshooting.



- Python 3.7+2. Select workflow (image or reel)

- pillow

- requests3. Click **Run workflow** → **Run workflow**   choco install ngrok

- ffmpeg (for video generation)



## GitHub Pages vs ngrok

### Workflows   ```   ```

| Feature | GitHub Pages | ngrok |

|---------|--------------|-------|

| Instagram compatibility | ✅ Works perfectly | ❌ Blocked |

| Setup | Simple | Complex |**📸 `publish-image-every-5m.yml`**

| Auth token | Not needed | Required |

| Cost | Free | Free tier limited |- Generates random color image

| Reliability | High | Medium |

| URL | Permanent | Temporary |- Publishes to Instagram## Usage   Follow the prompts to get your credentials.- **`generate_video_ffmpeg.py`** - Generate random color frame videos (9:16 aspect ratio)



## Token Management- Runs every 5 minutes



### Auto-Refresh



When `APP_ID` and `APP_SECRET` are set:**🎥 `publish-reel-every-5m.yml`**

- ✅ Token refreshes on every publish

- ✅ Expiration extends by 60 days- Generates random color video### ⭐ All-in-One: Generate & Publish

- ✅ Workflows run forever!

- Publishes to Instagram

### Without Auto-Refresh

- Runs every 5 minutes```bash

- Token expires after 60 days

- Must manually run `generate_token.py`

- Update `LONG_LIVED_TOKEN` secret

**Schedule:**# Publish both image and reel (default)2. **Set Environment Variables**:## Setup: Get Your Instagram Token

## Testing

```yaml

### Manual Workflow Trigger

1. Go to **Actions** tabcron: '*/5 * * * *'  # Every 5 minutespython generate_and_publish.py

2. Select workflow (image or reel)

3. Click **Run workflow** → **Run workflow**```

4. Wait ~30 seconds

5. Check Instagram profile!   ```powershell



### Verify GitHub Pages### What Happens Automatically

Visit: `https://tamer017.github.io/instagram_workflow/image.jpg`

# Or specify what to publish:

Should show the latest generated image.

Each workflow run:

## Troubleshooting

1. ✅ Installs Python, ffmpeg, ngrokpython generate_and_publish.py both   # Both image and reel   # PowerShell## Setup

**Workflow fails?**

- Check GitHub Pages is enabled (Settings → Pages)2. ✅ Generates random color content

- Verify all secrets are set correctly

- Check Actions logs for specific errors3. ✅ Starts HTTP serverpython generate_and_publish.py image  # Only image



**Image not on Instagram?**4. ✅ Creates ngrok tunnel (public HTTPS URL)

- Check GitHub Pages URL is accessible

- Verify token hasn't expired5. ✅ Publishes to Instagrampython generate_and_publish.py reel   # Only reel (video)   $env:IG_USER_ID="your_instagram_business_account_id"

- Check Instagram API limits (not exceeded)

6. ✅ Refreshes token (extends 60-day expiration)

**GitHub Pages 404?**

- Wait for first workflow run```

- Check `gh-pages` branch exists

- Settings → Pages → Verify branch selected## Usage



## Documentation   $env:LONG_LIVED_TOKEN="your_long_lived_token"**📺 Watch Tutorial**: For a video walkthrough, see: https://www.youtube.com/watch?v=dbzzLEHXLck



- 📖 [GITHUB_PAGES_SETUP.md](GITHUB_PAGES_SETUP.md) - Detailed GitHub Pages setup### All-in-One Script

- 🔧 [TROUBLESHOOTING.md](TROUBLESHOOTING.md) - Common issues and solutions

- 🔐 [NGROK_SETUP.md](NGROK_SETUP.md) - Legacy ngrok setup (not needed anymore)**What it does:**



## Schedule```bash



Both workflows run on:python generate_and_publish.py [mode]- Generates random color content (image/video/both)   $env:APP_ID="your_facebook_app_id"

```yaml

cron: '*/5 * * * *'  # Every 5 minutes

```

Modes:- Starts HTTP server and ngrok tunnel

You can modify the schedule in the workflow files.

  image  - Generate and publish image only

## Notes

  reel   - Generate and publish reel only- Publishes to Instagram automatically   $env:APP_SECRET="your_facebook_app_secret"1. **Generate Token**:

- ✅ GitHub Pages hosting is free and reliable

- ✅ No ngrok configuration needed  both   - Generate and publish both (default)

- ✅ Instagram-friendly domain

- ✅ Content updates within 10 seconds```- Auto-refreshes token (if APP_ID/APP_SECRET set)

- ✅ Files are publicly accessible (as required)

- ⚠️ GitHub Pages has 100GB/month bandwidth (more than enough)

- ⚠️ Each workflow overwrites previous content

### Individual Scripts   ```

## License



See LICENSE file for details.

```bash**Examples:**

# Publish image (uses default random image)

python publish_image.py```bash   ```bash**Option 1: Automated Script (Recommended)**



# Publish image with custom URL# Quick test with just an image

python publish_image.py https://example.com/image.jpg "My caption"

python generate_and_publish.py image3. **Install ngrok** (for all-in-one script):

# Publish reel (uses default demo video)

python publish_reel.py



# Publish reel with custom URL# Quick test with just a reel   ```bash   python generate_token.py```powershell

python publish_reel.py https://example.com/video.mp4 "My caption"

python generate_and_publish.py reel

# Generate video only (saves to outputs/)

python generate_video_ffmpeg.py   # Download from https://ngrok.com/download

```

# Publish both (default)

## Requirements

python generate_and_publish.py both   # Or via chocolatey:   ```python generate_instagram_token.py

```bash

pip install -r requirements.txt```

```

   choco install ngrok

- Python 3.7+

- ffmpeg### Publish Image Only

- ngrok

- pillow```bash   ```   Follow the prompts to get your credentials.```

- requests

# With default random image

## Publishing Modes

python publish_image.py

| Mode | Image | Video | Use Case |

|------|-------|-------|----------|

| `image` | ✅ | ❌ | Quick photo posts |

| `reel` | ❌ | ✅ | Quick video posts |# With custom image URL## UsageThe script will guide you through:

| `both` | ✅ | ✅ | Full content drop |

python publish_image.py https://example.com/image.jpg "My caption"

## Token Management

```

### Auto-Refresh



When `APP_ID` and `APP_SECRET` are set:

- Token refreshes automatically on each publish### Publish Reel Only### ⭐ All-in-One: Generate & Publish Everything2. **Set Environment Variables**:1. Getting a short-lived token via Facebook Graph API Explorer or OAuth

- Expiration extends by 60 days

- No manual intervention needed```bash

- **Workflows run forever!** ✨

# With default demo video```bash

### Without Auto-Refresh

python publish_reel.py

- Token expires after 60 days

- Must manually run `generate_token.py` to regeneratepython generate_and_publish.py   ```bash2. Exchanging it for a long-lived token (valid ~60 days)

- Update `LONG_LIVED_TOKEN` secret in GitHub

# With custom video URL

## Content Specifications

python publish_reel.py https://example.com/video.mp4 "My caption"```

**Images:**

- 9:16 aspect ratio (1080x1920)```

- JPEG format

- Public HTTPS URL requiredThis will:   export IG_USER_ID="your_instagram_business_account_id"3. Finding your Instagram Business Account ID from your Facebook Page



**Videos (Reels):**### Generate Video Only

- 9:16 aspect ratio (1080x1920)

- H.264 codec, yuv420p```bash1. ✅ Generate a random color image (1080x1920, 9:16)

- Max 60 seconds

- Public HTTPS URL requiredpython generate_video_ffmpeg.py



## Troubleshooting```2. ✅ Generate a random color video (1080x1920, 9:16, 5 seconds)   export LONG_LIVED_TOKEN="your_long_lived_token"4. Validating the token and showing your Instagram User ID



**"No Facebook Pages found"**Creates `outputs/video.mp4` with random color frames.

→ Create Facebook Page and link Instagram Business Account

3. ✅ Start HTTP server and ngrok tunnel

**"ngrok tunnel failed"**

→ Add `NGROK_AUTHTOKEN` secret (get from https://ngrok.com)## Requirements



**"Token expired"**4. ✅ Publish image to Instagram   export APP_ID="your_facebook_app_id"5. Optionally saving to `instagram_token.json`

→ Add `APP_ID` + `APP_SECRET` for auto-refresh

```bash

**Workflow not running**

→ Check Actions tab, verify secrets are setpip install -r requirements.txt5. ✅ Publish video to Instagram



**Both workflows running**```

→ Yes, they can run simultaneously. Disable one if needed (Settings → Actions)

   export APP_SECRET="your_facebook_app_secret"

## Notes

- Python 3.7+

- 🔐 Never commit tokens to git (use `.gitignore`)

- ⏰ Workflows run every 5 minutes (can be adjusted in workflow files)- ffmpeg (for video generation)**No manual steps needed!** Just run the script and it handles everything.

- 🌐 ngrok free tier is sufficient

- 📁 Generated content saved to `outputs/`- ngrok (for all-in-one script)

- 🔄 Both workflows can run at the same time

- requests   ```**Option 2: Manual Steps**

- pillow

### Publish Image Only

## Token Refresh

```bashSee `token_help.md` for detailed manual instructions.

All publish scripts automatically refresh your token if `APP_ID` and `APP_SECRET` are set. This extends token expiration by 60 days on each run.

# With default random image

## Notes

python publish_image.py## Usage

- Images/videos must be publicly accessible HTTPS URLs

- Videos: 9:16 aspect ratio, H.264 codec, max 60s duration

- Images: 9:16 aspect ratio recommended

- Keep your tokens secure - never commit them to git!# With custom image URL**Option 3: Complete Guide**

- The all-in-one script keeps ngrok running until you press Ctrl+C

python publish_image.py https://example.com/image.jpg "My caption"

## Quick Start

```### Publish ImageRead [`INSTAGRAM_API_GUIDE.md`](INSTAGRAM_API_GUIDE.md) for in-depth explanation of tokens, permissions, and the publishing workflow.

```powershell

# 1. Set credentials (from generate_token.py output)

$env:IG_USER_ID="17841477131944862"

$env:LONG_LIVED_TOKEN="your_token_here"### Publish Reel Only```bash

$env:APP_ID="1828867114681315"

$env:APP_SECRET="your_secret_here"```bash



# 2. Publish an image# With default demo videopython publish_image.py https://example.com/image.jpg "My caption"## Required Repository Secrets

python generate_and_publish.py image

python publish_reel.py

# 3. Publish a reel

python generate_and_publish.py reel```



# 4. Publish both# With custom video URL

python generate_and_publish.py both

```python publish_reel.py https://example.com/video.mp4 "My caption"Add these in GitHub: Settings → Secrets and variables → Actions → New repository secret



## Modes Comparison```



| Mode | Image Generated | Video Generated | Image Published | Reel Published |### Publish Reel

|------|----------------|-----------------|-----------------|----------------|

| `image` | ✅ | ❌ | ✅ | ❌ |### Generate Video Only

| `reel` | ❌ | ✅ | ❌ | ✅ |

| `both` | ✅ | ✅ | ✅ | ✅ |```bash```bash### Core Secrets (Required):


python generate_video_ffmpeg.py

```python publish_reel.py https://example.com/video.mp4 "My caption"- `IG_USER_ID` — Instagram Business Account ID (from token script)

Creates `outputs/video.mp4` with random color frames.

```- `LONG_LIVED_TOKEN` — Instagram long-lived user token (from token script)

## Requirements

- `NGROK_AUTHTOKEN` — ngrok v3 authtoken (get from https://dashboard.ngrok.com/get-started/your-authtoken)

```bash

pip install -r requirements.txt### Generate Video

```

```bash### Auto-Refresh Secrets (Highly Recommended):

- Python 3.7+

- ffmpeg (for video generation)python generate_video_ffmpeg.py- `APP_ID` — Your Facebook App ID (same one used in token generation)

- ngrok (for all-in-one script)

- requests```- `APP_SECRET` — Your Facebook App Secret (same one used in token generation)

- pillow

Creates `outputs/video.mp4` with random color frames.

## Token Refresh

**With APP_ID and APP_SECRET**: Token automatically refreshes every time the workflow runs, extending expiration by 60 days. The workflow updates the `LONG_LIVED_TOKEN` secret automatically. **Runs forever! ✓**

All publish scripts (`publish_image.py`, `publish_reel.py`, and `generate_and_publish.py`) automatically refresh your token if `APP_ID` and `APP_SECRET` are set. This extends token expiration by 60 days on each run.

## Requirements

## Notes

**Without them**: Token expires after 60 days, and you'll need to manually regenerate and update it.

- Images/videos must be publicly accessible HTTPS URLs

- Videos: 9:16 aspect ratio, H.264 codec, max 60s duration```bash

- Images: 9:16 aspect ratio recommended

- Keep your tokens secure - never commit them to git!pip install -r requirements.txt📖 **Setup Guide**: See [`AUTO_REFRESH_SETUP.md`](AUTO_REFRESH_SETUP.md) for detailed instructions on setting up automatic token refresh.

- The all-in-one script keeps ngrok running until you press Ctrl+C

```

## Workflow

⚠️ **Security**: Never commit tokens to git! See [`SECURITY.md`](SECURITY.md) for best practices.

```

generate_and_publish.py Flow:- Python 3.7+

┌─────────────────────────────────────┐

│ 1. Generate random color image      │- ffmpeg (for video generation)Workflow file: `.github/workflows/publish-reel-every-5m.yml`.

│    └─> outputs/generated_image.jpg  │

├─────────────────────────────────────┤- requests

│ 2. Generate random color video      │

│    └─> outputs/generated_video.mp4  │- pillowRun options:

├─────────────────────────────────────┤

│ 3. Start HTTP server (port 8000)    │- Scheduled: runs every 5 minutes via cron.

│    └─> Serves outputs/ directory    │

├─────────────────────────────────────┤## Token Refresh- Manual: Actions -> "Publish random-color reel every 5 minutes" -> Run workflow.

│ 4. Start ngrok tunnel               │

│    └─> Get public HTTPS URL         │

├─────────────────────────────────────┤

│ 5. Publish image                    │Both `publish_image.py` and `publish_reel.py` automatically refresh your token if `APP_ID` and `APP_SECRET` are set. This extends token expiration by 60 days on each run.Local testing (optional):

│    └─> https://ngrok.../image.jpg   │

├─────────────────────────────────────┤1. Install deps: `pip install -r requirements.txt` and ensure `ffmpeg` is on PATH.

│ 6. Publish video                    │

│    └─> https://ngrok.../video.mp4   │## Notes2. Generate assets: `python generate_video_ffmpeg.py outputs 3 24 3`.

└─────────────────────────────────────┘

```3. Serve `outputs/` and expose publicly (e.g., with ngrok), then set `VIDEO_URL` and `THUMBNAIL_URL` env vars and run `python publish_reel.py`.


- Images/videos must be publicly accessible HTTPS URLs

- Videos: 9:16 aspect ratio, H.264 codec, max 60s duration**Publishing images instead of reels:**

- Keep your tokens secure - never commit them to git!```powershell

# Publish a single image from a public URL
python publish_image.py "https://example.com/image.jpg" "Your caption"

# Or use environment variables
$env:IMAGE_URL="https://example.com/image.jpg"
$env:CAPTION="Your caption"
python publish_image.py
```

## Troubleshooting Token Generation

**Issue: "No Facebook Pages found"**

Your token has the right permissions, but you need to set up the Facebook Page → Instagram connection:

1. **Create a Facebook Page**: https://www.facebook.com/pages/creation/
   - Choose any category (Business, Community, etc.)
   - Fill in basic information
   
2. **Convert Instagram to Business Account** (if not already):
   - Instagram app → Settings → Account
   - "Switch to Professional Account" → Choose Business or Creator

3. **Link Instagram to Facebook Page**:
   - **Option A** - From Instagram app:
     - Settings → Account → Linked accounts → Facebook Page
     - Select the Page you created
   - **Option B** - From Facebook Page:
     - Your Page → Settings → Instagram → Connect account
     - Log in to your Instagram

4. **Verify**: Visit https://business.facebook.com/settings/instagram-accounts
   - You should see your Instagram account linked to your Page

5. **Run the script again** - it will now find your Page and Instagram account!

---

**Issue: "Missing required permissions"**
- In Graph API Explorer, ensure you select these permissions:
  - ✓ `pages_show_list` (REQUIRED)
  - ✓ `pages_read_engagement` (REQUIRED)
  - ✓ `instagram_basic`
  - ✓ `instagram_content_publish`

**Issue: "No Instagram Business Account found"**
- Your Instagram must be a Business or Creator account (not personal)
- It must be linked to a Facebook Page (see steps above)

**Issue: Token validation fails**
- The script will show which permissions are missing
- Go back to Graph API Explorer and regenerate with all required permissions

Notes:
- API version is pinned to `v17.0` in scripts.
- Polling waits for `status_code == FINISHED` before publishing.
- Ensure media URLs are publicly accessible when publishing.

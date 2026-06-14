# 🎦 Quranic Video Generator for Instagram

Automated system to generate beautiful Quran recitation videos with Arabic text overlays and publish to Instagram using GitHub Actions.

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![GitHub Actions](https://img.shields.io/badge/CI%2FCD-GitHub_Actions-black.svg)](https://github.com/features/actions)
[![FFmpeg](https://img.shields.io/badge/Video-FFmpeg-red.svg)](https://ffmpeg.org/)
[![Status](https://img.shields.io/badge/Status-Active%20%26%20Maintained-brightgreen.svg)]()

---

## ✨ Features

- 🎥 **Background Videos**: Nature scenes (water, fire, flowers, sky, etc.)
- 📱 **Instagram Reels Optimized**: 1080×1920 (9:16 portrait format)
- 🏽️ **Audio Sync**: Word-level Quranic text synchronized with reciter audio
- 📖 **Othmani Script**: Full Arabic text with tashkeel (diacritics)
- 🌍 **Multiple Reciters**: 12+ Quranic reciters available
- 🎨 **Bilingual**: Arabic and English translations
- ⚡ **Automated**: GitHub Actions workflows for generation and publishing
- 📤 **Auto-Publishing**: Posts to Instagram every 5 minutes
- 🔐 **Secure**: Private repository with GitHub Secrets

---

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Generate Videos Locally

```bash
# Generate video for a specific group
python generate_simple_video.py --group reciter1_s001_001-007
```

Output saved to: `generated_videos/`

### 3. Setup GitHub Actions (Automated)

#### Add Repository Secrets:
1. Go to: **Settings → Secrets and variables → Actions**
2. Add these secrets:
   - `IG_USER_ID` — Instagram Business Account ID
   - `LONG_LIVED_TOKEN` — Facebook Page access token
   - `APP_ID` — Facebook App ID
   - `APP_SECRET` — Facebook App Secret (optional, for auto-refresh)
   - `REEL_CAPTION` — (optional) Default caption

---

## 🤖 GitHub Actions Workflows

### 1. Publish Quranic Reels (Every 5 Minutes)
- **File**: `.github/workflows/publish-reel-automated.yml`
- **Action**: Generates and publishes Quranic reels to Instagram
- **Requirements**: Instagram API credentials

### 2. Push Generated Videos to Repository
- **File**: `.github/workflows/push-generated-videos.yml`
- **Action**: Generates videos and commits to repository
- **Schedule**: Every 30 minutes

### Run Manually:
1. Go to: **Actions** tab
2. Select workflow
3. Click **"Run workflow"** button
4. Check progress in real-time

---

## 🎯 Supported Reciters

- AbdulBaset AbdulSamad
- Abdur-Rahman as-Sudais
- Abu Bakr al-Shatri
- Hani ar-Rifai
- Mahmoud Khalil Al-Husary
- Mishari Rashid al-Afasy
- Mohamed Siddiq al-Minshawi
- Sa`ud ash-Shuraym
- Mohamed al-Tablawi
- And 3 more...

---

## 📁 Project Structure

```
instagram_workflow/
├── .github/workflows/           # GitHub Actions
├── quran_groups/                # Quranic verse groups
├── generated_videos/            # Output videos
├── fonts/                       # Arabic fonts
├── generate_simple_video.py     # Main generator
├── publish_reel.py              # Publishing script
└── requirements.txt
```

---

## 🔤 Arabic Text Support

- **Othmani Script**: Traditional Quranic writing
- **Full Tashkeel**: Complete diacritical marks
- **RTL Support**: Proper right-to-left rendering
- **Auto-Downloaded Fonts**: Best available Quranic fonts

---

## 🛠️ Usage Examples

```bash
# Generate with all text
python generate_simple_video.py --group reciter1_s001_001-007

# Generate without Arabic text
python generate_simple_video.py --group reciter1_s001_001-007 --no-arabic-text

# Generate without English text
python generate_simple_video.py --group reciter1_s001_001-007 --no-english-text
```

---

## 📊 Repository Privacy

✅ **Keep repository PRIVATE** for security
- All workflows work normally
- Instagram credentials stored safely in GitHub Secrets
- Branches automatically private at repository level

---

## 🔐 Security

- ✅ Never commit credentials to git
- ✅ Use GitHub Secrets for all sensitive data
- ✅ Keep repository PRIVATE
- ✅ Rotate tokens every 60 days

---

## 🔍 Troubleshooting

### FFmpeg not found
```bash
sudo apt-get install ffmpeg  # Linux
brew install ffmpeg          # macOS
choco install ffmpeg         # Windows
```

### Arabic text not rendering
- Verify fonts are in `fonts/` directory
- Fonts auto-download if missing

### Instagram publishing fails
- Verify `IG_USER_ID` is correct
- Check token hasn't expired
- Ensure credentials are in GitHub Secrets

---

## 📄 License

See LICENSE file

---

## 🤝 Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Push and create a Pull Request

---

**Last Updated**: November 22, 2025  
**Status**: ✅ Active & Maintained

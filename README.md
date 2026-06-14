# Instagram Automated Video Publishing Workflow

> A fully automated, CI/CD-driven pipeline that downloads, processes, and publishes video content to Instagram Reels using **FFmpeg**, **Instagrapi**, and **GitHub Actions**.

[![CI/CD](https://img.shields.io/badge/CI%2FCD-GitHub%20Actions-2088FF?style=flat-square&logo=github-actions)](https://github.com/features/actions)
[![Language](https://img.shields.io/badge/Language-Python%203.x-green?style=flat-square)](https://www.python.org/)
[![Video](https://img.shields.io/badge/Processing-FFmpeg-red?style=flat-square)](https://ffmpeg.org/)

---

## Overview

This project implements a **serverless video content pipeline** that automates the entire lifecycle of Instagram Reels publishing — from raw video download to fully formatted, scheduled publication. Designed around a cloud-native GitHub Actions CI/CD workflow, the pipeline eliminates manual intervention by chaining Python-based automation utilities with powerful CLI video processing tools.

All secrets (credentials, API tokens) are managed securely via GitHub Secrets, making the pipeline safe for use in public repositories without credential exposure.

---

## Pipeline Architecture

```
[Trigger: GitHub Actions Schedule / Manual Dispatch]
              |
              v
   [Step 1: Download Video]
   yt-dlp or requests-based downloader
              |
              v
   [Step 2: Video Processing — FFmpeg]
   • Transcode to H.264 / AAC
   • Scale to 9:16 vertical (1080×1920)
   • Trim, add watermark/overlay
   • Inject metadata
              |
              v
   [Step 3: Publish to Instagram — Instagrapi]
   • Authenticate with Instagram session
   • Upload as Reel with caption & hashtags
   • Optional: Add location, collaborators
              |
              v
   [Step 4: Notify / Log]
   • Commit upload log back to repository
   • Slack/Telegram notification (optional)
```

---

## Technical Highlights

### FFmpeg Video Processing
- Transcodes arbitrary input videos to **Instagram-compatible H.264/AAC MP4**
- Applies vertical crop/scale to enforce **9:16 aspect ratio** (1080×1920 for Reels)
- Supports overlay injection for watermarks, text burned via `drawtext` filter
- Normalizes audio levels with `loudnorm` filter for consistent volume

### Instagrapi — Instagram API Client
- Uses the unofficial but robust **Instagrapi** library for programmatic Instagram interaction
- Handles **session management** and two-factor authentication (2FA) challenge resolution
- Publishes Reels with full caption, hashtag set, and cover thumbnail selection

### GitHub Actions — Serverless Scheduler
- Triggered via `cron` schedule or `workflow_dispatch` (manual trigger)
- Manages Python dependencies with `pip cache` for faster runs
- Stores Instagram credentials, session cookies, and API tokens as **encrypted GitHub Secrets**
- Outputs structured logs with upload status for debugging

### Secure Secrets Management
```yaml
# .github/workflows/publish.yml (excerpt)
env:
  IG_USERNAME: ${{ secrets.IG_USERNAME }}
  IG_PASSWORD: ${{ secrets.IG_PASSWORD }}
  SESSION_FILE: ${{ secrets.IG_SESSION }}
```

---

## Project Structure

```
instagram_workflow/
├── .github/
│   └── workflows/
│       └── publish.yml      # GitHub Actions workflow definition
├── scripts/
│   ├── download.py          # Video acquisition
│   ├── process.py           # FFmpeg processing pipeline
│   └── publish.py           # Instagrapi upload logic
├── config/
│   └── settings.py          # Caption templates, hashtag sets
└── requirements.txt
```

---

## Getting Started

```bash
# Clone the repository
git clone https://github.com/tamer017/instagram_workflow.git
cd instagram_workflow

# Install Python dependencies
pip install -r requirements.txt

# Install FFmpeg (required)
brew install ffmpeg          # macOS
sudo apt install ffmpeg      # Ubuntu/Debian

# Set environment variables
export IG_USERNAME="your_username"
export IG_PASSWORD="your_password"

# Run the pipeline
python scripts/download.py
python scripts/process.py
python scripts/publish.py
```

---

## Skills Demonstrated

- **Automation Engineering:** End-to-end pipeline design, event-driven CI/CD triggers
- **Video Processing:** FFmpeg CLI, codec transcoding, filter graphs, aspect ratio management
- **API Integration:** Instagrapi (Instagram private API), session management, media upload
- **DevOps:** GitHub Actions YAML workflows, encrypted secrets, artifact caching
- **Python:** Subprocess management, async I/O, error handling for unstable network operations

---

## ⚠️ Disclaimer

> This project uses an **unofficial Instagram API client**. Use responsibly and in compliance with [Instagram’s Terms of Service](https://help.instagram.com/581066165581870). Excessive automated activity may result in account restrictions.

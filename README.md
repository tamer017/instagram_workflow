# Instagram Content Workflow — AI-Powered CI/CD Pipeline

> **Serverless CI/CD pipeline combining FFmpeg video processing, Instagram Graph API publishing, and GPT-4 content generation — fully automated via GitHub Actions.**

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![LangChain](https://img.shields.io/badge/LangChain-latest-green.svg)](https://langchain.com/)
[![GitHub Actions](https://img.shields.io/badge/CI%2FCD-GitHub_Actions-black.svg)](https://github.com/features/actions)
[![FFmpeg](https://img.shields.io/badge/Video-FFmpeg-red.svg)](https://ffmpeg.org/)

---

## Overview

This project automates the entire Instagram Reels publishing workflow — from raw video to published post with AI-generated captions — without any manual intervention. The pipeline runs entirely on GitHub Actions (serverless), triggered on schedule or by push.

---

## Pipeline Architecture

```
Trigger (Schedule / Push)
          │
    GitHub Actions
          │
┌─────────┼─────────┐
│         │         │
Video   LLM       Secrets
Process Content    Vault
(FFmpeg) Gen (GPT) (GitHub)
│         │         │
└─────────┼─────────┘
          │
Instagram Graph API
(Reels Publish)
```

---

## Features

### Video Processing (FFmpeg)
- **H.264 encoding** optimized for Instagram Reels
- **9:16 aspect ratio** enforcement with intelligent cropping
- **EBU R128 audio normalization** — consistent loudness across all posts
- **Watermark overlay** — logo/text overlay compositing
- Automated thumbnail extraction at specified timestamp

### LLM Content Generation (LangChain + GPT-4)
- **Tone-controlled caption generation** — configurable voice (professional, casual, inspirational)
- **Hashtag strategy** — mixes high-reach + niche tags for optimal discoverability
- **Image prompt generation** for thumbnail creation
- Multi-language support via system prompt configuration

### CI/CD Infrastructure (GitHub Actions)
- Runs on schedule (cron) or manual trigger
- All credentials managed via **encrypted GitHub Secrets** (never hardcoded)
- Automatic retry on transient API failures
- Posting log artifact saved per run

---

## Configuration

```yaml
# config.yaml
video:
  resolution: "1080x1920"   # 9:16 vertical
  codec: "libx264"
  audio_normalize: true
  watermark: "assets/logo.png"

content:
  tone: "professional"      # professional | casual | inspirational
  hashtag_count: 30
  language: "en"

scheduling:
  post_time: "18:00"        # Local timezone
  days: ["mon", "wed", "fri"]
```

---

## GitHub Secrets Required

| Secret | Description |
|---|---|
| `INSTAGRAM_ACCESS_TOKEN` | Long-lived Instagram Graph API token |
| `INSTAGRAM_BUSINESS_ID` | Instagram Business Account ID |
| `OPENAI_API_KEY` | OpenAI API key for GPT-4 |
| `VIDEO_SOURCE_URL` | URL or path of source video |

---

## Installation

```bash
git clone https://github.com/tamer017/instagram_workflow.git
cd instagram_workflow
pip install -r requirements.txt

# Install FFmpeg
brew install ffmpeg  # macOS
apt install ffmpeg   # Ubuntu
```

---

## Skills & Concepts

`AI Agents` `LangChain` `OpenAI GPT-4` `GitHub Actions` `CI/CD` `FFmpeg` `Instagram Graph API` `Content Automation` `Serverless Pipelines` `Video Processing` `Social Media Automation`

---

## Author

**Ahmed Tamer Assy** — [GitHub](https://github.com/tamer017) | Machine Learning Researcher @ Volkswagen AG

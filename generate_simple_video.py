# List of Quranic fonts with Tajweed support
FONT_SOURCES = [
    {
        "name": "Scheherazade New",
        "url": "https://github.com/silnrsi/font-scheherazade/releases/download/v3.300/ScheherazadeNew-3.300.zip",
        "filename": "ScheherazadeNew-Regular.ttf",
        "priority": True,
        "is_zip": True,
        "zip_path": "ScheherazadeNew-3.300/ScheherazadeNew-Regular.ttf"
    },
    {
        "name": "Amiri Quran",
        "url": "https://github.com/aliftype/amiri/releases/download/0.113/Amiri-0.113.zip",
        "filename": "AmiriQuran-Regular.ttf",
        "priority": True,
        "is_zip": True,
        "zip_path": "Amiri-0.113/AmiriQuran-Regular.ttf"
    },
    {
        "name": "Noto Naskh Arabic",
        "url": "https://github.com/notofonts/notofonts.github.io/raw/main/fonts/NotoNaskhArabic/full/ttf/NotoNaskhArabic-Regular.ttf",
        "filename": "NotoNaskhArabic-Regular.ttf",
        "priority": True
    },
    {
        "name": "Lateef",
        "url": "https://github.com/silnrsi/font-lateef/releases/download/v4.000/Lateef-4.000.zip",
        "filename": "Lateef-Regular.ttf",
        "priority": True,
        "is_zip": True,
        "zip_path": "Lateef-4.000/Lateef-Regular.ttf"
    }
]
import json
import os
import sys
import requests
import argparse
from pathlib import Path
from typing import Dict, List, Optional
import subprocess
import tempfile
import arabic_reshaper
from bidi.algorithm import get_display
from PIL import Image, ImageDraw, ImageFont

QURAN_GROUPS_DIR = Path("quran_groups")
MERGED_AUDIO_DIR = Path("merged_audio_samples")
OUTPUT_VIDEO_DIR = Path("generated_videos")
TEMP_AUDIO_DIR = Path("temp_audio_downloads")
APPROVED_VIDEOS_FILE = Path("approved_videos.json")
SURAH_NAMES_FILE = Path("surah_names.json")
RECITER_NAMES_FILE = Path("reciter_names.json")

# Video settings (Instagram Reels optimal)
VIDEO_WIDTH = 1080
VIDEO_HEIGHT = 1920
VIDEO_FPS = 30

# Audio settings (higher quality for better output)
AUDIO_BITRATE = "256k"

# Text overlay data (Arabic - displays in center)
ARABIC_TEXT = []

# Text overlay data (English - displays at bottom)
ENGLISH_TEXT = []

# Create directories
for directory in [MERGED_AUDIO_DIR, OUTPUT_VIDEO_DIR, TEMP_AUDIO_DIR]:
    directory.mkdir(parents=True, exist_ok=True)


def find_ffmpeg() -> Optional[str]:
    """Find FFmpeg executable."""
    for path in ["ffmpeg", "ffmpeg-master-latest-win64-gpl/bin/ffmpeg.exe", "ffmpeg/ffmpeg.exe", r"C:\ffmpeg\bin\ffmpeg.exe"]:
        try:
            if subprocess.run([path, "-version"], capture_output=True, timeout=5).returncode == 0:
                return path
        except (FileNotFoundError, subprocess.TimeoutExpired):
            continue
    return None


def download_quranic_font() -> Optional[str]:
    """
    Download a proper Quranic font with all necessary Arabic glyphs.
    Prioritizes UthmanTN1 font which is specifically designed for Uthmani Quran text.
    Returns the path to the downloaded font file.
    """
    fonts_dir = Path("fonts")
    fonts_dir.mkdir(exist_ok=True)
    
    # List of Quranic fonts - UthmanTN1 is the best for Uthmani script
    FONT_SOURCES = [
        {
            "name": "Scheherazade New",
            "url": "https://github.com/silnrsi/font-scheherazade/releases/download/v3.300/ScheherazadeNew-3.300.zip",
            "filename": "ScheherazadeNew-Regular.ttf",
            "priority": True,
            "is_zip": True,
            "zip_path": "ScheherazadeNew-3.300/ScheherazadeNew-Regular.ttf"
        },
        {
            "name": "Amiri Quran",
            "url": "https://github.com/aliftype/amiri/releases/download/0.113/Amiri-0.113.zip",
            "filename": "AmiriQuran-Regular.ttf",
            "priority": True,
            "is_zip": True,
            "zip_path": "Amiri-0.113/AmiriQuran-Regular.ttf"
        },
        {
            "name": "Noto Naskh Arabic",
            "url": "https://github.com/notofonts/notofonts.github.io/raw/main/fonts/NotoNaskhArabic/full/ttf/NotoNaskhArabic-Regular.ttf",
            "filename": "NotoNaskhArabic-Regular.ttf",
            "priority": True
        },
        {
            "name": "Lateef",
            "url": "https://github.com/silnrsi/font-lateef/releases/download/v4.000/Lateef-4.000.zip",
            "filename": "Lateef-Regular.ttf",
            "priority": True,
            "is_zip": True,
            "zip_path": "Lateef-4.000/Lateef-Regular.ttf"
        }
    ]
    
    # Check if priority Quranic fonts already exist
    for font in FONT_SOURCES:
        if font.get("priority", False):
            font_path = fonts_dir / font["filename"]
            if font_path.exists() and font_path.stat().st_size > 10000:  # At least 10KB
                print(f"✓ Using existing Quranic font: {font_path}")
                return str(font_path)
    
    # Check if inferior fonts exist and warn
    inferior_fonts = ["Amiri-Regular.ttf", "Arial.ttf", "DejaVuSans.ttf"]
    for inferior_font in inferior_fonts:
        font_path = fonts_dir / inferior_font
        if font_path.exists():
            print(f"⚠️  Found {inferior_font} but it doesn't fully support Uthmani Quranic text!")
            print(f"⚠️  Downloading proper Quranic font instead...")
            break
    
    # Try downloading fonts in order of preference
    for font in FONT_SOURCES:
        font_path = fonts_dir / font["filename"]
        print(f"📥 Downloading {font['name']} font...")
        
        try:
            response = requests.get(font["url"], timeout=30)
            response.raise_for_status()
            
            # Handle zip files if needed
            if font.get("is_zip", False):
                import zipfile
                import io
                
                # Extract the specific font file from zip
                with zipfile.ZipFile(io.BytesIO(response.content)) as z:
                    zip_path = font.get("zip_path", font["filename"])
                    with z.open(zip_path) as zf:
                        with open(font_path, 'wb') as f:
                            f.write(zf.read())
            else:
                # Save the font file directly
                with open(font_path, 'wb') as f:
                    f.write(response.content)
            
            # Verify the file was downloaded and has content
            if font_path.exists() and font_path.stat().st_size > 10000:
                print(f"✓ Successfully downloaded: {font['name']} ({format_size(font_path.stat().st_size)})")
                print(f"✓ Font saved to: {font_path}")
                return str(font_path)
            else:
                print(f"⚠️  Downloaded file is too small or empty")
                if font_path.exists():
                    font_path.unlink()
            
        except requests.exceptions.RequestException as e:
            print(f"⚠️  Could not download {font['name']}: {e}")
            continue
        except Exception as e:
            print(f"⚠️  Error downloading {font['name']}: {e}")
            continue
    
    # If all downloads fail, check for any .otf or .ttf files in fonts directory
    print("\n⚠️  All font downloads failed. Checking for local fonts...")
    for ext in ['*.otf', '*.ttf']:
        local_fonts = list(fonts_dir.glob(ext))
        if local_fonts:
            font_path = local_fonts[0]
            print(f"✓ Using local font: {font_path}")
            return str(font_path)
    
    raise FileNotFoundError(
        "\n❌ No Quranic font available!\n"
        "Please manually download a font:\n"
        "1. Download Scheherazade New from: https://github.com/silnrsi/font-scheherazade/releases\n"
        "2. Or download Amiri Quran from: https://github.com/aliftype/amiri/releases\n"
        "3. Save the .ttf file to the 'fonts/' directory\n"
        "4. Run the script again\n"
    )


def get_available_font():
    """Return the path of the first available Quranic font in priority order."""
    
    # Define preferred font order - Tajweed fonts first for color-coded recitation
    FONT_CANDIDATES = [
        ("KFGQPC Hafs Uthmanic Script (Tajweed)", "UthmanicHafs_v20.otf"),
        ("Scheherazade New", "ScheherazadeNew-Regular.ttf"),
        ("Amiri Quran", "AmiriQuran-Regular.ttf"),
        ("Noto Naskh Arabic", "NotoNaskhArabic-Regular.ttf"),
        ("Lateef", "Lateef-Regular.ttf"),
    ]
    
    fonts_dir = Path("fonts")
    
    print("🔍 Looking for Quranic fonts...")
    
    # Check for available fonts in priority order
    for font_name, filename in FONT_CANDIDATES:
        font_path = fonts_dir / filename
        if font_path.exists() and font_path.stat().st_size > 10000:
            print(f"✓ Using font: {font_path} ({font_name})")
            return str(font_path)
    
    # If no fonts found, try to download
    print("⚠️  No Quranic fonts found locally. Attempting to download...")
    try:
        font_path = download_quranic_font()
        if font_path:
            return font_path.replace("\\", "/")
    except FileNotFoundError as e:
        print(str(e))
        print("\n⚠️  Falling back to system fonts (may not display Arabic correctly)...")
    except Exception as e:
        print(f"⚠️  Error loading Quranic font: {e}")
        print("⚠️  Falling back to system fonts...")
    
    # Fall back to system fonts as last resort
    import platform
    system = platform.system()
    if system == "Windows":
        possible_fonts = [
            "C:/Windows/Fonts/tahoma.ttf",
            "C:/Windows/Fonts/arial.ttf",
        ]
    elif system == "Linux":
        # Linux system Arabic fonts
        possible_fonts = [
            "/usr/share/fonts/truetype/noto/NotoNaskhArabic-Regular.ttf",
            "/usr/share/fonts/truetype/noto/NotoSansArabic-Regular.ttf",
            # Scheherazade from fonts-sil-scheherazade package
            "/usr/share/fonts/truetype/Scheherazade/Scheherazade-Regular.ttf",
            "/usr/share/fonts/opentype/Scheherazade/Scheherazade-Regular.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
            "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
        ]
    else:  # macOS
        possible_fonts = [
            "/System/Library/Fonts/Supplemental/Arial Unicode.ttf",
            "/Library/Fonts/Arial Unicode.ttf",
            "/Library/Fonts/Arial.ttf",
        ]
    
    for font in possible_fonts:
        if Path(font).exists():
            print(f"✓ Using system font: {font}")
            return font
    
    # Last resort
    print("⚠️  No fonts found! Text may not display correctly.")
    return "arial.ttf"


def get_font_path() -> str:
    """Get the appropriate font path (wrapper for backward compatibility)."""
    return get_available_font()


def shape_arabic_text(text: str) -> str:
    """
    Properly shape Arabic text for display (handles ligatures, diacritics).
    
    Args:
        text: Raw Arabic text
    
    Returns:
        Shaped Arabic text ready for display in FFmpeg (reversed for RTL)
    """
    try:
        # FFmpeg with FreeType and HarfBuzz can handle Arabic shaping automatically
        # BUT it doesn't reverse the text for RTL, so we just reverse it
        # The font will handle the proper letter forms (initial, medial, final, isolated)
        
        # Simple reversal for RTL display
        # The Amiri font has the glyphs for proper contextual forms
        return text[::-1]
        
        # NOTE: arabic_reshaper produces presentation forms (U+FExx) which many fonts don't support
        # Better to let the font's OpenType features handle shaping
        
    except Exception as e:
        print(f"Warning: Could not reverse Arabic text: {e}")
        return text


def render_arabic_text_image(
    text: str,
    font_path: str,
    font_size: int = 60,
    color: tuple = (255, 255, 255, 255),
    max_width: int = 1000,
    add_shadow: bool = True,
    border_width: int = 2
) -> Optional[Path]:
    """
    Render Arabic text as a PNG image using PIL with proper Uthmani script support.
    This bypasses FFmpeg's drawtext issues with Arabic and supports full tashkeel.
    
    Args:
        text: Arabic text to render (Uthmani script with tashkeel)
        font_path: Path to font file (preferably UthmanTN1)
        font_size: Font size in pixels
        color: RGBA color tuple
        max_width: Maximum width for text wrapping
        add_shadow: Add shadow effect
        border_width: Border/stroke width
    
    Returns:
        Path to generated PNG image
    """
    try:
        # Use arabic_reshaper for connected letters (presentation forms)
        # Arial/Tahoma support these forms well
        reshaped = arabic_reshaper.reshape(text)
        # get_display() handles bidi algorithm to reverse for RTL
        bidi_text = get_display(reshaped)
        
        # Load font - try multiple options
        font = None
        loaded_font_path = None
        tried_fonts = []
        
        # List of fonts to try in order
        # Arial has best connected letters with presentation forms
        font_candidates = [
            "C:/Windows/Fonts/arial.ttf",   # Best for connected letters
            "C:/Windows/Fonts/tahoma.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",  # Linux
            "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
            "fonts/AmiriQuran.ttf",
            "fonts/ScheherazadeNew-Regular.ttf",
            "fonts/NotoNaskhArabic-Regular.ttf",
            font_path,
            "fonts/Lateef-Regular.ttf",
            "fonts/UthmanicHafs_v20.otf",
            "/usr/share/fonts/truetype/Scheherazade/Scheherazade-Regular.ttf",
            "/usr/share/fonts/opentype/Scheherazade/Scheherazade-Regular.ttf",
            "/usr/share/fonts/truetype/noto/NotoNaskhArabic-Regular.ttf",
            "/usr/share/fonts/truetype/noto/NotoSansArabic-Regular.ttf",
        ]
        
        for font_candidate in font_candidates:
            if font_candidate in tried_fonts:
                continue
            tried_fonts.append(font_candidate)
            
            try:
                if Path(font_candidate).exists():
                    font = ImageFont.truetype(font_candidate, font_size)
                    loaded_font_path = font_candidate
                    print(f"✓ Loaded font for rendering: {Path(font_candidate).name}")
                    break
            except Exception as e:
                print(f"  ⚠️  Could not load {Path(font_candidate).name}: {e}")
                continue
        
        if font is None:
            print("⚠️  All font loading attempts failed, using PIL default font")
            font = ImageFont.load_default()
            loaded_font_path = None
        
        # Create a temporary image to measure text size
        temp_img = Image.new('RGBA', (1, 1), (0, 0, 0, 0))
        draw = ImageDraw.Draw(temp_img)
        
        # Check if text needs to be split into multiple lines
        bbox = draw.textbbox((0, 0), bidi_text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        lines = [bidi_text]
        
        # If text is too wide, split into multiple lines
        if text_width > max_width and loaded_font_path:
            # Split text by words (spaces)
            words = bidi_text.split()
            lines = []
            current_line = []
            
            for word in words:
                test_line = ' '.join(current_line + [word])
                test_bbox = draw.textbbox((0, 0), test_line, font=font)
                test_width = test_bbox[2] - test_bbox[0]
                
                if test_width <= max_width:
                    current_line.append(word)
                else:
                    if current_line:
                        lines.append(' '.join(current_line))
                        current_line = [word]
                    else:
                        # Single word is too long, add it anyway
                        lines.append(word)
            
            if current_line:
                lines.append(' '.join(current_line))
            
            print(f"  📝 Split text into {len(lines)} lines to fit width {max_width}px")
        
        # Calculate total dimensions
        line_heights = []
        max_line_width = 0
        
        for line in lines:
            bbox = draw.textbbox((0, 0), line, font=font)
            line_width = bbox[2] - bbox[0]
            line_height = bbox[3] - bbox[1]
            line_heights.append(line_height)
            max_line_width = max(max_line_width, line_width)
        
        # Add padding for border, shadow, and tashkeel marks
        padding = max(30, border_width * 4)  # Extra padding for tashkeel
        line_spacing = 10  # Space between lines
        
        total_height = sum(line_heights) + line_spacing * max(0, len(lines) - 1)
        img_width = min(max_line_width + padding * 2, max_width + padding * 2)
        img_height = total_height + padding * 2
        
        # Create final image with transparent background
        img = Image.new('RGBA', (img_width, img_height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        # Create final image with transparent background
        img = Image.new('RGBA', (img_width, img_height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        # Draw each line
        current_y = padding
        
        for i, line in enumerate(lines):
            # Get line dimensions
            bbox = draw.textbbox((0, 0), line, font=font)
            line_width = bbox[2] - bbox[0]
            line_height = line_heights[i]
            
            # Center line horizontally
            x = (img_width - line_width) // 2
            y = current_y
            
            # Draw shadow if requested
            if add_shadow:
                shadow_offset = 3
                shadow_color = (0, 0, 0, 200)
                try:
                    draw.text((x + shadow_offset, y + shadow_offset), line, font=font, fill=shadow_color)
                except OSError as e:
                    if "Bitmap missing for glyph" in str(e):
                        print(f"⚠️  Shadow rendering failed (missing glyphs): {line[:30]}...")
                    else:
                        raise
            
            # Draw border/stroke for better readability
            if border_width > 0:
                border_color = (0, 0, 0, 255)
                for adj_x in range(-border_width, border_width + 1):
                    for adj_y in range(-border_width, border_width + 1):
                        if adj_x != 0 or adj_y != 0:
                            try:
                                draw.text((x + adj_x, y + adj_y), line, font=font, fill=border_color)
                            except OSError as e:
                                if "Bitmap missing for glyph" in str(e):
                                    print(f"⚠️  Border rendering failed (missing glyphs): {line[:30]}...")
                                    break
                                else:
                                    raise
            
            # Draw main text
            try:
                draw.text((x, y), line, font=font, fill=color)
            except OSError as e:
                if "Bitmap missing for glyph" in str(e):
                    print(f"⚠️  Text rendering failed (missing glyphs): {line[:30]}...")
                    print(f"⚠️  Font {Path(font_path).name} doesn't support all required characters.")
                    print(f"⚠️  Please ensure you're using UthmanTN1 or another Quranic font.")
                    return None
                else:
                    raise
            
            # Move to next line
            current_y += line_height + line_spacing
        
        # Save to temporary file
        temp_dir = Path("temp_text_overlays")
        temp_dir.mkdir(exist_ok=True)
        
        import hashlib
        text_hash = hashlib.md5(text.encode()).hexdigest()[:8]
        output_path = temp_dir / f"arabic_{text_hash}.png"
        
        img.save(output_path, 'PNG')
        
        return output_path
        
    except Exception as e:
        print(f"❌ Error rendering Arabic text image: {e}")
        import traceback
        traceback.print_exc()
        return None


def cleanup_temp_text_overlays():
    """Clean up temporary text overlay images."""
    temp_dir = Path("temp_text_overlays")
    if temp_dir.exists():
        for png_file in temp_dir.glob("*.png"):
            try:
                png_file.unlink()
            except:
                pass


def load_json_file(file_path: Path) -> Dict:
    """Load JSON file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading {file_path}: {e}")
        return {}


def load_surah_names() -> Dict:
    """Load surah names from JSON file."""
    data = load_json_file(SURAH_NAMES_FILE)
    return data.get('surahs', {})


def load_reciter_names() -> Dict:
    """Load reciter names from JSON file."""
    data = load_json_file(RECITER_NAMES_FILE)
    return data.get('reciters', {})


def wrap_text(text: str, max_chars_per_line: int = 35) -> str:
    """
    Wrap text into multiple lines to prevent overflow.
    Uses newline character to force line breaks.
    
    Args:
        text: The text to wrap
        max_chars_per_line: Maximum characters per line (default 35 for Arabic, ~25-30 for English)
    
    Returns:
        Text with newline characters inserted
    """
    words = text.split()
    lines = []
    current_line = []
    current_length = 0
    
    for word in words:
        word_length = len(word)
        # Check if adding this word would exceed the limit
        if current_length + word_length + len(current_line) > max_chars_per_line and current_line:
            # Save current line and start new one
            lines.append(' '.join(current_line))
            current_line = [word]
            current_length = word_length
        else:
            current_line.append(word)
            current_length += word_length
    
    # Add the last line
    if current_line:
        lines.append(' '.join(current_line))
    
    # Join with actual newline character (not escaped)
    return ' '.join(lines)


def get_surah_info(surah_number: int) -> Dict[str, str]:
    """Get surah information."""
    surah_data = load_surah_names().get(str(surah_number), {})
    return {
        'arabic': surah_data.get('arabic', f'سورة {surah_number}'),
        'english': surah_data.get('english', f'Surah {surah_number}')
    }


def get_reciter_names(reciter_name: str) -> Dict[str, str]:
    """Get reciter names in both languages."""
    normalized = reciter_name.lower().strip().replace('_', ' ')
    reciter_data = load_reciter_names().get(normalized, {})
    return {
        'arabic': reciter_data.get('arabic', reciter_name),
        'english': reciter_data.get('english', reciter_name.title())
    }


def format_size(size_bytes: int) -> str:
    """Format file size in human-readable format."""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.1f}{unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.1f}TB"


def download_audio_file(url: str, output_path: Path) -> bool:
    """Download audio file from URL."""
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        output_path.write_bytes(response.content)
        return True
    except Exception as e:
        print(f"  Error downloading: {e}")
        return False


def process_ayah_audio(ayah: Dict, index: int, total: int) -> Optional[Path]:
    """Process single ayah audio."""
    print(f"  [{index+1}/{total}] Ayah {ayah.get('ayah_number', index+1)}")
    
    audio_url = ayah.get('audio_url')
    if not audio_url:
        print("  Warning: No audio URL")
        return None
    
    temp_audio_path = TEMP_AUDIO_DIR / f"ayah_{index+1:03d}.mp3"
    print(f"  Downloading: {Path(audio_url).name}")
    
    if download_audio_file(audio_url, temp_audio_path):
        print(f"  Completed: {temp_audio_path.name}")
        return temp_audio_path
    return None


def merge_audio_files(audio_files: List[Path], output_path: Path, ffmpeg_path: str) -> bool:
    """Merge multiple audio files into one."""
    if not audio_files:
        print("No audio files to merge")
        return False
    
    print(f"Merging {len(audio_files)} audio files...")
    
    # Create concat file for FFmpeg
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False, encoding='utf-8') as f:
        concat_file = f.name
        for audio_file in audio_files:
            f.write(f"file '{str(audio_file.absolute()).replace(chr(92), '/')}'\n")
    
    try:
        cmd = [ffmpeg_path, '-f', 'concat', '-safe', '0', '-i', concat_file, '-c', 'copy', '-y', str(output_path)]
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode != 0:
            print(f"FFmpeg error: {result.stderr}")
            return False
        
        if output_path.exists() and output_path.stat().st_size > 0:
            print(f"Merged audio: {format_size(output_path.stat().st_size)}")
            return True
        else:
            print("Merged audio file is empty or missing")
            return False
    finally:
        try:
            os.unlink(concat_file)
        except:
            pass
    
    return False


def get_random_background_video() -> Optional[Dict]:
    """Get random approved background video."""
    try:
        data = load_json_file(APPROVED_VIDEOS_FILE)
        videos = data.get('approved_videos', data.get('videos', []))
        if not videos:
            print("No approved videos found")
            return None
        
        print(f"Loaded {len(videos)} approved background videos")
        
        import random
        video = random.choice(videos)
        if 'video_url' not in video and 'url' in video:
            video['video_url'] = video['url']
        return video
    except Exception as e:
        print(f"Error loading approved videos: {e}")
        return None


def download_background_video(video_info: Dict) -> Optional[Path]:
    """Download background video."""
    video_url = video_info.get('video_url')
    if not video_url:
        print("No video URL found")
        return None
    
    video_filename = f"bg_{video_info.get('id', 'video')}.mp4"
    output_path = TEMP_AUDIO_DIR / video_filename
    
    if output_path.exists():
        print(f"  Using cached background: {format_size(output_path.stat().st_size)}")
        return output_path
    
    print("  Downloading background video...")
    try:
        response = requests.get(video_url, timeout=60, stream=True)
        response.raise_for_status()
        
        with open(output_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        print(f"  Downloaded: {format_size(output_path.stat().st_size)}")
        return output_path
    except Exception as e:
        print(f"  Error downloading video: {e}")
        return None

def convert_number_to_arabic(num: int) -> str:
    """Convert Western numerals to Arabic-Indic numerals."""
    arabic_digits = {'0': '٠', '1': '١', '2': '٢', '3': '٣', '4': '٤',
                    '5': '٥', '6': '٦', '7': '٧', '8': '٨', '9': '٩'}
    return ''.join(arabic_digits.get(digit, digit) for digit in str(num))

def create_simple_video(
    group_data: Dict,
    audio_path: Path,
    output_path: Path,
    ffmpeg_path: str,
    text_data: Optional[List[tuple]] = None,
    english_text_data: Optional[List[tuple]] = None
) -> bool:
    """
    Create video with background, audio, and text overlays.
    
    Args:
        group_data: Group metadata
        audio_path: Path to merged audio
        output_path: Output video path
        ffmpeg_path: FFmpeg executable path
        text_data: Optional list of (text, duration) tuples to display in center (Arabic)
        english_text_data: Optional list of (text, duration) tuples to display at bottom (English)
    """
    print(f"\n{'='*70}")
    print("CREATING VIDEO WITH TEXT OVERLAY")
    print(f"{'='*70}")
    
    audio_duration = group_data.get('duration_ms', 0) / 1000.0
    print(f"Audio duration: {audio_duration:.1f}s")
    
    video_info = get_random_background_video()
    if not video_info:
        print("⚠️  No background videos available, using solid color background")
        bg_video_path = None
    else:
        print(f"Selected background: {video_info.get('tags', 'video')[:50]}")
        bg_video_path = download_background_video(video_info)
        if not bg_video_path:
            print("⚠️  Background download failed, using solid color background")
            bg_video_path = None
    
    # Get metadata
    surah_info = get_surah_info(group_data.get('surah', 1))
    reciter_names = get_reciter_names(group_data.get('reciter_name', ''))
    ayah_start = group_data.get('ayah_start', 1)
    ayah_end = group_data.get('ayah_end', 1)
    
    # Convert numbers to Arabic numerals
    arabic_digits = '٠١٢٣٤٥٦٧٨٩'
    to_arabic_numerals = lambda num: ''.join(arabic_digits[int(d)] if d.isdigit() else d for d in str(num))
    
    # Prepare text overlays
    surah_arabic = surah_info['arabic']
    ayah_numbers_ar = to_arabic_numerals(ayah_start) if ayah_start == ayah_end else f"{to_arabic_numerals(ayah_start)}-{to_arabic_numerals(ayah_end)}"
    top_arabic = f"{surah_arabic} {ayah_numbers_ar}"
    reciter_arabic = reciter_names['arabic']
    
    surah_english = surah_info['english']
    english_info = f"{surah_english} | Verse {ayah_start}" if ayah_start == ayah_end else f"{surah_english} | Verses {ayah_start}-{ayah_end}"
    reciter_english = reciter_names['english']
    
    print(f"\nText overlay:")
    print(f"  Top: {top_arabic}")
    print(f"  Top 2: {reciter_arabic}")
    print(f"  Bottom: {english_info}")
    print(f"  Bottom 2: {reciter_english}")
    
    if text_data:
        print(f"  Center text items: {len(text_data)}")
    
    if english_text_data:
        print(f"  Bottom English text items: {len(english_text_data)}")

    print(f"\nBuilding video with FFmpeg...")
    print("Rendering Arabic text as images using PIL...")
    
    # Get appropriate font path for the platform
    font_path = get_font_path()
    print(f"Using font: {font_path}")
    
    # Render Arabic text as images using PIL
    top_arabic_img = render_arabic_text_image(top_arabic, font_path, font_size=50, color=(255, 215, 0, 255))  # Gold color
    reciter_arabic_img = render_arabic_text_image(reciter_arabic, font_path, font_size=40, color=(255, 255, 255, 230))
    
    if not top_arabic_img or not reciter_arabic_img:
        print("⚠️  Failed to render Arabic text images, falling back to simple rendering")
        cleanup_temp_text_overlays()
        return False
    
    print(f"  ✅ Arabic text images rendered")
    
    # Escape text for FFmpeg (for English text only)
    def escape_text(text):
        escaped = text.replace(":", r"\:").replace("'", r"\'").replace(",", r"\,")
        escaped = escaped.replace("\n", r"\n")
        return escaped
    
    english_info_esc = escape_text(english_info)
    reciter_english_esc = escape_text(reciter_english)
    
    # Collect all inputs for FFmpeg
    if bg_video_path:
        # Use background video
        ffmpeg_inputs = [
            ('-stream_loop', '-1', '-i', str(bg_video_path)),  # [0:v] - background video (looped)
            ('-i', str(audio_path)),  # [1:a] - audio
            ('-i', str(top_arabic_img)),  # [2:v] - top Arabic text image
            ('-i', str(reciter_arabic_img)),  # [3:v] - reciter Arabic text image
        ]
        
        # Create filter complex with proper scaling and image overlays
        aspect_ratio = 9/16
        filter_parts = [
            # Scale video to COVER the entire frame (9:16) so there are NO black bars
            f"[0:v]scale='if(gt(a,{aspect_ratio}),-2,{VIDEO_WIDTH})':'if(gt(a,{aspect_ratio}),{VIDEO_HEIGHT},-2)'[scaled]",
            # Center-crop to exact 1080x1920
            f"[scaled]crop={VIDEO_WIDTH}:{VIDEO_HEIGHT}:(iw-{VIDEO_WIDTH})/2:(ih-{VIDEO_HEIGHT})/2[cropped]",
            # Enhance brightness and contrast
            f"[cropped]eq=brightness=0.05:contrast=1.15:saturation=1.1[adjusted]",
            # Overlay top Arabic text image (centered horizontally, y=220)
            f"[adjusted][2:v]overlay=(W-w)/2:220[t1]",
            # Overlay reciter Arabic text image (centered horizontally, y=280)
            f"[t1][3:v]overlay=(W-w)/2:280[t2]",
        ]
    else:
        # Create simple solid color background
        ffmpeg_inputs = [
            ('-i', str(audio_path)),  # [0:a] - audio
            ('-i', str(top_arabic_img)),  # [1:v] - top Arabic text image
            ('-i', str(reciter_arabic_img)),  # [2:v] - reciter Arabic text image
        ]
        
        # Create solid color background and overlay text
        filter_parts = [
            # Create solid dark background
            f"color=c=#0d1b2a:s={VIDEO_WIDTH}x{VIDEO_HEIGHT}:d={audio_duration}[bg]",
            # Overlay top Arabic text image (centered horizontally, y=220)
            f"[bg][1:v]overlay=(W-w)/2:220[t1]",
            # Overlay reciter Arabic text image (centered horizontally, y=280)
            f"[t1][2:v]overlay=(W-w)/2:280[t2]",
        ]
    
    # Add center text with timing if provided (Arabic - render as images)
    current_filter = "t2"
    center_text_images = []
    # Input index depends on whether we have background video or not
    input_index = 4 if bg_video_path else 3  # Next available input index
    
    if text_data:
        print(f"  Rendering {len(text_data)} center text images...")
        current_time = 0
        rendered_count = 0
        for i, (text, duration) in enumerate(text_data):
            start_time = float(f"{current_time:.2f}")
            end_time = float(f"{current_time + duration:.2f}")
            
            # Render Arabic text as image
            wrapped_text = wrap_text(text, max_chars_per_line=20)
            text_img = render_arabic_text_image(wrapped_text, font_path, font_size=60, color=(255, 255, 255, 255))
            
            if text_img:
                center_text_images.append((text_img, start_time, end_time))
                # Add input for this image
                ffmpeg_inputs.append(('-i', str(text_img)))
                # Add overlay filter with timing
                next_filter = f"c{i+1}" if i < len(text_data) - 1 else "t3"
                filter_parts.append(
                    f"[{current_filter}][{input_index}:v]overlay=(W-w)/2:(H-h)/2:enable='between(t,{start_time},{end_time})'[{next_filter}]"
                )
                current_filter = next_filter
                input_index += 1
                rendered_count += 1
            else:
                print(f"  ⚠️  Skipped text segment {i+1} due to rendering error")
            
            current_time = end_time
        print(f"  ✅ Rendered {rendered_count} center text images")
    else:
        filter_parts.append(f"[{current_filter}]null[t3]")
        current_filter = "t3"
    
    # Add bottom static text (English - use drawtext since it works fine for English)
    # Escape font path for FFmpeg
    font_path_esc = font_path.replace(":", r"\:").replace("\\", "/")
    
    filter_parts.append(
        f"[{current_filter}]drawtext=fontfile='{font_path_esc}':text='{english_info_esc}':"
        f"fontsize=45:fontcolor=gold:bordercolor=black:borderw=2:x=(w-text_w)/2:y=h-280[t4]"
    )
    
    filter_parts.append(
        f"[t4]drawtext=fontfile='{font_path_esc}':text='{reciter_english_esc}':"
        f"fontsize=38:fontcolor=white@0.9:bordercolor=black:borderw=2:x=(w-text_w)/2:y=h-220[t5]"
    )
    
    # Add bottom English text with timing if provided (higher position)
    current_filter = "t5"
    if english_text_data:
        current_time = 0
        for i, (text, duration) in enumerate(english_text_data):
            start_time = float(f"{current_time:.2f}")
            end_time = float(f"{current_time + duration:.2f}")
            # Wrap text to prevent overflow (18 chars per line for 48px English font to ensure no overflow)
            wrapped_text = wrap_text(text, max_chars_per_line=18)
            text_esc = escape_text(wrapped_text)
            next_filter = f"be{i+1}" if i < len(english_text_data) - 1 else "output"
            
            # English text positioned higher (y=h-350) with larger font 
            filter_parts.append(
                f"[{current_filter}]drawtext=fontfile='{font_path_esc}':text='{text_esc}':fontsize=32:fontcolor=white:bordercolor=black:borderw=2:"
                f"x=(w-text_w)/2:y=h-350:enable='between(t,{start_time},{end_time})'[{next_filter}]"
            )
            current_filter = next_filter
            current_time = end_time
    else:
        filter_parts.append(f"[{current_filter}]null[output]")
    
    filter_complex = ";".join(filter_parts)
    
    # Build FFmpeg command with all inputs
    cmd = [ffmpeg_path]
    
    # Add all inputs
    for input_args in ffmpeg_inputs:
        cmd.extend(input_args)
    
    # Add filter complex and output options
    # Audio input index depends on whether we have a background video
    audio_input_idx = '1:a' if bg_video_path else '0:a'
    cmd.extend([
        '-filter_complex', filter_complex,
        '-map', '[output]',
        '-map', audio_input_idx,
        # Video encoding with higher quality
        '-c:v', 'libx264',
        '-preset', 'slow',  # Slower preset = better quality
        '-crf', '18',  # Lower CRF = higher quality (18 is visually lossless)
        '-profile:v', 'high',  # High profile for better compression
        '-level', '4.2',  # H.264 level for HD video
        '-pix_fmt', 'yuv420p',  # Pixel format for maximum compatibility
        '-movflags', '+faststart',  # Optimize for streaming
        # Audio encoding with higher quality
        '-c:a', 'aac',
        '-b:a', AUDIO_BITRATE,
        '-ar', '48000',  # 48kHz sample rate (professional quality)
        # Ensure exact dimensions and duration
        '-s', f'{VIDEO_WIDTH}x{VIDEO_HEIGHT}',
        '-r', str(VIDEO_FPS),
        '-shortest',
        '-y', str(output_path)
    ])
    
    print("  Encoding video...")
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode != 0:
        print(f"\nFFmpeg error:\n{result.stderr}")
        cleanup_temp_files(bg_video_path)
        cleanup_temp_text_overlays()
        return False
    
    if output_path.exists() and output_path.stat().st_size > 0:
        print(f"\n{'='*70}")
        print(f"SUCCESS! Video created: {format_size(output_path.stat().st_size)}")
        print(f"{'='*70}")
        cleanup_temp_files(bg_video_path)
        cleanup_temp_text_overlays()
        return True
    else:
        print("Video file is empty or missing")
        cleanup_temp_files(bg_video_path)
        cleanup_temp_text_overlays()
        return False


def cleanup_temp_files(bg_video_path: Optional[Path] = None):
    """Clean up temporary audio and video files."""
    print("\nCleaning up temporary files...")
    
    if TEMP_AUDIO_DIR.exists():
        for temp_file in TEMP_AUDIO_DIR.glob("ayah_*.mp3"):
            try:
                temp_file.unlink()
                print(f"  Removed: {temp_file.name}")
            except Exception as e:
                print(f"  Could not remove {temp_file.name}: {e}")
    
    if bg_video_path and bg_video_path.exists():
        try:
            bg_video_path.unlink()
            print(f"  Removed: {bg_video_path.name}")
        except Exception as e:
            print(f"  Could not remove {bg_video_path.name}: {e}")
    
    print("Cleanup complete.")


def process_group(group_id: str, ffmpeg_path: str, text_data: Optional[List[tuple]] = None, english_text_data: Optional[List[tuple]] = None) -> bool:
    """Process a single group to create video.
    
    Args:
        group_id: The group identifier
        ffmpeg_path: Path to FFmpeg executable
        text_data: Optional list of (text, duration) tuples for center text display
        english_text_data: Optional list of (text, duration) tuples for bottom English text display
    """
    # Clear global text arrays at the start
    global ARABIC_TEXT, ENGLISH_TEXT
    ARABIC_TEXT.clear()
    ENGLISH_TEXT.clear()
    
    print(f"\n{'='*80}")
    print("SIMPLE QURAN VIDEO GENERATOR")
    print(f"{'='*80}")
    print(f"Group ID: {group_id}")
    print(f"{'='*80}")
    
    # Find and load group file
    reciter_num = group_id.split('_')[0].replace('reciter', '')
    group_files = list(QURAN_GROUPS_DIR.glob(f"reciter_{reciter_num}_*_groups.json"))
    
    if not group_files:
        print(f"Error: Group file not found for reciter {reciter_num}")
        return False
    
    print(f"Loading: {group_files[0].name}")
    groups_data = load_json_file(group_files[0])
    group_data = groups_data.get('groups', {}).get(group_id)
    
    if not group_data:
        print(f"Error: Group ID {group_id} not found in file")
        return False
    
    group_data['group_id'] = group_id
    group_data['reciter_name'] = groups_data.get('reciter_name', '')
    
    # Show group info
    surah_info = get_surah_info(group_data.get('surah', 1))
    reciter_names = get_reciter_names(group_data.get('reciter_name', ''))
    
    print(f"\nGroup Information:")
    print(f"  Surah: {surah_info['english']} ({surah_info['arabic']})")
    print(f"  Ayahs: {group_data.get('ayah_start')}-{group_data.get('ayah_end')}")
    print(f"  Reciter: {reciter_names['english']}")
    print(f"  Duration: {group_data.get('duration_ms', 0) / 1000:.1f}s")
    
    # Process audio
    print(f"\n{'='*70}\nAUDIO PROCESSING\n{'='*70}")
    ayahs = group_data.get('ayahs', [])
    print(f"Processing {len(ayahs)} ayahs")
    
    audio_files = [audio_path for i, ayah in enumerate(ayahs) if (audio_path := process_ayah_audio(ayah, i, len(ayahs)))]
    
    if not audio_files:
        print("Error: No audio files processed")
        return False
    
    # Merge audio
    merged_audio_path = MERGED_AUDIO_DIR / f"{group_id}_merged.mp3"
    if not merge_audio_files(audio_files, merged_audio_path, ffmpeg_path):
        return False
    
    # Populate text overlays from ayah data (if not disabled)
    def extract_arabic_text(segments, words, verse_num_arabic, lower_limit=4, upper_limit=7):
        if(len(words) == 0) or len(segments) == 0:
            return
        if len(words) < lower_limit:
            duration = ((segments[-1][-1] - segments[0][2]) / 1000.0)
            ARABIC_TEXT.append((" ".join(words) + f" ﴿{verse_num_arabic}﴾", duration))
        elif len(words) >= lower_limit and len(words) < upper_limit:
            duration1 = ((segments[len(words)//2][-1] - segments[0][2]) / 1000.0)
            duration2 = ((segments[-1][-1] - segments[len(words)//2 + 1][2]) / 1000.0) 
            ARABIC_TEXT.append((" ".join(words[:len(words)//2]), duration1))
            ARABIC_TEXT.append((" ".join(words[len(words)//2:]) + f" ﴿{verse_num_arabic}﴾", duration2))
        else:
            duration = ((segments[lower_limit-1][-1] - segments[0][2]) / 1000.0)
            ARABIC_TEXT.append((" ".join(words[:lower_limit]), duration))
            extract_arabic_text(segments[lower_limit:], words=words[lower_limit:],verse_num_arabic=verse_num_arabic)
    
    def extract_english_text(words, duration, lower_limit=10):
        groups = len(words) // lower_limit + (1 if len(words) % lower_limit != 0 else 0)
        group_duration = (duration / groups)
        for i in range(groups):
            start = i * lower_limit
            end = start + lower_limit
            ENGLISH_TEXT.append((" ".join(words[start:end]), group_duration))
    
    # Extract text from ayahs
    for ayah in group_data.get('ayahs', []):
        words = ayah.get('arabic_words', [])
        segments = ayah.get('segments',[[]])
        english_words = ayah.get('translation', "").split()

        processed_words = []   
        for segment in segments:
            processed_words.append(" ".join(words[segment[0]:segment[1]]))
        verse_number = ayah.get('ayah_number', 0)
        verse_num_arabic = convert_number_to_arabic(verse_number)
        extract_arabic_text(segments, words=processed_words, verse_num_arabic=verse_num_arabic)
        extract_english_text(english_words, ayah.get('duration_ms', 0) / 1000.0)

    print(f"Generated {len(ARABIC_TEXT)} Arabic text segments")
    print(f"Generated {len(ENGLISH_TEXT)} English text segments")
    
    # Use populated text arrays unless disabled by function parameters
    final_arabic_text = ARABIC_TEXT if text_data is None else text_data
    final_english_text = ENGLISH_TEXT if english_text_data is None else english_text_data
    
    # Create video
    print(f"\n{'='*70}\nVIDEO GENERATION\n{'='*70}")
    output_video_path = OUTPUT_VIDEO_DIR / f"{group_id}.mp4"
    
    if not create_simple_video(group_data, merged_audio_path, output_video_path, ffmpeg_path, final_arabic_text, final_english_text):
        return False
    
    print(f"\n{'='*80}\nSUCCESS!\n{'='*80}")
    print(f"Audio: {merged_audio_path}")
    print(f"Video: {output_video_path}")
    print(f"{'='*80}")
    
    return True


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description='Simple Quran Video Generator with UthmanTN1 Font Support',
        epilog="""
Examples:
  # Generate video with both Arabic and English text overlays (default)
  python generate_simple_video.py --group reciter2_s001_001-007
  
  # Generate video without Arabic text overlays
  python generate_simple_video.py --group reciter2_s001_001-007 --no-arabic-text
  
  # Generate video without English text overlays
  python generate_simple_video.py --group reciter2_s001_001-007 --no-english-text
  
  # Generate video with only static text (no custom overlays)
  python generate_simple_video.py --group reciter2_s001_001-007 --no-arabic-text --no-english-text

Note: The script will automatically download UthmanTN1 font for proper Quranic text display.
      To customize text overlays, edit ARABIC_TEXT and ENGLISH_TEXT in the script.
        """
    )
    
    parser.add_argument('--group', type=str, required=True, help='Group ID (e.g., reciter2_s001_001-007)')
    parser.add_argument('--no-arabic-text', action='store_true', help='Disable Arabic text overlays in center')
    parser.add_argument('--no-english-text', action='store_true', help='Disable English text overlays at bottom')
    
    args = parser.parse_args()
    
    ffmpeg_path = find_ffmpeg()
    if not ffmpeg_path:
        print("ERROR: FFmpeg not found!")
        print("Please install FFmpeg or add it to your PATH")
        sys.exit(1)
    
    print(f"FFmpeg found: {ffmpeg_path}\n")
    
    # Ensure fonts are available before starting
    print("Verifying Arabic fonts...")
    try:
        font_path = get_font_path()
        print(f"✓ Font ready: {font_path}\n")
    except Exception as e:
        print(f"❌ Font verification failed: {e}")
        print("Please ensure at least one Arabic font is available.")
        sys.exit(1)
    
    # Use static text overlays unless disabled
    text_data = None if args.no_arabic_text else ARABIC_TEXT
    english_text_data = None if args.no_english_text else ENGLISH_TEXT
    
    success = process_group(args.group, ffmpeg_path, text_data, english_text_data)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
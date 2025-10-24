import json
import os
import sys
import requests
import argparse
from pathlib import Path
from typing import Dict, List, Optional
import subprocess
import tempfile

QURAN_GROUPS_DIR = Path("quran_groups")
MERGED_AUDIO_DIR = Path("merged_audio_samples")
OUTPUT_VIDEO_DIR = Path("generated_videos")
TEMP_AUDIO_DIR = Path("temp_audio_downloads")
APPROVED_VIDEOS_FILE = Path("approved_videos.json")
SURAH_NAMES_FILE = Path("surah_names.json")
RECITER_NAMES_FILE = Path("reciter_names.json")

# Video settings
VIDEO_WIDTH = 1080
VIDEO_HEIGHT = 1920
VIDEO_FPS = 30

# Audio settings
AUDIO_BITRATE = "192k"

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


def get_font_path() -> str:
    """Get the appropriate font path for the current platform."""
    import platform
    system = platform.system()
    
    if system == "Windows":
        # Windows font path
        font_path = "C\\:/Windows/Fonts/arial.ttf"
    elif system == "Linux":
        # Try common Linux font paths for DejaVu Sans (good Arabic support)
        possible_fonts = [
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
            "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
            "/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf",
            "/usr/share/fonts/dejavu/DejaVuSans.ttf"
        ]
        for font in possible_fonts:
            if Path(font).exists():
                font_path = font.replace("\\", "/")
                break
        else:
            # Fallback to DejaVu Sans (should be installed by workflow)
            font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
    elif system == "Darwin":  # macOS
        font_path = "/Library/Fonts/Arial.ttf"
    else:
        # Default fallback
        font_path = "arial.ttf"
    
    return font_path


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
        return False
    
    print(f"Selected background: {video_info.get('tags', 'video')[:50]}")
    
    bg_video_path = download_background_video(video_info)
    if not bg_video_path:
        return False
    
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

    def extract_arabic_text(segments, words, verse_num_arabic, lower_limit=5, upper_limit=8):
        if(len(words) == 0) or len(segments) == 0:
            return
        if len(words) < lower_limit:
            duration = ((segments[-1][-1] - segments[0][2]) / 1000.0) + 1
            ARABIC_TEXT.append(("﴾" + " ".join(words) + f" ﴿{verse_num_arabic}", duration))
        elif len(words) >= lower_limit and len(words) < upper_limit:
            duration1 = ((segments[len(words)//2][-1] - segments[0][2]) / 1000.0) + 1
            duration2 = ((segments[-1][-1] - segments[len(words)//2 + 1][2]) / 1000.0) + 1
            ARABIC_TEXT.append((" ".join(words[:len(words)//2]), duration1))
            ARABIC_TEXT.append(("﴾" + " ".join(words[len(words)//2:]) + f" ﴿{verse_num_arabic}", duration2))
        else:
            duration = ((segments[lower_limit-1][-1] - segments[0][2]) / 1000.0) + 1.5
            ARABIC_TEXT.append((" ".join(words[:lower_limit]), duration))
            extract_arabic_text(segments[lower_limit:], words=words[lower_limit:],verse_num_arabic=verse_num_arabic)
    
    def extract_english_text(words, duration, lower_limit=10):
        groups = len(words) // lower_limit + (1 if len(words) % lower_limit != 0 else 0)
        group_duration = (duration / groups) + 0.25
        for i in range(groups):
            start = i * lower_limit
            end = start + lower_limit
            ENGLISH_TEXT.append((" ".join(words[start:end]), group_duration))


    for ayah in group_data.get('ayahs', []):
        words = ayah.get('arabic_words', [])
        segments = ayah.get('segments',[[]])
        english_words = ayah.get('translation', "").split()
        if len(words) != len(segments):
            new_words = []
            for word in words:
                if len(word.strip()) > 1:
                    new_words.append(word)
                else:
                    new_words[-1] += word
            words = new_words
            
        verse_number = ayah.get('ayah_number', 0)
        verse_num_arabic = convert_number_to_arabic(verse_number)

        extract_arabic_text(segments, words=words, verse_num_arabic=verse_num_arabic)
        extract_english_text(english_words, ayah.get('duration_ms', 0) / 1000.0)


    print(f"\nBuilding video with FFmpeg...")
    
    # Escape text for FFmpeg (preserve newlines for multi-line text)
    def escape_text(text):
        # First escape special characters, but preserve actual newlines
        escaped = text.replace(":", r"\:").replace("'", r"\'").replace(",", r"\,")
        # Replace actual newlines with FFmpeg's newline escape sequence
        escaped = escaped.replace("\n", r"\n")
        return escaped
    
    top_arabic_esc, reciter_arabic_esc = escape_text(top_arabic), escape_text(reciter_arabic)
    english_info_esc, reciter_english_esc = escape_text(english_info), escape_text(reciter_english)
    
    # Get appropriate font path for the platform
    font_path = get_font_path()
    print(f"Using font: {font_path}")
    
    # Create filter complex with text overlays
    filter_parts = [
        f"[0:v]scale={VIDEO_WIDTH}:{int(VIDEO_WIDTH * 16/9)}[scaled]",
        f"[scaled]crop={VIDEO_WIDTH}:{VIDEO_HEIGHT}[cropped]",
        f"[cropped]eq=brightness=0.0:contrast=1.1[adjusted]",
        f"[adjusted]drawtext=fontfile='{font_path}':text='{top_arabic_esc}':fontsize=50:fontcolor=gold:bordercolor=black:borderw=2:x=(w-text_w)/2:y=60[t1]",
        f"[t1]drawtext=fontfile='{font_path}':text='{reciter_arabic_esc}':fontsize=40:fontcolor=white@0.9:bordercolor=black:borderw=2:x=(w-text_w)/2:y=130[t2]",
    ]
    
    # Add center text with timing if provided (Arabic - larger font)
    current_filter = "t2"
    if text_data:
        current_time = 0
        for i, (text, duration) in enumerate(text_data):
            start_time = current_time
            end_time = current_time + duration
            # Wrap text to prevent overflow (20 chars per line for 70px Arabic font to ensure no overflow)
            wrapped_text = wrap_text(text, max_chars_per_line=20)
            text_esc = escape_text(wrapped_text)
            next_filter = f"c{i+1}" if i < len(text_data) - 1 else "t3"
            
            # Larger Arabic font (70px) with proper positioning and line breaks
            filter_parts.append(
                f"[{current_filter}]drawtext=fontfile='{font_path}':"
                f"text='{text_esc}':fontsize=60:fontcolor=white:bordercolor=black:borderw=3:"
                f"x=(w-text_w)/2:y=(h-text_h)/2:"
                f"line_spacing=10:"
                f"enable='between(t,{start_time},{end_time})'[{next_filter}]"
            )
            current_filter = next_filter
            current_time = end_time
    else:
        filter_parts.append(f"[{current_filter}]null[t3]")
        current_filter = "t3"
    
    # Add bottom static text (English info and reciter)
    filter_parts.append(
        f"[{current_filter}]drawtext=fontfile='{font_path}':text='{english_info_esc}':"
        f"fontsize=45:fontcolor=gold:bordercolor=black:borderw=2:x=(w-text_w)/2:y=h-180[t4]"
    )
    
    filter_parts.append(
        f"[t4]drawtext=fontfile='{font_path}':text='{reciter_english_esc}':"
        f"fontsize=38:fontcolor=white@0.9:bordercolor=black:borderw=2:x=(w-text_w)/2:y=h-120[t5]"
    )
    
    # Add bottom English text with timing if provided (higher position)
    current_filter = "t5"
    if english_text_data:
        current_time = 0
        for i, (text, duration) in enumerate(english_text_data):
            start_time = current_time
            end_time = current_time + duration
            # Wrap text to prevent overflow (18 chars per line for 48px English font to ensure no overflow)
            wrapped_text = wrap_text(text, max_chars_per_line=18)
            text_esc = escape_text(wrapped_text)
            next_filter = f"be{i+1}" if i < len(english_text_data) - 1 else "output"
            
            # English text positioned higher (y=h-350) with larger font and line breaks
            filter_parts.append(
                f"[{current_filter}]drawtext=fontfile='{font_path}':"
                f"text='{text_esc}':fontsize=32:fontcolor=white:bordercolor=black:borderw=2:"
                f"x=(w-text_w)/2:y=h-350:"
                f"line_spacing=8:"
                f"enable='between(t,{start_time},{end_time})'[{next_filter}]"
            )
            current_filter = next_filter
            current_time = end_time
    else:
        filter_parts.append(f"[{current_filter}]null[output]")
    
    filter_complex = ";".join(filter_parts)
    
    cmd = [
        ffmpeg_path, '-stream_loop', '-1', '-i', str(bg_video_path), '-i', str(audio_path),
        '-filter_complex', filter_complex, '-map', '[output]', '-map', '1:a',
        '-c:v', 'libx264', '-preset', 'medium', '-crf', '23',
        '-c:a', 'aac', '-b:a', AUDIO_BITRATE, '-shortest', '-y', str(output_path)
    ]
    
    print("  Encoding video...")
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode != 0:
        print(f"\nFFmpeg error:\n{result.stderr}")
        cleanup_temp_files(bg_video_path)
        return False
    
    if output_path.exists() and output_path.stat().st_size > 0:
        print(f"\n{'='*70}")
        print(f"SUCCESS! Video created: {format_size(output_path.stat().st_size)}")
        print(f"{'='*70}")
        cleanup_temp_files(bg_video_path)
        return True
    else:
        print("Video file is empty or missing")
        cleanup_temp_files(bg_video_path)
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
    
    # Create video
    print(f"\n{'='*70}\nVIDEO GENERATION\n{'='*70}")
    output_video_path = OUTPUT_VIDEO_DIR / f"{group_id}.mp4"
    
    if not create_simple_video(group_data, merged_audio_path, output_video_path, ffmpeg_path, text_data, english_text_data):
        return False
    
    print(f"\n{'='*80}\nSUCCESS!\n{'='*80}")
    print(f"Audio: {merged_audio_path}")
    print(f"Video: {output_video_path}")
    print(f"{'='*80}")
    
    return True


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description='Simple Quran Video Generator',
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

Note: To customize text overlays, edit ARABIC_TEXT and ENGLISH_TEXT in the script.
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
    
    # Use static text overlays unless disabled
    text_data = None if args.no_arabic_text else ARABIC_TEXT
    english_text_data = None if args.no_english_text else ENGLISH_TEXT
    
    success = process_group(args.group, ffmpeg_path, text_data, english_text_data)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()

# generate_video.py
"""
Generates a simple vertical (9:16) color-changing MP4 and multiple thumbnails.
Usage:
  python generate_video.py <output_dir> [duration_seconds] [fps] [num_thumbs]

Defaults:
  output_dir=outputs
  duration_seconds=6
  fps=30
  num_thumbs=3
"""
import os
import sys
from moviepy.editor import ColorClip, TextClip, CompositeVideoClip, concatenate_videoclips
import random
import time

def make_color_clip(color, w, h, duration):
    return ColorClip(size=(w,h), color=color).set_duration(duration)

def make_text_clip(text, w, fontsize=90, duration=0.5):
    txt = TextClip(text, fontsize=fontsize, color='white', size=(w-100,None), method='caption')
    txt = txt.set_position(('center','center')).set_duration(duration)
    return txt

def create_video(out_dir, duration=6, fps=30):
    w, h = 1080, 1920
    # create a few color clips and concatenate for a simple color-changing video
    segments = []
    seg_dur = max(0.5, duration / 6.0)
    for i in range(int(duration / seg_dur) + 1):
        # generate a random bright-ish color
        color = tuple(random.randint(30, 230) for _ in range(3))
        clip = make_color_clip(color, w, h, seg_dur)
        segments.append(clip)
    video = concatenate_videoclips(segments).set_duration(duration)
    # overlay a timestamp text that changes per second
    # (moviepy TextClip rendering can be slow for many frames so keep it simple)
    out_path = os.path.join(out_dir, "video.mp4")
    video.write_videofile(
        out_path,
        fps=fps,
        codec='libx264',
        audio=False,
        ffmpeg_params=['-movflags','+faststart','-pix_fmt','yuv420p'],
        verbose=False,
        logger=None
    )
    return out_path

def extract_thumbnails(video_path, out_dir, count=3):
    from moviepy.editor import VideoFileClip
    clip = VideoFileClip(video_path)
    duration = clip.duration
    thumbs = []
    for i in range(count):
        t = (i+1) * duration / (count+1)
        frame_path = os.path.join(out_dir, f"thumb_{i+1}.jpg")
        clip.save_frame(frame_path, t)
        thumbs.append(frame_path)
    clip.reader.close()
    clip.audio = None
    return thumbs

def zip_outputs(out_dir):
    import zipfile
    zip_path = os.path.join(out_dir, "video_and_thumbs.zip")
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as z:
        for fn in os.listdir(out_dir):
            if fn.endswith(('.mp4', '.jpg', '.zip')):
                z.write(os.path.join(out_dir, fn), fn)
    return zip_path

if __name__ == "__main__":
    out_dir = sys.argv[1] if len(sys.argv) >= 2 else "outputs"
    duration = float(sys.argv[2]) if len(sys.argv) >= 3 else 6.0
    fps = int(sys.argv[3]) if len(sys.argv) >= 4 else 30
    num_thumbs = int(sys.argv[4]) if len(sys.argv) >= 5 else 3

    os.makedirs(out_dir, exist_ok=True)
    print("Creating video...")
    vpath = create_video(out_dir, duration=duration, fps=fps)
    print("Video created:", vpath)
    print("Extracting thumbnails...")
    thumbs = extract_thumbnails(vpath, out_dir, count=num_thumbs)
    print("Thumbnails:", thumbs)
    print("Zipping outputs...")
    z = zip_outputs(out_dir)
    print("Zipped outputs at:", z)
    print(vpath)

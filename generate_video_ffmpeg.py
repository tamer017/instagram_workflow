# generate_video_ffmpeg.py
# Generates a short vertical MP4 and thumbnails (thumb_1.jpg used as image upload)
import os, sys, math, subprocess
from PIL import Image

def make_frame(color, size=(1080,1920)):
    return Image.new('RGB', size, color)

def color_for_frame(i, total):
    t = float(i) / max(1, total-1)
    r = int(128 + 127 * math.sin(2*math.pi*(t + 0.0)))
    g = int(128 + 127 * math.sin(2*math.pi*(t + 0.33)))
    b = int(128 + 127 * math.sin(2*math.pi*(t + 0.66)))
    return (r, g, b)

def generate_frames(out_dir, duration=2, fps=24):
    frames_dir = os.path.join(out_dir, "frames")
    os.makedirs(frames_dir, exist_ok=True)
    total_frames = int(duration * fps)
    for i in range(total_frames):
        color = color_for_frame(i, total_frames)
        img = make_frame(color)
        path = os.path.join(frames_dir, f"frame_{i:04d}.png")
        img.save(path, format='PNG')
    return frames_dir, total_frames

def build_video_with_ffmpeg(frames_dir, out_video, fps=24):
    cmd = [
        "ffmpeg", "-y",
        "-framerate", str(fps),
        "-i", os.path.join(frames_dir, "frame_%04d.png"),
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        "-movflags", "+faststart",
        out_video
    ]
    subprocess.check_call(cmd)

def extract_thumbnails(frames_dir, out_dir, count=3, total_frames=None):
    from PIL import Image
    os.makedirs(out_dir, exist_ok=True)
    if total_frames is None:
        files = sorted([f for f in os.listdir(frames_dir) if f.endswith('.png')])
        total_frames = len(files)
    thumbs = []
    for i in range(count):
        idx = int((i+1) * total_frames / (count+1))
        src = os.path.join(frames_dir, f"frame_{idx:04d}.png")
        dst = os.path.join(out_dir, f"thumb_{i+1}.jpg")
        im = Image.open(src)
        im.convert("RGB").save(dst, format='JPEG', quality=90)
        thumbs.append(dst)
    return thumbs

def zip_outputs(out_dir):
    zip_path = os.path.join(out_dir, "video_and_thumbs.zip")
    import zipfile
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as z:
        for fn in os.listdir(out_dir):
            if fn.endswith(('.mp4', '.jpg', '.zip')):
                z.write(os.path.join(out_dir, fn), fn)
    return zip_path

def main():
    out_dir = sys.argv[1] if len(sys.argv) >= 2 else "outputs"
    duration = float(sys.argv[2]) if len(sys.argv) >= 3 else 2.0
    fps = int(sys.argv[3]) if len(sys.argv) >= 4 else 24
    num_thumbs = int(sys.argv[4]) if len(sys.argv) >= 5 else 3

    os.makedirs(out_dir, exist_ok=True)
    frames_dir, total = generate_frames(out_dir, duration=duration, fps=fps)
    video_path = os.path.join(out_dir, "video.mp4")
    build_video_with_ffmpeg(frames_dir, video_path, fps=fps)
    thumbs = extract_thumbnails(frames_dir, out_dir, count=num_thumbs, total_frames=total)
    z = zip_outputs(out_dir)
    print(video_path)

if __name__ == '__main__':
    main()

import os
import subprocess

def extract_frames_with_ffmpeg(base_path, fps=1):
    for gesture in os.listdir(base_path):
        videos_dir = os.path.join(base_path, gesture, "videos")
        frames_base = os.path.join(base_path, gesture, "frames")
        if not os.path.isdir(videos_dir):
            continue

        for fname in os.listdir(videos_dir):
            if not fname.lower().endswith(".mp4"):
                continue

            video_path = os.path.join(videos_dir, fname)
            video_name = os.path.splitext(fname)[0]
            out_dir   = os.path.join(frames_base, video_name)
            os.makedirs(out_dir, exist_ok=True)

            # Build ffmpeg command:
            cmd = [
                "ffmpeg",
                "-i", video_path,
                "-vf", f"fps={fps}",
                os.path.join(out_dir, "frame_%03d.png")
            ]

            print("Running:", " ".join(cmd))
            subprocess.run(cmd, check=True)

if __name__ == "__main__":
    extract_frames_with_ffmpeg("gesture_dataset", fps=1)
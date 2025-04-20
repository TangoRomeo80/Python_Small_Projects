import os
import ffmpeg

def process_videos_with_ffmpeg(base_path,
                               resolution=(640, 640),
                               target_fps=30,
                               overwrite=True):
    """
    Walk every gesture/video folder and:
      - scales to `resolution` (width x height)
      - sets output fps to `target_fps`
      - writes H.264/AAC .mp4 (to a temp file, then renames if overwrite=True)
    """
    for gesture in os.listdir(base_path):
        videos_dir = os.path.join(base_path, gesture, "videos")
        if not os.path.isdir(videos_dir):
            continue

        for fname in os.listdir(videos_dir):
            if not fname.lower().endswith(".mp4"):
                continue

            inp_path = os.path.join(videos_dir, fname)
            # always write to a new file
            out_tmp = inp_path.replace(".mp4", "_tmp.mp4")
            out_final = inp_path if overwrite else inp_path.replace(".mp4", f"_{target_fps}fps.mp4")

            print(f"\nFFmpeg →\n  IN : {inp_path}\n  OUT: {out_tmp}\n")

            try:
                (
                    ffmpeg
                    .input(inp_path)
                    .filter("fps", fps=target_fps, round="up")
                    .filter("scale", resolution[0], resolution[1])
                    .output(out_tmp,
                            vcodec="libx264",
                            acodec="aac",
                            pix_fmt="yuv420p",
                            movflags="+faststart")
                    .overwrite_output()
                    .run()   # remove quiet=True to see errors
                )
            except ffmpeg.Error as e:
                print("FFmpeg failed with:\n", e.stderr.decode())
                continue

            # if overwrite was requested, replace original
            if overwrite:
                os.replace(out_tmp, out_final)
            else:
                # just rename tmp → final
                os.rename(out_tmp, out_final)

            print(f"  ✔ Completed: {out_final}")

if __name__ == "__main__":
    dataset_path = "gesture_dataset"
    process_videos_with_ffmpeg(dataset_path,
                               resolution=(640, 640),
                               target_fps=30,
                               overwrite=True)

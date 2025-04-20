import os
import cv2

def extract_frames(base_path, fps=1):
    gestures = [d for d in os.listdir(base_path) if os.path.isdir(os.path.join(base_path, d))]

    for gesture in gestures:
        videos_path = os.path.join(base_path, gesture, "videos")
        frames_base_path = os.path.join(base_path, gesture, "frames")

        if not os.path.exists(videos_path):
            continue

        for file in os.listdir(videos_path):
            if not file.endswith(".mp4"):
                continue

            video_path = os.path.join(videos_path, file)
            video_name = os.path.splitext(file)[0]
            frames_folder = os.path.join(frames_base_path, video_name)
            os.makedirs(frames_folder, exist_ok=True)

            cap = cv2.VideoCapture(video_path)
            frame_rate = int(cap.get(cv2.CAP_PROP_FPS))
            interval = max(1, frame_rate // fps)

            print(f"Extracting frames from {file} at {fps} FPS...")

            count = 0
            saved = 0
            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break
                if count % interval == 0:
                    frame_file = os.path.join(frames_folder, f"frame_{saved:03d}.png")
                    cv2.imwrite(frame_file, frame)
                    saved += 1
                count += 1
            cap.release()

if __name__ == "__main__":
    extract_frames("gesture_dataset", fps=1)

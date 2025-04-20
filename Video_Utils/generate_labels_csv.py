import os
import csv

def generate_labels_csv(base_path, output_file="labels.csv"):
    rows = []
    gestures = [d for d in os.listdir(base_path) if os.path.isdir(os.path.join(base_path, d))]

    for gesture in gestures:
        videos_path = os.path.join(base_path, gesture, "videos")
        frames_base_path = os.path.join(base_path, gesture, "frames")

        if not os.path.exists(videos_path):
            continue

        for file in os.listdir(videos_path):
            if not file.endswith(".mp4"):
                continue

            video_name = os.path.splitext(file)[0]  # e.g. thumbs_up_p01_bright_01
            parts = video_name.split("_")
            if len(parts) < 4:
                print(f"Skipping malformed filename: {file}")
                continue

            gesture_name = gesture
            participant = parts[1].replace("p", "")
            lighting = parts[2]
            take = parts[3]
            frames_path = os.path.join(gesture, "frames", video_name)

            rows.append([
                file,
                gesture_name,
                participant,
                lighting,
                take,
                frames_path
            ])

    # Save to CSV
    csv_path = os.path.join(base_path, output_file)
    with open(csv_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["filename", "gesture", "participant", "lighting", "take", "frames_path"])
        writer.writerows(rows)

    print(f"Saved metadata to {csv_path}")

if __name__ == "__main__":
    generate_labels_csv("gesture_dataset")

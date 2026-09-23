import os
import cv2

DATASET_ROOT = "datasets"

VIDEO_EXTENSIONS = (".mp4", ".avi", ".mov", ".mkv", ".wmv")


def extract_frames(video_path):

    print(f"\nOpening: {video_path}")

    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print("❌ Cannot open video")
        return

    fps = cap.get(cv2.CAP_PROP_FPS)

    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    print(f"FPS: {fps}")
    print(f"Total Frames: {frame_count}")

    if fps <= 0:
        fps = 30

    interval = int(fps)     # 1 frame every second

    video_name = os.path.splitext(os.path.basename(video_path))[0]

    folder = os.path.dirname(video_path)

    count = 0
    saved = 0

    while True:

        ret, frame = cap.read()

        if not ret:
            break

        if count % interval == 0:

            filename = f"{video_name}_{saved:05d}.jpg"

            cv2.imwrite(
                os.path.join(folder, filename),
                frame
            )

            saved += 1

        count += 1

    cap.release()

    print(f"Saved {saved} frames")


for split in ["train", "validation", "test"]:

    split_path = os.path.join(DATASET_ROOT, split)

    print(f"\nChecking {split_path}")

    if not os.path.exists(split_path):
        print("Folder not found")
        continue

    for class_name in os.listdir(split_path):

        class_path = os.path.join(split_path, class_name)

        if not os.path.isdir(class_path):
            continue

        print(f"\nClass: {class_name}")

        files = os.listdir(class_path)

        print(f"Found {len(files)} files")

        for file in files:

            print(file)

            if file.lower().endswith(VIDEO_EXTENSIONS):

                print("✅ Video Detected")

                extract_frames(os.path.join(class_path, file))

print("\nDone")
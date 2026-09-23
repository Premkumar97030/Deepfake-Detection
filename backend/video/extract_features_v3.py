import os
from pathlib import Path

import cv2
import torch
import torch.nn as nn
from torchvision import models, transforms
from PIL import Image

from video import config


# ============================================================
# FRAME SAMPLING
# ============================================================

def sample_frames(video_path, num_frames):

    cap = cv2.VideoCapture(
        str(video_path)
    )

    if not cap.isOpened():

        print(
            f"WARNING: Could not open {video_path}"
        )

        return []

    total_frames = int(
        cap.get(
            cv2.CAP_PROP_FRAME_COUNT
        )
    )

    if total_frames <= 0:

        cap.release()

        return []

    indices = torch.linspace(
        0,
        total_frames - 1,
        steps=num_frames
    ).long().tolist()

    frames = []

    for index in indices:

        cap.set(
            cv2.CAP_PROP_POS_FRAMES,
            index
        )

        success, frame = cap.read()

        if not success:

            continue

        frame = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2RGB
        )

        frames.append(
            Image.fromarray(frame)
        )

    cap.release()

    return frames


# ============================================================
# RESNET50
# ============================================================

def create_resnet():

    print(
        "\nLoading ResNet50..."
    )

    model = models.resnet50(
        weights=models.ResNet50_Weights.DEFAULT
    )

    model.fc = nn.Identity()

    model = model.to(
        config.DEVICE
    )

    model.eval()

    for parameter in model.parameters():

        parameter.requires_grad = False

    print(
        "ResNet50 loaded successfully."
    )

    return model


# ============================================================
# TRANSFORM
# ============================================================

transform = transforms.Compose(
    [
        transforms.Resize(
            (
                config.IMAGE_SIZE,
                config.IMAGE_SIZE
            )
        ),

        transforms.ToTensor(),

        transforms.Normalize(
            mean=[
                0.485,
                0.456,
                0.406
            ],

            std=[
                0.229,
                0.224,
                0.225
            ]
        )
    ]
)


# ============================================================
# PROCESS ONE VIDEO
# ============================================================

@torch.no_grad()
def extract_video_features(
    model,
    video_path
):

    frames = sample_frames(
        video_path,
        config.SEQUENCE_LENGTH
    )

    if len(frames) == 0:

        return None

    # If fewer frames were successfully
    # extracted, repeat the final frame.
    while len(frames) < config.SEQUENCE_LENGTH:

        frames.append(
            frames[-1].copy()
        )

    frames = frames[
        :config.SEQUENCE_LENGTH
    ]

    tensors = []

    for frame in frames:

        tensors.append(
            transform(frame)
        )

    batch = torch.stack(
        tensors
    )

    batch = batch.to(
        config.DEVICE
    )

    features = model(
        batch
    )

    features = features.cpu()

    return features


# ============================================================
# PROCESS SPLIT
# ============================================================

def process_split(
    model,
    split
):

    input_root = Path(
        config.VIDEO_SPLIT_PATH
    ) / split

    output_root = Path(
        config.FEATURE_PATH
    ) / split

    output_root.mkdir(
        parents=True,
        exist_ok=True
    )

    print(
        "\n"
        + "=" * 70
    )

    print(
        f"PROCESSING: {split.upper()}"
    )

    print(
        "=" * 70
    )

    total = 0

    successful = 0

    skipped = 0

    for class_name in config.CLASS_NAMES:

        input_dir = (
            input_root / class_name
        )

        output_dir = (
            output_root / class_name
        )

        output_dir.mkdir(
            parents=True,
            exist_ok=True
        )

        if not input_dir.exists():

            print(
                f"WARNING: {input_dir} "
                f"does not exist."
            )

            continue

        videos = [
            p for p in input_dir.iterdir()
            if p.is_file()
            and p.suffix.lower()
            in config.VIDEO_EXTENSIONS
        ]

        print(
            f"\n{class_name.upper()}: "
            f"{len(videos)} videos"
        )

        for video_path in videos:

            total += 1

            output_file = (
                output_dir
                / f"{video_path.stem}.pt"
            )

            if output_file.exists():

                successful += 1

                continue

            try:

                features = extract_video_features(
                    model,
                    video_path
                )

                if features is None:

                    skipped += 1

                    print(
                        f"SKIPPED: "
                        f"{video_path.name}"
                    )

                    continue

                torch.save(
                    features,
                    output_file
                )

                successful += 1

            except Exception as error:

                skipped += 1

                print(
                    f"ERROR: "
                    f"{video_path.name}"
                )

                print(
                    f"       {error}"
                )

            if total % 10 == 0:

                print(
                    f"Progress: "
                    f"{total} processed"
                )

    print(
        f"\n{split.upper()} completed."
    )

    print(
        f"Processed : {total}"
    )

    print(
        f"Saved     : {successful}"
    )

    print(
        f"Skipped   : {skipped}"
    )


# ============================================================
# MAIN
# ============================================================

def main():

    print("=" * 70)

    print(
        "VIDEO FEATURE EXTRACTION V3"
    )

    print(
        "ResNet50 → 8 frames → 2048-D features"
    )

    print(
        "Classes: FAKE / REAL"
    )

    print("=" * 70)

    print(
        f"\nDevice: {config.DEVICE}"
    )

    if torch.cuda.is_available():

        print(
            "GPU:",
            torch.cuda.get_device_name(0)
        )

    os.makedirs(
        config.FEATURE_PATH,
        exist_ok=True
    )

    model = create_resnet()

    for split in [
        "train",
        "validation",
        "test"
    ]:

        process_split(
            model,
            split
        )

    print("\n")
    print("=" * 70)

    print(
        "FEATURE EXTRACTION COMPLETED"
    )

    print("=" * 70)


if __name__ == "__main__":

    main()
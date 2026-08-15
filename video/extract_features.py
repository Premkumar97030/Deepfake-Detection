import os

import torch
from PIL import Image

from video import config

from video.frame_sampler import sample_frames
from video.preprocessing import video_transform
from video.feature_extractor import ResNetFeatureExtractor


# ============================================================
# FEATURE EXTRACTION
# ============================================================

def extract_video_features(
    video_path,
    model
):

    frames = sample_frames(
        video_path,
        config.SEQUENCE_LENGTH
    )

    processed_frames = []

    for frame in frames:

        image = video_transform(
            frame
        )

        processed_frames.append(
            image
        )

    frames_tensor = torch.stack(
        processed_frames
    )

    frames_tensor = frames_tensor.to(
        config.DEVICE
    )

    with torch.no_grad():

        features = model(
            frames_tensor
        )

    # [16, 2048]

    return features.cpu()


# ============================================================
# PROCESS SPLIT
# ============================================================

def process_split(
    split_name,
    model
):

    source_root = os.path.join(
        config.VIDEO_SPLIT_PATH,
        split_name
    )

    destination_root = os.path.join(
        config.FEATURE_PATH,
        split_name
    )

    total = 0

    for class_name in config.CLASS_NAMES:

        source_folder = os.path.join(
            source_root,
            class_name
        )

        destination_folder = os.path.join(
            destination_root,
            class_name
        )

        os.makedirs(
            destination_folder,
            exist_ok=True
        )

        if not os.path.exists(
            source_folder
        ):
            continue

        videos = [
            filename
            for filename in os.listdir(
                source_folder
            )
            if filename.lower().endswith(
                config.VIDEO_EXTENSIONS
            )
        ]

        print(
            f"\n{split_name.upper()} - "
            f"{class_name.upper()}"
        )

        for index, filename in enumerate(
            videos,
            start=1
        ):

            video_path = os.path.join(
                source_folder,
                filename
            )

            feature_filename = (
                os.path.splitext(
                    filename
                )[0]
                + ".pt"
            )

            feature_path = os.path.join(
                destination_folder,
                feature_filename
            )

            # Don't recompute existing features
            if os.path.exists(
                feature_path
            ):

                print(
                    f"[{index}/{len(videos)}] "
                    f"Already exists: "
                    f"{filename}"
                )

                total += 1

                continue

            try:

                features = extract_video_features(
                    video_path,
                    model
                )

                torch.save(
                    features,
                    feature_path
                )

                print(
                    f"[{index}/{len(videos)}] "
                    f"Processed: "
                    f"{filename}"
                )

                total += 1

            except Exception as e:

                print(
                    f"ERROR: "
                    f"{filename} -> {e}"
                )

    return total


# ============================================================
# MAIN
# ============================================================

def main():

    print("=" * 70)
    print(
        "VIDEO FRAME EXTRACTION + "
        "RESNET50 FEATURE EXTRACTION"
    )
    print("=" * 70)

    print(
        "\nDevice:",
        config.DEVICE
    )

    if torch.cuda.is_available():

        print(
            "GPU:",
            torch.cuda.get_device_name(0)
        )

    print(
        "\nLoading image ResNet50..."
    )

    model = ResNetFeatureExtractor()

    model = model.to(
        config.DEVICE
    )

    model.eval()

    print(
        "ResNet50 feature extractor loaded."
    )

    print(
        "\nSequence length:",
        config.SEQUENCE_LENGTH
    )

    print(
        "Feature size:",
        config.FEATURE_SIZE
    )

    for split in [
        "train",
        "validation",
        "test"
    ]:

        process_split(
            split,
            model
        )

    print("\n")
    print("=" * 70)
    print("FEATURE EXTRACTION COMPLETED")
    print("=" * 70)


if __name__ == "__main__":
    main()
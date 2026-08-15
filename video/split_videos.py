import os
import shutil
import random

from video import config

# ============================================================
# SETTINGS
# ============================================================

TRAIN_RATIO = 0.70

VALIDATION_RATIO = 0.15

TEST_RATIO = 0.15
import os
import shutil
import random

from video import config


# ============================================================
# SETTINGS
# ============================================================

TRAIN_RATIO = 0.70
VALIDATION_RATIO = 0.15
TEST_RATIO = 0.15

RANDOM_SEED = 42


# ============================================================
# SPLIT ONE CLASS
# ============================================================

def split_class(class_name):

    source_folder = os.path.join(
        config.RAW_VIDEO_PATH,
        class_name
    )

    if not os.path.exists(source_folder):

        raise FileNotFoundError(
            f"Folder not found: {source_folder}"
        )

    videos = [
        filename
        for filename in os.listdir(source_folder)
        if filename.lower().endswith(
            config.VIDEO_EXTENSIONS
        )
    ]

    videos.sort()

    random.shuffle(videos)

    total = len(videos)

    train_count = int(
        total * TRAIN_RATIO
    )

    validation_count = int(
        total * VALIDATION_RATIO
    )

    train_videos = videos[
        :train_count
    ]

    validation_videos = videos[
        train_count:
        train_count + validation_count
    ]

    test_videos = videos[
        train_count + validation_count:
    ]

    splits = {
        "train": train_videos,
        "validation": validation_videos,
        "test": test_videos
    }

    print("\n" + "=" * 60)
    print(
        f"{class_name.upper()} - "
        f"{total} videos"
    )
    print("=" * 60)

    for split_name, split_videos in splits.items():

        destination_folder = os.path.join(
            config.VIDEO_SPLIT_PATH,
            split_name,
            class_name
        )

        os.makedirs(
            destination_folder,
            exist_ok=True
        )

        for filename in split_videos:

            source = os.path.join(
                source_folder,
                filename
            )

            destination = os.path.join(
                destination_folder,
                filename
            )

            shutil.copy2(
                source,
                destination
            )

        print(
            f"{split_name:<12}: "
            f"{len(split_videos)}"
        )


# ============================================================
# MAIN
# ============================================================

def main():

    random.seed(
        RANDOM_SEED
    )

    print("=" * 60)
    print("VIDEO DATASET SPLITTING")
    print("=" * 60)

    print("\nSource:")
    print(
        config.RAW_VIDEO_PATH
    )

    print("\nExpected split:")
    print("Train      : 70%")
    print("Validation : 15%")
    print("Test       : 15%")

    for class_name in config.CLASS_NAMES:

        split_class(
            class_name
        )

    print("\n" + "=" * 60)
    print("SPLITTING COMPLETED")
    print("=" * 60)


if __name__ == "__main__":

    main()

RANDOM_SEED = 42


# ============================================================
# SPLIT FUNCTION
# ============================================================

def split_class(class_name):

    source_folder = os.path.join(
        config.RAW_VIDEO_PATH,
        class_name
    )

    if not os.path.exists(source_folder):

        print(
            f"ERROR: Folder not found: {source_folder}"
        )

        return

    videos = [
        filename
        for filename in os.listdir(source_folder)
        if filename.lower().endswith(
            config.VIDEO_EXTENSIONS
        )
    ]

    random.shuffle(videos)

    total = len(videos)

    train_end = int(
        total * TRAIN_RATIO
    )

    validation_end = train_end + int(
        total * VALIDATION_RATIO
    )

    train_videos = videos[:train_end]

    validation_videos = videos[
        train_end:validation_end
    ]

    test_videos = videos[
        validation_end:
    ]

    splits = {
        "train": train_videos,
        "validation": validation_videos,
        "test": test_videos
    }

    print("\n")
    print("=" * 60)
    print(class_name.upper())
    print("=" * 60)

    for split_name, split_videos in splits.items():

        destination = os.path.join(
            config.VIDEO_SPLIT_PATH,
            split_name,
            class_name
        )

        os.makedirs(
            destination,
            exist_ok=True
        )

        for filename in split_videos:

            source = os.path.join(
                source_folder,
                filename
            )

            destination_file = os.path.join(
                destination,
                filename
            )

            shutil.copy2(
                source,
                destination_file
            )

        print(
            f"{split_name:<12}: "
            f"{len(split_videos)} videos"
        )


# ============================================================
# MAIN
# ============================================================

def main():

    random.seed(
        RANDOM_SEED
    )

    print("=" * 60)
    print("VIDEO DATASET SPLITTING")
    print("=" * 60)

    print("\nSplit:")
    print("Train      : 70%")
    print("Validation : 15%")
    print("Test       : 15%")

    for class_name in config.CLASS_NAMES:

        split_class(
            class_name
        )

    print("\n")
    print("=" * 60)
    print("VIDEO SPLITTING COMPLETED")
    print("=" * 60)


if __name__ == "__main__":
    main()
import os
import shutil


# ============================================================
# CONFIGURATION
# ============================================================

DATASET_DIR = "datasets"

SPLITS = [
    "train",
    "validation",
    "test"
]

# Only these are IMAGE classes
IMAGE_CLASSES = [
    "ai",
    "cgi",
    "real"
]

# DeepFake is treated as AI/manipulated,
# but its frames go into video_frames, NOT images.
VIDEO_FRAME_CLASS = "deepfake"


IMAGE_EXTENSIONS = {
    ".jpg",
    ".jpeg",
    ".png",
    ".webp",
    ".bmp",
    ".tif",
    ".tiff"
}


# ============================================================
# COPY NORMAL IMAGES
# ============================================================

def copy_image_dataset():

    total = 0

    print("\n")
    print("=" * 60)
    print("COPYING NORMAL IMAGE DATASET")
    print("=" * 60)

    for split in SPLITS:

        print(f"\nProcessing: {split.upper()}")

        for class_name in IMAGE_CLASSES:

            source_dir = os.path.join(
                DATASET_DIR,
                split,
                class_name
            )

            destination_dir = os.path.join(
                DATASET_DIR,
                "images",
                split,
                class_name
            )

            if not os.path.exists(source_dir):

                print(
                    f"WARNING: {source_dir} does not exist"
                )

                continue

            os.makedirs(
                destination_dir,
                exist_ok=True
            )

            count = 0

            for filename in os.listdir(source_dir):

                source_file = os.path.join(
                    source_dir,
                    filename
                )

                if not os.path.isfile(source_file):
                    continue

                extension = os.path.splitext(
                    filename
                )[1].lower()

                if extension not in IMAGE_EXTENSIONS:
                    continue

                destination_file = os.path.join(
                    destination_dir,
                    filename
                )

                if os.path.exists(destination_file):
                    continue

                shutil.copy2(
                    source_file,
                    destination_file
                )

                count += 1
                total += 1

            print(
                f"  {class_name:8s}: {count} images"
            )

    print("\nNormal images copied:", total)


# ============================================================
# COPY VIDEO FRAMES
# ============================================================

def copy_video_frames():

    total = 0

    print("\n")
    print("=" * 60)
    print("COPYING VIDEO FRAMES")
    print("=" * 60)

    for split in SPLITS:

        print(f"\nProcessing: {split.upper()}")

        source_dir = os.path.join(
            DATASET_DIR,
            split,
            VIDEO_FRAME_CLASS
        )

        destination_dir = os.path.join(
            DATASET_DIR,
            "video_frames",
            split,
            "ai"
        )

        if not os.path.exists(source_dir):

            print(
                f"WARNING: {source_dir} does not exist"
            )

            continue

        os.makedirs(
            destination_dir,
            exist_ok=True
        )

        count = 0

        for filename in os.listdir(source_dir):

            source_file = os.path.join(
                source_dir,
                filename
            )

            if not os.path.isfile(source_file):
                continue

            extension = os.path.splitext(
                filename
            )[1].lower()

            if extension not in IMAGE_EXTENSIONS:
                continue

            destination_file = os.path.join(
                destination_dir,
                filename
            )

            if os.path.exists(destination_file):
                continue

            shutil.copy2(
                source_file,
                destination_file
            )

            count += 1
            total += 1

        print(
            f"  DeepFake frames → video_frames/{split}/ai : {count}"
        )

    print("\nVideo frames copied:", total)


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    print("=" * 60)
    print("DATASET REORGANIZATION")
    print("=" * 60)

    print("\nMapping:")
    print("AI images       → images/")
    print("CGI images      → images/")
    print("Real images     → images/")
    print("DeepFake frames → video_frames/ai/")

    copy_image_dataset()

    copy_video_frames()

    print("\n")
    print("=" * 60)
    print("REORGANIZATION COMPLETED")
    print("=" * 60)
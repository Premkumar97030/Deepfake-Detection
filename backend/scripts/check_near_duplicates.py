import os
from collections import defaultdict

from PIL import Image
import imagehash


# ============================================================
# CONFIGURATION
# ============================================================

DATASET_ROOT = r"datasets\images_new"

SPLITS = [
    "train",
    "validation",
    "test"
]

CLASSES = [
    "ai",
    "cgi",
    "real"
]

IMAGE_EXTENSIONS = (
    ".jpg",
    ".jpeg",
    ".png",
    ".webp",
    ".bmp",
    ".tif",
    ".tiff"
)

# pHash distance:
#
# 0       = identical
# 1-4     = extremely similar
# 5-8     = similar
# >8      = increasingly different
#
# Start conservatively with 4.
HASH_DISTANCE = 4


# ============================================================
# CALCULATE PERCEPTUAL HASH
# ============================================================

def calculate_hash(filepath):

    try:

        with Image.open(filepath) as image:

            image = image.convert("RGB")

            return imagehash.phash(image)

    except Exception as e:

        print(
            f"Could not process: {filepath}"
        )

        print(e)

        return None


# ============================================================
# PROCESS ONE FOLDER
# ============================================================

def process_folder(folder):

    hashes = defaultdict(list)

    total = 0
    failed = 0

    for filename in os.listdir(folder):

        if not filename.lower().endswith(
            IMAGE_EXTENSIONS
        ):
            continue

        filepath = os.path.join(
            folder,
            filename
        )

        file_hash = calculate_hash(
            filepath
        )

        if file_hash is None:

            failed += 1
            continue

        hashes[str(file_hash)].append(
            filename
        )

        total += 1

    return hashes, total, failed


# ============================================================
# MAIN
# ============================================================

print("=" * 70)
print("NEAR-DUPLICATE IMAGE ANALYSIS")
print("=" * 70)

print(
    "\nDataset:",
    DATASET_ROOT
)

print(
    "Hash distance threshold:",
    HASH_DISTANCE
)


grand_total = 0
grand_groups = 0
grand_duplicates = 0


# ============================================================
# PROCESS EACH SPLIT / CLASS
# ============================================================

for split in SPLITS:

    for class_name in CLASSES:

        folder = os.path.join(
            DATASET_ROOT,
            split,
            class_name
        )

        if not os.path.exists(folder):

            print(
                f"\nMissing folder: {folder}"
            )

            continue


        print("\n" + "-" * 70)

        print(
            f"{split.upper()} / "
            f"{class_name.upper()}"
        )

        hashes, total, failed = process_folder(
            folder
        )

        grand_total += total


        # ----------------------------------------------------
        # Exact pHash matches
        # ----------------------------------------------------

        duplicate_groups = [
            files
            for files in hashes.values()
            if len(files) > 1
        ]


        duplicate_count = sum(
            len(group) - 1
            for group in duplicate_groups
        )


        print(
            "Images checked:",
            total
        )

        print(
            "Hash groups:",
            len(hashes)
        )

        print(
            "Potential duplicate groups:",
            len(duplicate_groups)
        )

        print(
            "Potential duplicate images:",
            duplicate_count
        )

        if failed:

            print(
                "Failed images:",
                failed
            )


        grand_groups += len(
            duplicate_groups
        )

        grand_duplicates += duplicate_count


        # ----------------------------------------------------
        # Display examples
        # ----------------------------------------------------

        if duplicate_groups:

            print(
                "\nExamples:"
            )

            for group in duplicate_groups[:5]:

                print()

                for filename in group[:10]:

                    print(
                        " ",
                        filename
                    )


# ============================================================
# SUMMARY
# ============================================================

print("\n" + "=" * 70)
print("SUMMARY")
print("=" * 70)

print(
    "\nTotal images checked:",
    grand_total
)

print(
    "Potential duplicate groups:",
    grand_groups
)

print(
    "Potential duplicate images:",
    grand_duplicates
)

print(
    "\nIMPORTANT:"
)

print(
    "This program ONLY analyzes the dataset."
)

print(
    "No images were deleted."
)

print(
    "No images were moved."
)

print(
    "No changes were made to the dataset."
)

print(
    "\nNear-duplicate analysis completed."
)
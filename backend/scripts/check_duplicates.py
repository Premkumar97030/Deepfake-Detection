import os
import hashlib
from collections import defaultdict

DATASET_ROOT = r"datasets\images_new"

SPLITS = ["train", "validation", "test"]

CLASSES = ["ai", "cgi", "real"]

IMAGE_EXTENSIONS = (
    ".jpg",
    ".jpeg",
    ".png",
    ".webp",
    ".bmp",
    ".tif",
    ".tiff"
)


def calculate_hash(filepath):

    sha256 = hashlib.sha256()

    with open(filepath, "rb") as f:

        while True:

            data = f.read(1024 * 1024)

            if not data:
                break

            sha256.update(data)

    return sha256.hexdigest()


hashes = defaultdict(list)

total_images = 0


print("=" * 70)
print("EXACT DUPLICATE CHECK - images_new")
print("=" * 70)


for split in SPLITS:

    for class_name in CLASSES:

        folder = os.path.join(
            DATASET_ROOT,
            split,
            class_name
        )

        if not os.path.exists(folder):
            print("Missing:", folder)
            continue

        print(
            f"\nProcessing: {split}/{class_name}"
        )

        for filename in os.listdir(folder):

            if not filename.lower().endswith(
                IMAGE_EXTENSIONS
            ):
                continue

            filepath = os.path.join(
                folder,
                filename
            )

            try:

                file_hash = calculate_hash(
                    filepath
                )

                hashes[file_hash].append(
                    (
                        split,
                        class_name,
                        filename
                    )
                )

                total_images += 1

            except Exception as e:

                print(
                    "Could not process:",
                    filepath
                )

                print(e)


# ============================================================
# FIND DUPLICATES
# ============================================================

duplicate_groups = []

for file_hash, files in hashes.items():

    if len(files) > 1:

        duplicate_groups.append(files)


# ============================================================
# CROSS-SPLIT DUPLICATES
# ============================================================

cross_split_duplicates = []

for files in duplicate_groups:

    splits_found = set(
        item[0]
        for item in files
    )

    if len(splits_found) > 1:

        cross_split_duplicates.append(
            files
        )


# ============================================================
# RESULTS
# ============================================================

print("\n" + "=" * 70)
print("RESULTS")
print("=" * 70)

print(
    "\nTotal images checked:",
    total_images
)

print(
    "Duplicate groups:",
    len(duplicate_groups)
)

print(
    "Duplicate groups across splits:",
    len(cross_split_duplicates)
)


# ============================================================
# DISPLAY CROSS-SPLIT DUPLICATES
# ============================================================

if cross_split_duplicates:

    print(
        "\n⚠️ EXACT DUPLICATES ACROSS SPLITS"
    )

    for group in cross_split_duplicates[:20]:

        print("\nDuplicate group:")

        for item in group:

            print(
                f"  {item[0]} / "
                f"{item[1]} / "
                f"{item[2]}"
            )

else:

    print(
        "\n✅ NO EXACT DUPLICATES ACROSS SPLITS"
    )


print(
    "\nDuplicate check completed."
)
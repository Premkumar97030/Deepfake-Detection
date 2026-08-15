import os
import hashlib
from collections import defaultdict

DATASET_ROOT = "datasets/images_clean"

SPLITS = [
    "train",
    "validation",
    "test"
]

IMAGE_EXTENSIONS = (
    ".jpg",
    ".jpeg",
    ".png",
    ".webp",
    ".bmp"
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


print("=" * 60)
print("EXACT DUPLICATE IMAGE CHECK")
print("=" * 60)


for split in SPLITS:

    split_path = os.path.join(
        DATASET_ROOT,
        split
    )

    if not os.path.exists(split_path):
        continue

    for class_name in os.listdir(split_path):

        class_path = os.path.join(
            split_path,
            class_name
        )

        if not os.path.isdir(class_path):
            continue

        for filename in os.listdir(class_path):

            if not filename.lower().endswith(
                IMAGE_EXTENSIONS
            ):
                continue

            filepath = os.path.join(
                class_path,
                filename
            )

            try:

                file_hash = calculate_hash(
                    filepath
                )

                hashes[file_hash].append(
                    (split, class_name, filename)
                )

                total_images += 1

            except Exception as e:

                print(
                    f"Could not process: {filepath}"
                )

                print(e)


print("\nTotal images checked:", total_images)


# ==========================================================
# FIND DUPLICATES ACROSS DIFFERENT SPLITS
# ==========================================================

duplicate_groups = []

for file_hash, files in hashes.items():

    splits_found = set(
        item[0]
        for item in files
    )

    if len(splits_found) > 1:

        duplicate_groups.append(
            files
        )


print("\nDuplicate groups across splits:")

print(len(duplicate_groups))


if len(duplicate_groups) == 0:

    print(
        "\n✅ NO EXACT IMAGE DUPLICATES "
        "FOUND ACROSS TRAIN/VALIDATION/TEST"
    )

else:

    print(
        "\n⚠️ EXACT DUPLICATES FOUND"
    )

    for group in duplicate_groups[:20]:

        print("\nDuplicate:")

        for item in group:

            print(
                f"  {item[0]} / "
                f"{item[1]} / "
                f"{item[2]}"
            )


print("\nDuplicate check completed.")
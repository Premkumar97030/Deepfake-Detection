import os
from collections import defaultdict

DATASET_ROOT = "datasets"

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


def get_deepfake_files(split):

    folder = os.path.join(
        DATASET_ROOT,
        split,
        "deepfake"
    )

    files = []

    if not os.path.exists(folder):
        print(f"Folder not found: {folder}")
        return files

    for filename in os.listdir(folder):

        if filename.lower().endswith(IMAGE_EXTENSIONS):

            files.append(filename)

    return files


def get_video_id(filename):

    name = os.path.splitext(filename)[0]

    # Example:
    #
    # id47_id39_0006_face_00001.jpg
    #
    # Remove the final frame number.
    #
    parts = name.rsplit("_", 1)

    if len(parts) == 2 and parts[1].isdigit():

        return parts[0]

    return None


print("=" * 60)
print("DEEPFAKE VIDEO-LEVEL LEAKAGE CHECK")
print("=" * 60)


# ----------------------------------------------------------
# Collect files
# ----------------------------------------------------------

split_files = {}

for split in SPLITS:

    files = get_deepfake_files(split)

    split_files[split] = files

    print(
        f"\n{split.upper()}: {len(files)} DeepFake frames"
    )


# ----------------------------------------------------------
# Extract video IDs
# ----------------------------------------------------------

split_video_ids = {}

for split in SPLITS:

    ids = set()

    for filename in split_files[split]:

        video_id = get_video_id(filename)

        if video_id is not None:

            ids.add(video_id)

    split_video_ids[split] = ids

    print(
        f"{split.upper()}: {len(ids)} detected video IDs"
    )


# ----------------------------------------------------------
# Check video ID overlap
# ----------------------------------------------------------

train_val = (
    split_video_ids["train"]
    &
    split_video_ids["validation"]
)

train_test = (
    split_video_ids["train"]
    &
    split_video_ids["test"]
)

val_test = (
    split_video_ids["validation"]
    &
    split_video_ids["test"]
)


print("\n" + "=" * 60)
print("VIDEO ID OVERLAP")
print("=" * 60)

print(
    "Train ↔ Validation:",
    len(train_val)
)

print(
    "Train ↔ Test:",
    len(train_test)
)

print(
    "Validation ↔ Test:",
    len(val_test)
)


# ----------------------------------------------------------
# Show suspicious IDs
# ----------------------------------------------------------

if train_val:

    print("\nTrain / Validation suspicious IDs:")

    for item in list(train_val)[:20]:

        print(" ", item)


if train_test:

    print("\nTrain / Test suspicious IDs:")

    for item in list(train_test)[:20]:

        print(" ", item)


if val_test:

    print("\nValidation / Test suspicious IDs:")

    for item in list(val_test)[:20]:

        print(" ", item)


# ----------------------------------------------------------
# Exact filename overlap
# ----------------------------------------------------------

print("\n" + "=" * 60)
print("EXACT FRAME FILENAME OVERLAP")
print("=" * 60)


train_files = set(split_files["train"])
val_files = set(split_files["validation"])
test_files = set(split_files["test"])


print(
    "Train ↔ Validation:",
    len(train_files & val_files)
)

print(
    "Train ↔ Test:",
    len(train_files & test_files)
)

print(
    "Validation ↔ Test:",
    len(val_files & test_files)
)


# ----------------------------------------------------------
# Final result
# ----------------------------------------------------------

if not train_val and not train_test and not val_test:

    print("\n" + "=" * 60)
    print("✅ NO DEEPFAKE VIDEO-ID OVERLAP DETECTED")
    print("=" * 60)

else:

    print("\n" + "=" * 60)
    print("⚠️ POSSIBLE VIDEO-LEVEL LEAKAGE")
    print("=" * 60)

    print(
        "\nDo NOT retrain yet."
    )

    print(
        "We need to inspect the suspicious video IDs."
    )
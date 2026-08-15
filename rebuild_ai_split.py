import os
import shutil
import random
from collections import defaultdict

BASE = r"datasets\images"

SOURCE_DIRS = [
    os.path.join(BASE, "train", "ai"),
    os.path.join(BASE, "validation", "ai"),
    os.path.join(BASE, "test", "ai")
]

OUTPUT_BASE = os.path.join(BASE, "_ai_clean")

SPLITS = {
    "train": 0.70,
    "validation": 0.15,
    "test": 0.15
}

random.seed(42)


def get_source(filename):

    name = os.path.splitext(filename)[0]

    if "_face_" in name:
        return name.split("_face_")[0]

    return name


# ------------------------------------------------------------
# Collect every AI image
# ------------------------------------------------------------

groups = defaultdict(list)

for folder in SOURCE_DIRS:

    if not os.path.exists(folder):
        continue

    for filename in os.listdir(folder):

        if not filename.lower().endswith(
            (".jpg", ".jpeg", ".png", ".webp", ".bmp")
        ):
            continue

        source = get_source(filename)

        groups[source].append(
            os.path.join(folder, filename)
        )


print("=" * 60)
print("REBUILDING AI DATASET BY SOURCE")
print("=" * 60)

print("Total images:", sum(len(v) for v in groups.values()))
print("Unique sources:", len(groups))


# ------------------------------------------------------------
# Shuffle source groups
# ------------------------------------------------------------

source_groups = list(groups.items())

random.shuffle(source_groups)


# ------------------------------------------------------------
# Assign groups to splits
# ------------------------------------------------------------

total_images = sum(
    len(files)
    for _, files in source_groups
)

target_train = int(total_images * SPLITS["train"])
target_val = int(total_images * SPLITS["validation"])

split_groups = {
    "train": [],
    "validation": [],
    "test": []
}

train_count = 0
val_count = 0

for source, files in source_groups:

    if train_count < target_train:

        split_groups["train"].append(
            (source, files)
        )

        train_count += len(files)

    elif val_count < target_val:

        split_groups["validation"].append(
            (source, files)
        )

        val_count += len(files)

    else:

        split_groups["test"].append(
            (source, files)
        )


# ------------------------------------------------------------
# Create clean directories
# ------------------------------------------------------------

for split in SPLITS:

    folder = os.path.join(
        OUTPUT_BASE,
        split,
        "ai"
    )

    os.makedirs(
        folder,
        exist_ok=True
    )


# ------------------------------------------------------------
# Copy files
# ------------------------------------------------------------

counts = {
    "train": 0,
    "validation": 0,
    "test": 0
}

for split, source_groups_list in split_groups.items():

    destination = os.path.join(
        OUTPUT_BASE,
        split,
        "ai"
    )

    for source, files in source_groups_list:

        for source_file in files:

            filename = os.path.basename(
                source_file
            )

            destination_file = os.path.join(
                destination,
                filename
            )

            shutil.copy2(
                source_file,
                destination_file
            )

            counts[split] += 1


# ------------------------------------------------------------
# Results
# ------------------------------------------------------------

print("\nNew AI dataset:")

print("Train      :", counts["train"])
print("Validation :", counts["validation"])
print("Test       :", counts["test"])

print("\nClean AI dataset created at:")

print(OUTPUT_BASE)

print("\nIMPORTANT:")
print("Every source group is kept inside ONE split only.")
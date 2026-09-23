import os
from collections import defaultdict


# ============================================================
# DATASET
# ============================================================

DATASET_ROOT = "datasets/images_clean"

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
    ".bmp"
)


# ============================================================
# SOURCE EXTRACTION
# ============================================================

def get_source_id(filename):

    """
    AI filenames look like:

    id0_id16_0002_face_18.jpg
    id0_id16_0002_face_26.jpg

    Everything before '_face_' is treated
    as the source identifier.
    """

    name = os.path.splitext(filename)[0]

    if "_face_" in name:

        return name.split("_face_")[0]

    # For CGI / REAL images where this pattern
    # does not exist, use the filename itself.

    return name


# ============================================================
# COLLECT SOURCES
# ============================================================

sources = defaultdict(list)

total_images = 0


print("=" * 70)
print("IMAGE SOURCE / VIDEO-LEVEL LEAKAGE CHECK")
print("=" * 70)


for split in SPLITS:

    print(f"\nProcessing: {split}")

    for class_name in CLASSES:

        folder = os.path.join(
            DATASET_ROOT,
            split,
            class_name
        )

        if not os.path.exists(folder):

            print(
                f"WARNING: {folder} not found"
            )

            continue

        for filename in os.listdir(folder):

            if not filename.lower().endswith(
                IMAGE_EXTENSIONS
            ):
                continue

            source_id = get_source_id(
                filename
            )

            sources[source_id].append(
                (
                    split,
                    class_name,
                    filename
                )
            )

            total_images += 1


# ============================================================
# FIND SOURCES ACROSS SPLITS
# ============================================================

leakage = []

for source_id, files in sources.items():

    splits_found = set(
        item[0]
        for item in files
    )

    if len(splits_found) > 1:

        leakage.append(
            (
                source_id,
                files
            )
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
    "Unique source IDs:",
    len(sources)
)

print(
    "Sources appearing in multiple splits:",
    len(leakage)
)


# ============================================================
# DISPLAY LEAKAGE
# ============================================================

if len(leakage) == 0:

    print(
        "\n✅ NO SOURCE-LEVEL LEAKAGE FOUND"
    )

else:

    print(
        "\n⚠️ SOURCE-LEVEL LEAKAGE FOUND"
    )

    print(
        "\nFirst 20 problematic sources:"
    )

    for source_id, files in leakage[:20]:

        print("\nSource:", source_id)

        splits = set(
            item[0]
            for item in files
        )

        print(
            "Appears in:",
            ", ".join(sorted(splits))
        )

        for split, class_name, filename in files[:10]:

            print(
                f"  {split}/{class_name}/{filename}"
            )

        if len(files) > 10:

            print(
                f"  ... and "
                f"{len(files) - 10} more files"
            )


print(
    "\nSource leakage check completed."
)
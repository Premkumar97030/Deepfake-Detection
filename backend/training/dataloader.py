import os

import torch
from torch.utils.data import DataLoader
from torchvision import datasets, transforms

import config


# ============================================================
# IMAGE TRANSFORMS
# ============================================================

train_transform = transforms.Compose([

    transforms.Resize(
        (config.IMAGE_SIZE, config.IMAGE_SIZE)
    ),

    transforms.RandomHorizontalFlip(
        p=0.5
    ),

    transforms.RandomRotation(
        degrees=10
    ),

    transforms.ColorJitter(
        brightness=0.15,
        contrast=0.15,
        saturation=0.15
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
])


# ============================================================
# VALIDATION / TEST TRANSFORMS
# ============================================================

evaluation_transform = transforms.Compose([

    transforms.Resize(
        (config.IMAGE_SIZE, config.IMAGE_SIZE)
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
])


# ============================================================
# CHECK DATASET DIRECTORIES
# ============================================================

required_directories = [
    config.IMAGE_TRAIN_PATH,
    config.IMAGE_VALIDATION_PATH,
    config.IMAGE_TEST_PATH
]


for directory in required_directories:

    if not os.path.exists(directory):

        raise FileNotFoundError(
            f"\nDataset directory not found:\n"
            f"{directory}"
        )


# ============================================================
# DATASETS
# ============================================================

train_dataset = datasets.ImageFolder(
    root=config.IMAGE_TRAIN_PATH,
    transform=train_transform
)


validation_dataset = datasets.ImageFolder(
    root=config.IMAGE_VALIDATION_PATH,
    transform=evaluation_transform
)


test_dataset = datasets.ImageFolder(
    root=config.IMAGE_TEST_PATH,
    transform=evaluation_transform
)


# ============================================================
# CLASS CHECK
# ============================================================

if train_dataset.classes != config.CLASS_NAMES:

    raise ValueError(
        "\nClass mismatch!\n"
        f"Config classes : {config.CLASS_NAMES}\n"
        f"Dataset classes: {train_dataset.classes}"
    )


if validation_dataset.classes != config.CLASS_NAMES:

    raise ValueError(
        "\nValidation class mismatch!\n"
        f"Config classes : {config.CLASS_NAMES}\n"
        f"Dataset classes: {validation_dataset.classes}"
    )


if test_dataset.classes != config.CLASS_NAMES:

    raise ValueError(
        "\nTest class mismatch!\n"
        f"Config classes : {config.CLASS_NAMES}\n"
        f"Dataset classes: {test_dataset.classes}"
    )


# ============================================================
# DATA LOADERS
# ============================================================

train_loader = DataLoader(

    train_dataset,

    batch_size=config.BATCH_SIZE,

    shuffle=True,

    num_workers=config.WORKERS,

    pin_memory=config.PIN_MEMORY
)


validation_loader = DataLoader(

    validation_dataset,

    batch_size=config.BATCH_SIZE,

    shuffle=False,

    num_workers=config.WORKERS,

    pin_memory=config.PIN_MEMORY
)


test_loader = DataLoader(

    test_dataset,

    batch_size=config.BATCH_SIZE,

    shuffle=False,

    num_workers=config.WORKERS,

    pin_memory=config.PIN_MEMORY
)


# ============================================================
# INFORMATION
# ============================================================

print("=" * 60)
print("3-CLASS IMAGE DATASET")
print("=" * 60)

print()

print(
    "Classes:"
)

print(
    train_dataset.classes
)

print()

print(
    "Training Images:"
)

print(
    len(train_dataset)
)

print()

print(
    "Validation Images:"
)

print(
    len(validation_dataset)
)

print()

print(
    "Testing Images:"
)

print(
    len(test_dataset)
)


# ============================================================
# TEST BATCH
# ============================================================

if __name__ == "__main__":

    images, labels = next(
        iter(train_loader)
    )

    print()

    print(
        "Image Batch Shape:"
    )

    print(
        images.shape
    )

    print()

    print(
        "Label Batch Shape:"
    )

    print(
        labels.shape
    )

    print()

    print(
        "Label Example:"
    )

    print(
        labels
    )

    print()

    print(
        "DataLoader working successfully."
    )
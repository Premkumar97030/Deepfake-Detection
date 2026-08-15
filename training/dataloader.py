import torch

from torch.utils.data import DataLoader
from torchvision import datasets

import config

from preprocessing.image_preprocessing import (
    train_transform,
    test_transform
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
    transform=test_transform
)

test_dataset = datasets.ImageFolder(
    root=config.IMAGE_TEST_PATH,
    transform=test_transform
)


# ============================================================
# DATALOADERS
# ============================================================

train_loader = DataLoader(
    train_dataset,
    batch_size=config.BATCH_SIZE,
    shuffle=True,
    num_workers=config.NUM_WORKERS,
    pin_memory=config.PIN_MEMORY
)

validation_loader = DataLoader(
    validation_dataset,
    batch_size=config.BATCH_SIZE,
    shuffle=False,
    num_workers=config.NUM_WORKERS,
    pin_memory=config.PIN_MEMORY
)

test_loader = DataLoader(
    test_dataset,
    batch_size=config.BATCH_SIZE,
    shuffle=False,
    num_workers=config.NUM_WORKERS,
    pin_memory=config.PIN_MEMORY
)


# ============================================================
# TEST DATA LOADER
# ============================================================

if __name__ == "__main__":

    print("=" * 60)
    print("3-CLASS IMAGE DATASET")
    print("=" * 60)

    print("\nClasses:")
    print(train_dataset.classes)

    print("\nTraining Images:")
    print(len(train_dataset))

    print("\nValidation Images:")
    print(len(validation_dataset))

    print("\nTesting Images:")
    print(len(test_dataset))

    # Get one batch
    images, labels = next(iter(train_loader))

    print("\nImage Batch Shape:")
    print(images.shape)

    print("\nLabel Batch Shape:")
    print(labels.shape)

    print("\nLabel Example:")
    print(labels)

    print("\nDataLoader working successfully.")
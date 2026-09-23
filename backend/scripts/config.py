import os
import torch


# ============================================================
# PROJECT DIRECTORY
# ============================================================

PROJECT_DIR = os.path.dirname(
    os.path.abspath(__file__)
)


# ============================================================
# DEVICE
# ============================================================

DEVICE = torch.device(
    "cuda" if torch.cuda.is_available() else "cpu"
)


# ============================================================
# IMAGE DATASET
# ============================================================

TRAIN_DIR = os.path.join(
    PROJECT_DIR,
    "datasets",
    "images_new",
    "train"
)

VALIDATION_DIR = os.path.join(
    PROJECT_DIR,
    "datasets",
    "images_new",
    "validation"
)

TEST_DIR = os.path.join(
    PROJECT_DIR,
    "datasets",
    "images_new",
    "test"
)


# ============================================================
# COMPATIBILITY PATH NAMES
# Used by training/dataloader.py
# ============================================================

IMAGE_TRAIN_PATH = TRAIN_DIR

IMAGE_VALIDATION_PATH = VALIDATION_DIR

IMAGE_TEST_PATH = TEST_DIR


# ============================================================
# IMAGE CLASSES
# ============================================================

CLASS_NAMES = [
    "ai",
    "cgi",
    "real"
]

NUM_CLASSES = len(CLASS_NAMES)


# ============================================================
# IMAGE PROCESSING
# ============================================================

IMAGE_SIZE = 224


# ============================================================
# TRAINING
# ============================================================

BATCH_SIZE = 16

# Fine-tuning the existing ResNet50
EPOCHS = 5

LEARNING_RATE = 0.00001

WEIGHT_DECAY = 0.0001


# ============================================================
# DATALOADER
# ============================================================

WORKERS = 2

PIN_MEMORY = torch.cuda.is_available()


# ============================================================
# EXISTING RESNET50 MODEL
# ============================================================

MODEL_PATH = os.path.join(
    PROJECT_DIR,
    "weights",
    "image_resnet50_best.pth"
)


# ============================================================
# NEW FINE-TUNED MODEL
# ============================================================

NEW_MODEL_PATH = os.path.join(
    PROJECT_DIR,
    "weights",
    "image_resnet50_images_new_best.pth"
)


# ============================================================
# DISPLAY CONFIGURATION
# ============================================================

if __name__ == "__main__":

    print("=" * 60)
    print("IMAGE CLASSIFICATION CONFIGURATION")
    print("=" * 60)

    print()

    print(
        "Train Path      :",
        TRAIN_DIR
    )

    print(
        "Validation Path :",
        VALIDATION_DIR
    )

    print(
        "Test Path       :",
        TEST_DIR
    )

    print()

    print(
        "Image Size      :",
        IMAGE_SIZE
    )

    print(
        "Batch Size      :",
        BATCH_SIZE
    )

    print(
        "Epochs          :",
        EPOCHS
    )

    print(
        "Learning Rate   :",
        LEARNING_RATE
    )

    print(
        "Weight Decay    :",
        WEIGHT_DECAY
    )

    print()

    print(
        "Classes         :",
        CLASS_NAMES
    )

    print(
        "Num Classes     :",
        NUM_CLASSES
    )

    print()

    print(
        "Device          :",
        DEVICE
    )

    if torch.cuda.is_available():

        print(
            "GPU             :",
            torch.cuda.get_device_name(0)
        )

    print()

    print(
        "Workers         :",
        WORKERS
    )

    print(
        "Pin Memory      :",
        PIN_MEMORY
    )

    print()

    print(
        "Existing Model  :",
        MODEL_PATH
    )

    print(
        "New Model       :",
        NEW_MODEL_PATH
    )

    print("=" * 60)
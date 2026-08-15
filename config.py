import os
import torch


# ============================================================
# PROJECT PATH
# ============================================================

PROJECT_DIR = os.path.dirname(
    os.path.abspath(__file__)
)


# ============================================================
# IMAGE DATASET PATHS
# ============================================================

IMAGE_TRAIN_PATH = os.path.join(
    PROJECT_DIR,
    "datasets",
    "images_clean",
    "train"
)

IMAGE_VALIDATION_PATH = os.path.join(
    PROJECT_DIR,
    "datasets",
    "images_clean",
    "validation"
)

IMAGE_TEST_PATH = os.path.join(
    PROJECT_DIR,
    "datasets",
    "images_clean",
    "test"
)


# ============================================================
# IMAGE SETTINGS
# ============================================================

IMAGE_SIZE = 224

BATCH_SIZE = 16

EPOCHS = 10

LEARNING_RATE = 0.0001


# ============================================================
# CLASSES
# ============================================================

CLASS_NAMES = [
    "ai",
    "cgi",
    "real"
]

NUM_CLASSES = len(CLASS_NAMES)


# ============================================================
# DEVICE
# ============================================================

DEVICE = torch.device(
    "cuda" if torch.cuda.is_available() else "cpu"
)


# ============================================================
# GPU / DATALOADER SETTINGS
# ============================================================

NUM_WORKERS = 2

PIN_MEMORY = torch.cuda.is_available()


# ============================================================
# MODEL WEIGHTS
# ============================================================

MODEL_PATH = os.path.join(
    PROJECT_DIR,
    "weights",
    "image_resnet50_best.pth"
)


# ============================================================
# DISPLAY CONFIGURATION
# ============================================================

if __name__ == "__main__":

    print("=" * 60)
    print("IMAGE CLASSIFICATION CONFIGURATION")
    print("=" * 60)

    print()
    print("Train Path      :", IMAGE_TRAIN_PATH)
    print("Validation Path :", IMAGE_VALIDATION_PATH)
    print("Test Path       :", IMAGE_TEST_PATH)

    print()

    print("Image Size      :", IMAGE_SIZE)
    print("Batch Size      :", BATCH_SIZE)
    print("Epochs          :", EPOCHS)
    print("Learning Rate   :", LEARNING_RATE)

    print()

    print("Classes         :", CLASS_NAMES)
    print("Num Classes     :", NUM_CLASSES)

    print()

    print("Device          :", DEVICE)

    if torch.cuda.is_available():

        print(
            "GPU             :",
            torch.cuda.get_device_name(0)
        )

    else:

        print(
            "GPU             : Not available"
        )

    print()

    print("Workers         :", NUM_WORKERS)
    print("Pin Memory      :", PIN_MEMORY)

    print()

    print("Model Path      :", MODEL_PATH)

    print("=" * 60)
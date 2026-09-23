import os
from pathlib import Path
import torch

# Directory locations
BACKEND_DIR = Path(__file__).resolve().parent
PROJECT_DIR = BACKEND_DIR.parent

# Computation Device
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Image Classification Configuration
CLASS_NAMES = ["ai", "cgi", "real"]
NUM_CLASSES = len(CLASS_NAMES)
IMAGE_SIZE = 224
BATCH_SIZE = 16

# Weights resolution: search backend/weights first, then project root weights/
WEIGHTS_DIR = BACKEND_DIR / "weights" if (BACKEND_DIR / "weights").exists() else PROJECT_DIR / "weights"

MODEL_PATH = str(WEIGHTS_DIR / "image_resnet50_best.pth")
NEW_MODEL_PATH = str(WEIGHTS_DIR / "image_resnet50_images_new_best.pth")
VIDEO_MODEL_PATH = str(WEIGHTS_DIR / "video_lstm_v3_best.pth")

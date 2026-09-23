import sys
import os

import torch
from PIL import Image
from torchvision import transforms

import config
from models.resnet import ImageClassifier


# ============================================================
# IMAGE TRANSFORM
# ============================================================

transform = transforms.Compose([
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
# LOAD MODEL
# ============================================================

def load_model():

    model = ImageClassifier()

    checkpoint = torch.load(
        config.NEW_MODEL_PATH,
        map_location=config.DEVICE
    )

    if (
        isinstance(checkpoint, dict)
        and "state_dict" in checkpoint
    ):
        checkpoint = checkpoint["state_dict"]

    # Remove module. if present
    cleaned_state_dict = {}

    for key, value in checkpoint.items():

        if key.startswith("module."):
            key = key[7:]

        cleaned_state_dict[key] = value

    model.load_state_dict(
        cleaned_state_dict
    )

    model = model.to(
        config.DEVICE
    )

    model.eval()

    return model


# ============================================================
# PREDICT
# ============================================================

def predict(image_path):

    if not os.path.exists(image_path):

        raise FileNotFoundError(
            f"Image not found:\n{image_path}"
        )

    model = load_model()

    image = Image.open(
        image_path
    ).convert("RGB")

    image_tensor = transform(
        image
    ).unsqueeze(0)

    image_tensor = image_tensor.to(
        config.DEVICE
    )

    with torch.no_grad():

        outputs = model(
            image_tensor
        )

        probabilities = torch.softmax(
            outputs,
            dim=1
        )[0]

    predicted_index = torch.argmax(
        probabilities
    ).item()

    predicted_class = (
        config.CLASS_NAMES[
            predicted_index
        ]
    )

    confidence = (
        probabilities[
            predicted_index
        ].item() * 100
    )

    print("=" * 60)
    print("DEEPFAKE IMAGE PREDICTION")
    print("=" * 60)

    print()
    print("Image:")
    print(image_path)

    print()
    print("Prediction:")
    print(predicted_class.upper())

    print()
    print(
        f"Confidence: {confidence:.2f}%"
    )

    print()
    print("Class Probabilities:")

    for i, class_name in enumerate(
        config.CLASS_NAMES
    ):

        probability = (
            probabilities[i].item()
            * 100
        )

        print(
            f"{class_name.upper():8s}: "
            f"{probability:.2f}%"
        )

    print("=" * 60)


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    if len(sys.argv) != 2:

        print(
            "\nUsage:"
        )

        print(
            "python predict.py "
            "\"path\\to\\image.jpg\""
        )

        sys.exit(1)

    predict(
        sys.argv[1]
    )
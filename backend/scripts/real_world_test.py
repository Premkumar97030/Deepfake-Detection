import sys
import os

import torch
from PIL import Image
from torchvision import transforms

import config
from models.resnet import ImageClassifier


# ============================================================
# TRANSFORM
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

    print("=" * 70)
    print("LOADING FINE-TUNED RESNET50")
    print("=" * 70)

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

    print()
    print("Model loaded successfully.")
    print("Model:", config.NEW_MODEL_PATH)
    print("Device:", config.DEVICE)

    return model


# ============================================================
# PREDICT SINGLE IMAGE
# ============================================================

def predict_image(model, image_path):

    if not os.path.exists(image_path):
        print()
        print("ERROR: Image not found.")
        print("Path:", image_path)
        return

    try:

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

        print()
        print("=" * 70)
        print("SINGLE IMAGE RESULT")
        print("=" * 70)

        print()
        print("Image      :", os.path.abspath(image_path))
        print("Prediction :", predicted_class.upper())
        print(f"Confidence : {confidence:.2f}%")

        print()
        print("Class Probabilities")
        print("-" * 40)

        for index, class_name in enumerate(
            config.CLASS_NAMES
        ):

            probability = (
                probabilities[index].item()
                * 100
            )

            print(
                f"{class_name.upper():8s}: "
                f"{probability:.2f}%"
            )

        print()
        print("=" * 70)
        print("TEST COMPLETED")
        print("=" * 70)

    except Exception as error:

        print()
        print("ERROR: Could not process image.")
        print("Image:", image_path)
        print("Error:", error)


# ============================================================
# MAIN
# ============================================================

def main():

    print()
    print("=" * 70)
    print("REAL-WORLD SINGLE IMAGE TEST")
    print("=" * 70)

    # --------------------------------------------------------
    # Check command-line argument
    # --------------------------------------------------------

    if len(sys.argv) != 2:

        print()
        print("Usage:")
        print('python real_world_test.py "image_name.jpeg"')
        print()

        print("Example:")
        print('python real_world_test.py "gottam.jpeg"')

        return

    image_path = sys.argv[1]

    # --------------------------------------------------------
    # Load model
    # --------------------------------------------------------

    model = load_model()

    # --------------------------------------------------------
    # Predict
    # --------------------------------------------------------

    predict_image(
        model,
        image_path
    )


# ============================================================
# WINDOWS ENTRY POINT
# ============================================================

if __name__ == "__main__":
    main()
import sys
import os
import torch
from PIL import Image

import config
from models.resnet import ImageClassifier
from preprocessing.image_preprocessing import test_transform


# ============================================================
# LOAD MODEL
# ============================================================

def load_model():

    model = ImageClassifier()

    model.load_state_dict(
        torch.load(
            config.MODEL_PATH,
            map_location=config.DEVICE
        )
    )

    model = model.to(config.DEVICE)
    model.eval()

    return model


# ============================================================
# PREDICT IMAGE
# ============================================================

def predict_image(model, image_path):

    if not os.path.exists(image_path):

        print("ERROR: Image not found.")
        print("Path:", image_path)
        return

    # Open image
    image = Image.open(image_path).convert("RGB")

    # Apply test preprocessing
    image_tensor = test_transform(image)

    # Add batch dimension
    image_tensor = image_tensor.unsqueeze(0)

    # Move to GPU/CPU
    image_tensor = image_tensor.to(
        config.DEVICE
    )

    # Prediction
    with torch.no_grad():

        output = model(image_tensor)

        probabilities = torch.softmax(
            output,
            dim=1
        )

        confidence, predicted_class = torch.max(
            probabilities,
            dim=1
        )

    predicted_class = predicted_class.item()
    confidence = confidence.item() * 100

    predicted_label = config.CLASS_NAMES[
        predicted_class
    ]


    # ========================================================
    # RESULT
    # ========================================================

    print()
    print("=" * 60)
    print("IMAGE PREDICTION")
    print("=" * 60)

    print("Image      :", image_path)

    print(
        "Prediction :",
        predicted_label.upper()
    )

    print(
        f"Confidence : {confidence:.2f}%"
    )

    print()
    print("Class Probabilities:")

    for i, class_name in enumerate(
        config.CLASS_NAMES
    ):

        probability = (
            probabilities[0][i].item() * 100
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

    print("=" * 60)
    print("3-CLASS IMAGE PREDICTION")
    print("=" * 60)

    print(
        "\nDevice:",
        config.DEVICE
    )

    if torch.cuda.is_available():

        print(
            "GPU:",
            torch.cuda.get_device_name(0)
        )

    # Check argument
    if len(sys.argv) < 2:

        print()
        print("Usage:")
        print(
            'python predict_image.py "path_to_image"'
        )

        print()
        print("Example:")
        print(
            'python predict_image.py "real_world_test\\test1.jpg"'
        )

        sys.exit(1)


    image_path = sys.argv[1]

    # Load model
    model = load_model()

    print(
        "\nModel loaded successfully."
    )

    # Predict
    predict_image(
        model,
        image_path
    )
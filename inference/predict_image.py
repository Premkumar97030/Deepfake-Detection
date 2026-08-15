import sys
import torch
from PIL import Image
from torchvision import transforms

import config
from models.resnet import DeepFakeDetector


# ==========================================================
# IMAGE TRANSFORMATION
# ==========================================================

transform = transforms.Compose([
    transforms.Resize(
        (config.IMAGE_SIZE, config.IMAGE_SIZE)
    ),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225]
    )
])


# ==========================================================
# LOAD MODEL
# ==========================================================

def load_model():

    model = DeepFakeDetector()

    model.load_state_dict(
        torch.load(
            config.MODEL_PATH,
            map_location=config.DEVICE
        )
    )

    model = model.to(config.DEVICE)

    model.eval()

    return model


# ==========================================================
# PREDICT IMAGE
# ==========================================================

def predict_image(image_path):

    model = load_model()

    # Open image
    image = Image.open(image_path).convert("RGB")

    # Transform image
    image_tensor = transform(image)

    # Add batch dimension
    image_tensor = image_tensor.unsqueeze(0)

    # Move to GPU
    image_tensor = image_tensor.to(config.DEVICE)

    # Prediction
    with torch.no_grad():

        output = model(image_tensor)

        probabilities = torch.softmax(
            output,
            dim=1
        )[0]

        predicted_index = torch.argmax(
            probabilities
        ).item()

    predicted_class = config.CLASS_NAMES[
        predicted_index
    ]

    confidence = probabilities[
        predicted_index
    ].item() * 100

    # ======================================================
    # DISPLAY RESULT
    # ======================================================

    print("\n" + "=" * 55)
    print("DEEPFAKE DETECTION RESULT")
    print("=" * 55)

    print(
        f"\nPrediction : {predicted_class.upper()}"
    )

    print(
        f"Confidence : {confidence:.2f}%"
    )

    print("\nClass Probabilities:")

    for class_name, probability in zip(
        config.CLASS_NAMES,
        probabilities
    ):

        print(
            f"{class_name.upper():12s}: "
            f"{probability.item() * 100:.2f}%"
        )

    print("=" * 55)


# ==========================================================
# MAIN
# ==========================================================

if __name__ == "__main__":

    if len(sys.argv) < 2:

        print(
            "\nUsage:"
        )

        print(
            'python -m inference.predict_image "image.jpg"'
        )

        sys.exit(1)

    image_path = sys.argv[1]

    predict_image(image_path)
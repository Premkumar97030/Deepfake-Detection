import os
import torch
from PIL import Image
from sklearn.metrics import classification_report, confusion_matrix

import config
from models.resnet import ImageClassifier
from preprocessing.image_preprocessing import test_transform


# ============================================================
# CONFIG
# ============================================================

DATASET_ROOT = "real_world_test"

CLASS_NAMES = [
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
# DEVICE
# ============================================================

device = config.DEVICE

print("=" * 70)
print("EXTERNAL REAL-WORLD EVALUATION")
print("=" * 70)

print("\nDevice:", device)

if torch.cuda.is_available():
    print(
        "GPU:",
        torch.cuda.get_device_name(0)
    )


# ============================================================
# LOAD MODEL
# ============================================================

model = ImageClassifier()

model.load_state_dict(
    torch.load(
        config.MODEL_PATH,
        map_location=device
    )
)

model = model.to(device)
model.eval()

print("\nModel loaded successfully.")
print("Weights:", config.MODEL_PATH)


# ============================================================
# EVALUATION
# ============================================================

y_true = []
y_pred = []

results = []

correct = 0
total = 0


for true_class in CLASS_NAMES:

    folder = os.path.join(
        DATASET_ROOT,
        true_class
    )

    if not os.path.exists(folder):

        print(
            f"\nWARNING: Folder not found: {folder}"
        )

        continue

    files = [
        filename
        for filename in os.listdir(folder)
        if filename.lower().endswith(
            IMAGE_EXTENSIONS
        )
    ]

    print(
        f"\n{true_class.upper()} images: {len(files)}"
    )

    for filename in files:

        image_path = os.path.join(
            folder,
            filename
        )

        try:

            image = Image.open(
                image_path
            ).convert("RGB")

            image_tensor = test_transform(
                image
            ).unsqueeze(0)

            image_tensor = image_tensor.to(
                device
            )

            with torch.no_grad():

                outputs = model(
                    image_tensor
                )

                probabilities = torch.softmax(
                    outputs,
                    dim=1
                )

                confidence, predicted_index = torch.max(
                    probabilities,
                    dim=1
                )

            predicted_class = CLASS_NAMES[
                predicted_index.item()
            ]

            confidence_value = (
                confidence.item() * 100
            )

            y_true.append(true_class)
            y_pred.append(predicted_class)

            total += 1

            if predicted_class == true_class:
                correct += 1

            results.append({
                "file": filename,
                "actual": true_class,
                "predicted": predicted_class,
                "confidence": confidence_value
            })

        except Exception as e:

            print(
                f"ERROR: {filename} -> {e}"
            )


# ============================================================
# ACCURACY
# ============================================================

accuracy = (
    correct / total
    if total > 0
    else 0
)

print("\n")
print("=" * 70)
print("EXTERNAL TEST RESULTS")
print("=" * 70)

print(
    f"\nCorrect Predictions : {correct}/{total}"
)

print(
    f"External Accuracy   : {accuracy * 100:.2f}%"
)


# ============================================================
# CLASSIFICATION REPORT
# ============================================================

print("\nClassification Report:\n")

print(
    classification_report(
        y_true,
        y_pred,
        labels=CLASS_NAMES,
        target_names=CLASS_NAMES,
        digits=4,
        zero_division=0
    )
)


# ============================================================
# CONFUSION MATRIX
# ============================================================

print("\nConfusion Matrix")

print("\nRows = Actual")
print("Columns = Predicted\n")

matrix = confusion_matrix(
    y_true,
    y_pred,
    labels=CLASS_NAMES
)

print(
    "          AI    CGI   REAL"
)

for i, class_name in enumerate(CLASS_NAMES):

    print(
        f"{class_name:<8}",
        matrix[i]
    )


# ============================================================
# WRONG PREDICTIONS
# ============================================================

wrong = [
    result
    for result in results
    if result["actual"] != result["predicted"]
]

print("\n")
print("=" * 70)
print("WRONG PREDICTIONS")
print("=" * 70)

print(
    f"\nTotal wrong predictions: {len(wrong)}"
)

for result in wrong:

    print(
        f"\nFile       : {result['file']}"
    )

    print(
        f"Actual     : {result['actual']}"
    )

    print(
        f"Predicted  : {result['predicted']}"
    )

    print(
        f"Confidence : {result['confidence']:.2f}%"
    )


print("\nExternal evaluation completed.")
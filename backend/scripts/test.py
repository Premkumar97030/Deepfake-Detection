import os

import torch
from torch.utils.data import DataLoader
from torchvision import datasets

from sklearn.metrics import (
    classification_report,
    confusion_matrix
)

import config

from models.resnet import ImageClassifier

from preprocessing.image_preprocessing import (
    test_transform
)


# ============================================================
# MAIN
# ============================================================

def main():

    print("=" * 70)
    print("3-CLASS RESNET50 - FINAL TEST")
    print("=" * 70)

    # ========================================================
    # TEST DATASET
    # ========================================================

    test_dataset = datasets.ImageFolder(
        root=config.IMAGE_TEST_PATH,
        transform=test_transform
    )

    # ========================================================
    # CHECK CLASSES
    # ========================================================

    if test_dataset.classes != config.CLASS_NAMES:

        raise ValueError(
            "\nClass mismatch!\n"
            f"Config classes : {config.CLASS_NAMES}\n"
            f"Test classes   : {test_dataset.classes}"
        )

    # ========================================================
    # TEST DATALOADER
    # ========================================================

    test_loader = DataLoader(

        test_dataset,

        batch_size=config.BATCH_SIZE,

        shuffle=False,

        # Windows-safe
        num_workers=0,

        pin_memory=config.PIN_MEMORY
    )

    # ========================================================
    # CHECK MODEL FILE
    # ========================================================

    if not os.path.exists(
        config.NEW_MODEL_PATH
    ):

        raise FileNotFoundError(
            "\nFine-tuned model not found:\n"
            f"{config.NEW_MODEL_PATH}"
        )

    # ========================================================
    # LOAD FINE-TUNED MODEL
    # ========================================================

    print()
    print("=" * 70)
    print("LOADING FINE-TUNED MODEL")
    print("=" * 70)

    print()
    print(
        "Model:",
        config.NEW_MODEL_PATH
    )

    model = ImageClassifier()

    checkpoint = torch.load(
        config.NEW_MODEL_PATH,
        map_location=config.DEVICE
    )

    # --------------------------------------------------------
    # Handle normal state_dict or checkpoint
    # --------------------------------------------------------

    if (
        isinstance(checkpoint, dict)
        and "state_dict" in checkpoint
    ):

        state_dict = checkpoint[
            "state_dict"
        ]

    else:

        state_dict = checkpoint

    # --------------------------------------------------------
    # Remove DataParallel "module." prefix if present
    # --------------------------------------------------------

    cleaned_state_dict = {}

    for key, value in state_dict.items():

        if key.startswith("module."):

            key = key[
                len("module.") :
            ]

        cleaned_state_dict[key] = value

    # --------------------------------------------------------
    # Load weights
    # --------------------------------------------------------

    model.load_state_dict(
        cleaned_state_dict,
        strict=True
    )

    print(
        "\nFine-tuned ResNet50 loaded successfully."
    )

    # ========================================================
    # MOVE MODEL TO DEVICE
    # ========================================================

    model = model.to(
        config.DEVICE
    )

    model.eval()

    # ========================================================
    # INFORMATION
    # ========================================================

    print()
    print("=" * 70)
    print("TEST CONFIGURATION")
    print("=" * 70)

    print()

    print(
        "Classes:"
    )

    print(
        config.CLASS_NAMES
    )

    print()

    print(
        "Test Dataset:"
    )

    print(
        config.IMAGE_TEST_PATH
    )

    print()

    print(
        "Test Images:"
    )

    print(
        len(test_dataset)
    )

    print()

    print(
        "Device:"
    )

    print(
        config.DEVICE
    )

    if torch.cuda.is_available():

        print(
            "GPU:",
            torch.cuda.get_device_name(0)
        )

    # ========================================================
    # TEST
    # ========================================================

    all_predictions = []

    all_labels = []

    correct = 0

    total = 0

    print()
    print("=" * 70)
    print("RUNNING TEST")
    print("=" * 70)

    with torch.no_grad():

        for images, labels in test_loader:

            images = images.to(
                config.DEVICE,
                non_blocking=True
            )

            labels = labels.to(
                config.DEVICE,
                non_blocking=True
            )

            # ------------------------------------------------
            # Forward pass
            # ------------------------------------------------

            outputs = model(
                images
            )

            # ------------------------------------------------
            # Predictions
            # ------------------------------------------------

            predictions = torch.argmax(
                outputs,
                dim=1
            )

            # ------------------------------------------------
            # Accuracy
            # ------------------------------------------------

            correct += (
                predictions == labels
            ).sum().item()

            total += labels.size(0)

            # ------------------------------------------------
            # Store results
            # ------------------------------------------------

            all_predictions.extend(
                predictions.cpu().numpy()
            )

            all_labels.extend(
                labels.cpu().numpy()
            )

    # ========================================================
    # TEST ACCURACY
    # ========================================================

    accuracy = (
        correct / total
    )

    print()
    print("=" * 70)
    print("TEST RESULTS")
    print("=" * 70)

    print()

    print(
        f"Correct Predictions : "
        f"{correct}/{total}"
    )

    print(
        f"Test Accuracy       : "
        f"{accuracy * 100:.2f}%"
    )

    # ========================================================
    # CLASSIFICATION REPORT
    # ========================================================

    print()
    print("=" * 70)
    print("CLASSIFICATION REPORT")
    print("=" * 70)

    report = classification_report(

        all_labels,

        all_predictions,

        target_names=config.CLASS_NAMES,

        digits=4,

        zero_division=0
    )

    print(
        report
    )

    # ========================================================
    # CONFUSION MATRIX
    # ========================================================

    cm = confusion_matrix(

        all_labels,

        all_predictions,

        labels=[
            0,
            1,
            2
        ]
    )

    print("=" * 70)
    print("CONFUSION MATRIX")
    print("=" * 70)

    print()

    print(
        "Rows = Actual"
    )

    print(
        "Columns = Predicted"
    )

    print()

    print(
        f"{'':12s}"
        f"{'AI':>10s}"
        f"{'CGI':>10s}"
        f"{'REAL':>10s}"
    )

    for i, row in enumerate(cm):

        print(
            f"{config.CLASS_NAMES[i]:12s}"
            f"{row[0]:10d}"
            f"{row[1]:10d}"
            f"{row[2]:10d}"
        )

    # ========================================================
    # PER-CLASS ACCURACY
    # ========================================================

    print()
    print("=" * 70)
    print("PER-CLASS ACCURACY")
    print("=" * 70)

    for i, class_name in enumerate(
        config.CLASS_NAMES
    ):

        class_total = cm[i].sum()

        class_correct = cm[i, i]

        if class_total > 0:

            class_accuracy = (
                class_correct /
                class_total
            ) * 100

        else:

            class_accuracy = 0.0

        print(
            f"{class_name:8s}: "
            f"{class_correct}/{class_total} "
            f"({class_accuracy:.2f}%)"
        )

    # ========================================================
    # COMPLETED
    # ========================================================

    print()
    print("=" * 70)
    print("TEST COMPLETED SUCCESSFULLY")
    print("=" * 70)

    print()

    print(
        "Model tested:"
    )

    print(
        config.NEW_MODEL_PATH
    )

    print()

    print(
        f"Final Test Accuracy: "
        f"{accuracy * 100:.2f}%"
    )


# ============================================================
# WINDOWS ENTRY POINT
# ============================================================

if __name__ == "__main__":

    main()
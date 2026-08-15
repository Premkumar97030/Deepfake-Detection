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


def main():

    # ============================================================
    # TEST DATASET
    # ============================================================

    test_dataset = datasets.ImageFolder(
        config.IMAGE_TEST_PATH,
        transform=test_transform
    )

    # Windows-safe: use 0 workers for testing
    test_loader = DataLoader(
        test_dataset,
        batch_size=config.BATCH_SIZE,
        shuffle=False,
        num_workers=0,
        pin_memory=config.PIN_MEMORY
    )


    # ============================================================
    # LOAD MODEL
    # ============================================================

    model = ImageClassifier()

    model.load_state_dict(
        torch.load(
            config.MODEL_PATH,
            map_location=config.DEVICE
        )
    )

    model = model.to(config.DEVICE)

    model.eval()


    # ============================================================
    # INFORMATION
    # ============================================================

    print("=" * 70)
    print("3-CLASS IMAGE CLASSIFICATION - TEST")
    print("=" * 70)

    print("\nClasses:")
    print(config.CLASS_NAMES)

    print("\nTest Images:")
    print(len(test_dataset))

    print("\nDevice:")
    print(config.DEVICE)

    if torch.cuda.is_available():

        print(
            "GPU:",
            torch.cuda.get_device_name(0)
        )


    # ============================================================
    # TEST
    # ============================================================

    all_predictions = []
    all_labels = []

    correct = 0
    total = 0


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


            # Forward pass
            outputs = model(images)


            # Predictions
            predictions = torch.argmax(
                outputs,
                dim=1
            )


            # Accuracy
            correct += (
                predictions == labels
            ).sum().item()

            total += labels.size(0)


            # Save predictions
            all_predictions.extend(
                predictions.cpu().numpy()
            )

            all_labels.extend(
                labels.cpu().numpy()
            )


    # ============================================================
    # TEST ACCURACY
    # ============================================================

    accuracy = correct / total


    print("\n")
    print("=" * 70)
    print("TEST RESULTS")
    print("=" * 70)

    print(
        f"\nCorrect Predictions : {correct}/{total}"
    )

    print(
        f"Test Accuracy       : {accuracy * 100:.2f}%"
    )


    # ============================================================
    # CLASSIFICATION REPORT
    # ============================================================

    print("\n")
    print("=" * 70)
    print("CLASSIFICATION REPORT")
    print("=" * 70)

    print(
        classification_report(
            all_labels,
            all_predictions,
            target_names=config.CLASS_NAMES,
            digits=4
        )
    )


    # ============================================================
    # CONFUSION MATRIX
    # ============================================================

    cm = confusion_matrix(
        all_labels,
        all_predictions
    )


    print("=" * 70)
    print("CONFUSION MATRIX")
    print("=" * 70)

    print("\nRows = Actual")
    print("Columns = Predicted\n")

    print(
        f"{'':12s}"
        f"{'AI':>8s}"
        f"{'CGI':>8s}"
        f"{'REAL':>8s}"
    )


    for i, row in enumerate(cm):

        print(
            f"{config.CLASS_NAMES[i]:12s}"
            f"{row[0]:8d}"
            f"{row[1]:8d}"
            f"{row[2]:8d}"
        )


    print("\nTest completed successfully.")


# ============================================================
# WINDOWS ENTRY POINT
# ============================================================

if __name__ == "__main__":
    main()
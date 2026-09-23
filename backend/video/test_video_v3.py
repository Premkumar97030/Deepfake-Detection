import os

import torch
from torch.utils.data import DataLoader

from sklearn.metrics import (
    classification_report,
    confusion_matrix
)

from video import config

from video.feature_dataset_v3 import (
    FeatureDatasetV3
)

from video.video_model_v3 import (
    VideoLSTM
)


def main():

    print("=" * 70)

    print(
        "VIDEO MODEL TEST V3"
    )

    print(
        "Classes: FAKE / REAL"
    )

    print("=" * 70)

    # ========================================================
    # DATASET
    # ========================================================

    test_dataset = FeatureDatasetV3(
        os.path.join(
            config.FEATURE_PATH,
            "test"
        )
    )

    test_loader = DataLoader(

        test_dataset,

        batch_size=config.BATCH_SIZE,

        shuffle=False,

        num_workers=0,

        pin_memory=torch.cuda.is_available()
    )

    print(
        "\nTest videos:",
        len(test_dataset)
    )

    # ========================================================
    # MODEL
    # ========================================================

    model = VideoLSTM()

    model.load_state_dict(
        torch.load(
            config.VIDEO_MODEL_PATH,
            map_location=config.DEVICE,
            weights_only=True
        )
    )

    model = model.to(
        config.DEVICE
    )

    model.eval()

    print(
        "\nModel loaded successfully."
    )

    # ========================================================
    # PREDICTION
    # ========================================================

    all_predictions = []

    all_labels = []

    with torch.no_grad():

        for features, labels in test_loader:

            features = features.to(
                config.DEVICE
            )

            outputs = model(
                features
            )

            predictions = torch.argmax(
                outputs,
                dim=1
            )

            all_predictions.extend(
                predictions.cpu().tolist()
            )

            all_labels.extend(
                labels.tolist()
            )

    # ========================================================
    # ACCURACY
    # ========================================================

    correct = sum(
        prediction == label
        for prediction, label
        in zip(
            all_predictions,
            all_labels
        )
    )

    total = len(
        all_labels
    )

    accuracy = (
        correct / total
        if total > 0
        else 0
    )

    print(
        f"\nCorrect Predictions : "
        f"{correct}/{total}"
    )

    print(
        f"Test Accuracy       : "
        f"{accuracy * 100:.2f}%"
    )

    # ========================================================
    # CLASSIFICATION REPORT
    # ========================================================

    print(
        "\nClassification Report:\n"
    )

    print(
        classification_report(
            all_labels,
            all_predictions,
            target_names=config.CLASS_NAMES,
            digits=4,
            zero_division=0
        )
    )

    # ========================================================
    # CONFUSION MATRIX
    # ========================================================

    matrix = confusion_matrix(
        all_labels,
        all_predictions
    )

    print(
        "Confusion Matrix\n"
    )

    print(
        "Rows = Actual"
    )

    print(
        "Columns = Predicted\n"
    )

    print(
        "             FAKE   REAL"
    )

    print(
        f"FAKE        "
        f"{matrix[0][0]:5d}"
        f" {matrix[0][1]:6d}"
    )

    print(
        f"REAL        "
        f"{matrix[1][0]:5d}"
        f" {matrix[1][1]:6d}"
    )


if __name__ == "__main__":

    main()
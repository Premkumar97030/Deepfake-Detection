import os

import torch

from torch.utils.data import DataLoader

from sklearn.metrics import (
    classification_report,
    confusion_matrix
)

from video import config

from video.feature_dataset import (
    VideoFeatureDataset
)

from video.video_lstm import (
    VideoLSTM
)


def main():

    print("=" * 70)
    print("VIDEO MODEL TEST")
    print("Classes: FAKE / REAL")
    print("=" * 70)

    dataset = VideoFeatureDataset(
        os.path.join(
            config.FEATURE_PATH,
            "test"
        )
    )

    loader = DataLoader(
        dataset,
        batch_size=config.BATCH_SIZE,
        shuffle=False,
        num_workers=0
    )

    print(
        "\nTest videos:",
        len(dataset)
    )

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

    y_true = []
    y_pred = []

    with torch.no_grad():

        for features, labels in loader:

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

            y_true.extend(
                labels.tolist()
            )

            y_pred.extend(
                predictions.cpu().tolist()
            )

    correct = sum(
        actual == predicted
        for actual, predicted
        in zip(y_true, y_pred)
    )

    total = len(y_true)

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

    print("\nClassification Report:\n")

    print(
        classification_report(
            y_true,
            y_pred,
            labels=[0, 1],
            target_names=[
                "fake",
                "real"
            ],
            digits=4,
            zero_division=0
        )
    )

    matrix = confusion_matrix(
        y_true,
        y_pred,
        labels=[0, 1]
    )

    print("Confusion Matrix")

    print(
        "\nRows = Actual"
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
        f"  {matrix[0][1]:5d}"
    )

    print(
        f"REAL        "
        f"{matrix[1][0]:5d}"
        f"  {matrix[1][1]:5d}"
    )


if __name__ == "__main__":

    main()
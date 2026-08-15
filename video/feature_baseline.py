import os

import torch

from video import config
from video.feature_dataset import VideoFeatureDataset


def collect_features(split):

    dataset = VideoFeatureDataset(
        os.path.join(
            config.FEATURE_PATH,
            split
        )
    )

    features = []
    labels = []

    for i in range(len(dataset)):

        x, y = dataset[i]

        # Average the 16 frames
        x = x.mean(dim=0)

        features.append(x)
        labels.append(y)

    return (
        torch.stack(features),
        torch.stack(labels)
    )


def main():

    print("=" * 70)
    print("VIDEO FEATURE BASELINE")
    print("Classes: FAKE / REAL")
    print("=" * 70)

    train_x, train_y = collect_features(
        "train"
    )

    test_x, test_y = collect_features(
        "test"
    )

    print(
        "\nTrain:",
        train_x.shape,
        train_y.shape
    )

    print(
        "Test:",
        test_x.shape,
        test_y.shape
    )

    # --------------------------------------------------------
    # CLASS MEANS
    # --------------------------------------------------------

    fake_features = train_x[
        train_y == 0
    ]

    real_features = train_x[
        train_y == 1
    ]

    fake_mean = fake_features.mean(
        dim=0
    )

    real_mean = real_features.mean(
        dim=0
    )

    distance = torch.norm(
        fake_mean - real_mean
    )

    print(
        "\nDistance between FAKE and REAL "
        "feature means:"
    )

    print(
        distance.item()
    )

    # --------------------------------------------------------
    # SIMPLE NEAREST-CENTROID CLASSIFIER
    # --------------------------------------------------------

    predictions = []

    for x in test_x:

        fake_distance = torch.norm(
            x - fake_mean
        )

        real_distance = torch.norm(
            x - real_mean
        )

        if fake_distance < real_distance:

            predictions.append(0)

        else:

            predictions.append(1)

    predictions = torch.tensor(
        predictions
    )

    accuracy = (
        predictions == test_y
    ).float().mean()

    print(
        "\nNearest-centroid accuracy:"
    )

    print(
        f"{accuracy.item() * 100:.2f}%"
    )

    # --------------------------------------------------------
    # CONFUSION MATRIX
    # --------------------------------------------------------

    fake_correct = (
        (test_y == 0)
        & (predictions == 0)
    ).sum()

    fake_total = (
        test_y == 0
    ).sum()

    real_correct = (
        (test_y == 1)
        & (predictions == 1)
    ).sum()

    real_total = (
        test_y == 1
    ).sum()

    print(
        "\nFAKE:",
        f"{fake_correct}/{fake_total}"
    )

    print(
        "REAL:",
        f"{real_correct}/{real_total}"
    )


if __name__ == "__main__":
    main()
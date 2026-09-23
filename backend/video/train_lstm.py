import os

import torch
import torch.nn as nn
import torch.optim as optim

from torch.utils.data import DataLoader

from video import config

from video.feature_dataset import (
    VideoFeatureDataset
)

from video.video_lstm import (
    VideoLSTM
)


def evaluate(
    model,
    loader,
    criterion
):

    model.eval()

    total_loss = 0.0
    correct = 0
    total = 0

    with torch.no_grad():

        for features, labels in loader:

            features = features.to(
                config.DEVICE
            )

            labels = labels.to(
                config.DEVICE
            )

            outputs = model(
                features
            )

            loss = criterion(
                outputs,
                labels
            )

            total_loss += (
                loss.item()
                * labels.size(0)
            )

            predictions = torch.argmax(
                outputs,
                dim=1
            )

            correct += (
                predictions == labels
            ).sum().item()

            total += labels.size(0)

    if total == 0:
        return 0.0, 0.0

    return (
        total_loss / total,
        correct / total
    )


def main():

    print("=" * 70)
    print("VIDEO DEEPFAKE DETECTION")
    print("ResNet50 Features + LSTM")
    print("Classes: FAKE / REAL")
    print("=" * 70)

    print("\nDevice:", config.DEVICE)

    if torch.cuda.is_available():

        print(
            "GPU:",
            torch.cuda.get_device_name(0)
        )

    # --------------------------------------------------------
    # DATASETS
    # --------------------------------------------------------

    train_dataset = VideoFeatureDataset(
        os.path.join(
            config.FEATURE_PATH,
            "train"
        )
    )

    validation_dataset = VideoFeatureDataset(
        os.path.join(
            config.FEATURE_PATH,
            "validation"
        )
    )

    print(
        "\nTraining videos:",
        len(train_dataset)
    )

    print(
        "Validation videos:",
        len(validation_dataset)
    )

    # --------------------------------------------------------
    # DATALOADERS
    # --------------------------------------------------------

    train_loader = DataLoader(
        train_dataset,
        batch_size=config.BATCH_SIZE,
        shuffle=True,
        num_workers=0,
        pin_memory=torch.cuda.is_available()
    )

    validation_loader = DataLoader(
        validation_dataset,
        batch_size=config.BATCH_SIZE,
        shuffle=False,
        num_workers=0,
        pin_memory=torch.cuda.is_available()
    )

    # --------------------------------------------------------
    # MODEL
    # --------------------------------------------------------

    model = VideoLSTM()

    model = model.to(
        config.DEVICE
    )

    # --------------------------------------------------------
    # LOSS
    # --------------------------------------------------------

    criterion = nn.CrossEntropyLoss()

    # --------------------------------------------------------
    # OPTIMIZER
    # --------------------------------------------------------

    optimizer = optim.AdamW(
        model.parameters(),
        lr=config.LEARNING_RATE,
        weight_decay=config.WEIGHT_DECAY
    )

    # --------------------------------------------------------
    # SAVE
    # --------------------------------------------------------

    os.makedirs(
        "weights",
        exist_ok=True
    )

    best_validation_accuracy = 0.0

    # --------------------------------------------------------
    # TRAIN
    # --------------------------------------------------------

    for epoch in range(config.EPOCHS):

        model.train()

        running_loss = 0.0

        correct = 0
        total = 0

        for features, labels in train_loader:

            features = features.to(
                config.DEVICE
            )

            labels = labels.to(
                config.DEVICE
            )

            # Forward
            outputs = model(
                features
            )

            # Loss
            loss = criterion(
                outputs,
                labels
            )

            # Backpropagation
            optimizer.zero_grad()

            loss.backward()

            optimizer.step()

            # Statistics
            running_loss += (
                loss.item()
                * labels.size(0)
            )

            predictions = torch.argmax(
                outputs,
                dim=1
            )

            correct += (
                predictions == labels
            ).sum().item()

            total += labels.size(0)

        train_loss = (
            running_loss / total
        )

        train_accuracy = (
            correct / total
        )

        # Validation
        validation_loss, validation_accuracy = evaluate(
            model,
            validation_loader,
            criterion
        )

        print(
            f"\nEpoch {epoch + 1}/{config.EPOCHS}"
        )

        print(
            f"Train Loss     : {train_loss:.4f}"
        )

        print(
            f"Train Accuracy : "
            f"{train_accuracy * 100:.2f}%"
        )

        print(
            f"Val Loss       : "
            f"{validation_loss:.4f}"
        )

        print(
            f"Val Accuracy   : "
            f"{validation_accuracy * 100:.2f}%"
        )

        # ----------------------------------------------------
        # SAVE BEST MODEL
        # ----------------------------------------------------

        if validation_accuracy > best_validation_accuracy:

            best_validation_accuracy = (
                validation_accuracy
            )

            torch.save(
                model.state_dict(),
                config.VIDEO_MODEL_PATH
            )

            print(
                "✓ Best LSTM model saved."
            )

    print("\n")
    print("=" * 70)
    print("VIDEO LSTM TRAINING COMPLETED")
    print("=" * 70)

    print(
        f"\nBest Validation Accuracy: "
        f"{best_validation_accuracy * 100:.2f}%"
    )

    print(
        "\nSaved:",
        config.VIDEO_MODEL_PATH
    )


if __name__ == "__main__":

    main()
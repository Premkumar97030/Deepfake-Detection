import os

import torch
import torch.nn as nn
import torch.optim as optim

from torch.utils.data import DataLoader

from video import config

from video.feature_dataset_v3 import (
    FeatureDatasetV3
)

from video.video_model_v3 import (
    VideoLSTM
)


# ============================================================
# EVALUATION
# ============================================================

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
                config.DEVICE,
                non_blocking=True
            )

            labels = labels.to(
                config.DEVICE,
                non_blocking=True
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


# ============================================================
# MAIN
# ============================================================

def main():

    print("=" * 70)

    print(
        "VIDEO DEEPFAKE DETECTOR V3"
    )

    print(
        "Saved ResNet50 Features + LSTM"
    )

    print(
        "Classes: FAKE / REAL"
    )

    print("=" * 70)

    print(
        "\nDevice:",
        config.DEVICE
    )

    if torch.cuda.is_available():

        print(
            "GPU:",
            torch.cuda.get_device_name(0)
        )

    # ========================================================
    # DATASETS
    # ========================================================

    train_dataset = FeatureDatasetV3(
        os.path.join(
            config.FEATURE_PATH,
            "train"
        )
    )

    validation_dataset = FeatureDatasetV3(
        os.path.join(
            config.FEATURE_PATH,
            "validation"
        )
    )

    print(
        "\nTraining feature sequences:",
        len(train_dataset)
    )

    print(
        "Validation feature sequences:",
        len(validation_dataset)
    )

    if len(train_dataset) == 0:

        raise RuntimeError(
            "No training features found. "
            "Run extract_features_v3 first."
        )

    # ========================================================
    # DATALOADERS
    # ========================================================

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

    # ========================================================
    # MODEL
    # ========================================================

    model = VideoLSTM()

    model = model.to(
        config.DEVICE
    )

    print(
        "\nLSTM model created."
    )

    # ========================================================
    # LOSS
    # ========================================================

    criterion = nn.CrossEntropyLoss()

    # ========================================================
    # OPTIMIZER
    # ========================================================

    optimizer = optim.AdamW(

        model.parameters(),

        lr=config.LEARNING_RATE,

        weight_decay=config.WEIGHT_DECAY
    )

    # ========================================================
    # SAVE
    # ========================================================

    os.makedirs(
        "weights",
        exist_ok=True
    )

    best_accuracy = 0.0

    patience = 5

    patience_counter = 0

    # ========================================================
    # TRAINING
    # ========================================================

    for epoch in range(
        config.EPOCHS
    ):

        model.train()

        running_loss = 0.0

        correct = 0

        total = 0

        for features, labels in train_loader:

            features = features.to(
                config.DEVICE,
                non_blocking=True
            )

            labels = labels.to(
                config.DEVICE,
                non_blocking=True
            )

            optimizer.zero_grad(
                set_to_none=True
            )

            outputs = model(
                features
            )

            loss = criterion(
                outputs,
                labels
            )

            loss.backward()

            torch.nn.utils.clip_grad_norm_(
                model.parameters(),
                max_norm=1.0
            )

            optimizer.step()

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

        validation_loss, validation_accuracy = evaluate(
            model,
            validation_loader,
            criterion
        )

        print(
            f"\nEpoch {epoch + 1}/"
            f"{config.EPOCHS}"
        )

        print(
            f"Train Loss     : "
            f"{train_loss:.4f}"
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

        # ====================================================
        # BEST MODEL
        # ====================================================

        if validation_accuracy > best_accuracy:

            best_accuracy = (
                validation_accuracy
            )

            torch.save(
                model.state_dict(),
                config.VIDEO_MODEL_PATH
            )

            patience_counter = 0

            print(
                "Best V3 model saved."
            )

        else:

            patience_counter += 1

        # ====================================================
        # EARLY STOPPING
        # ====================================================

        if patience_counter >= patience:

            print(
                "\nEarly stopping."
            )

            break

    print("\n")
    print("=" * 70)

    print(
        "V3 TRAINING COMPLETED"
    )

    print("=" * 70)

    print(
        f"\nBest Validation Accuracy: "
        f"{best_accuracy * 100:.2f}%"
    )

    print(
        "\nSaved:",
        config.VIDEO_MODEL_PATH
    )


if __name__ == "__main__":

    main()
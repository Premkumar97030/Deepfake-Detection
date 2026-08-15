import os
import time

import torch
import torch.nn as nn
import torch.optim as optim

from torch.utils.data import DataLoader

from video import config

from video.video_dataset_v2 import (
    VideoDatasetV2
)

from video.video_model_v2 import (
    VideoResNetLSTM
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

        for videos, labels in loader:

            videos = videos.to(
                config.DEVICE,
                non_blocking=True
            )

            labels = labels.to(
                config.DEVICE,
                non_blocking=True
            )

            outputs = model(
                videos
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
    print("VIDEO DEEPFAKE DETECTOR V2")
    print("ResNet50 + LSTM")
    print("Classes: FAKE / REAL")
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
    # DATASET
    # ========================================================

    train_dataset = VideoDatasetV2(
        os.path.join(
            config.VIDEO_SPLIT_PATH,
            "train"
        )
    )

    validation_dataset = VideoDatasetV2(
        os.path.join(
            config.VIDEO_SPLIT_PATH,
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

    # ========================================================
    # DATALOADER
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

    print(
        "Training batches:",
        len(train_loader)
    )

    print(
        "Validation batches:",
        len(validation_loader)
    )

    # ========================================================
    # MODEL
    # ========================================================

    model = VideoResNetLSTM(
        hidden_size=128,
        num_layers=1,
        dropout=0.5
    )

    model = model.to(
        config.DEVICE
    )

    # ========================================================
    # LOSS
    # ========================================================

    criterion = nn.CrossEntropyLoss()

    # ========================================================
    # OPTIMIZER
    # ========================================================

    optimizer = optim.AdamW(
        filter(
            lambda parameter:
            parameter.requires_grad,
            model.parameters()
        ),
        lr=0.00001,
        weight_decay=0.0001
    )

    # ========================================================
    # SAVE DIRECTORY
    # ========================================================

    os.makedirs(
        "weights",
        exist_ok=True
    )

    best_accuracy = 0.0

    # ========================================================
    # TRAIN
    # ========================================================

    for epoch in range(
        config.EPOCHS
    ):

        epoch_start = time.time()

        print("\n")
        print("=" * 70)

        print(
            f"STARTING EPOCH "
            f"{epoch + 1}/{config.EPOCHS}"
        )

        print("=" * 70)

        model.train()

        running_loss = 0.0

        correct = 0
        total = 0

        # ====================================================
        # TRAINING BATCHES
        # ====================================================

        for batch_index, (
            videos,
            labels
        ) in enumerate(train_loader):

            videos = videos.to(
                config.DEVICE,
                non_blocking=True
            )

            labels = labels.to(
                config.DEVICE,
                non_blocking=True
            )

            # Forward
            outputs = model(
                videos
            )

            # Loss
            loss = criterion(
                outputs,
                labels
            )

            # Backward
            optimizer.zero_grad(
                set_to_none=True
            )

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

            # =================================================
            # PROGRESS
            # =================================================

            if (
                batch_index == 0
                or
                (batch_index + 1) % 10 == 0
                or
                batch_index + 1 == len(train_loader)
            ):

                current_accuracy = (
                    correct / total
                )

                print(
                    f"Batch "
                    f"{batch_index + 1}/"
                    f"{len(train_loader)}"
                    f" | Loss: "
                    f"{loss.item():.4f}"
                    f" | Accuracy: "
                    f"{current_accuracy * 100:.2f}%"
                )

        # ====================================================
        # TRAIN METRICS
        # ====================================================

        train_loss = (
            running_loss / total
        )

        train_accuracy = (
            correct / total
        )

        # ====================================================
        # VALIDATION
        # ====================================================

        print(
            "\nRunning validation..."
        )

        validation_loss, validation_accuracy = evaluate(
            model,
            validation_loader,
            criterion
        )

        epoch_time = (
            time.time()
            - epoch_start
        )

        print("\n")
        print(
            f"Epoch {epoch + 1}/"
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

        print(
            f"Epoch Time     : "
            f"{epoch_time / 60:.2f} minutes"
        )

        # ====================================================
        # SAVE BEST MODEL
        # ====================================================

        if validation_accuracy > best_accuracy:

            best_accuracy = (
                validation_accuracy
            )

            torch.save(
                model.state_dict(),
                "weights/video_resnet_lstm_v2.pth"
            )

            print(
                "✓ Best V2 model saved."
            )

        # ====================================================
        # SAVE CHECKPOINT
        # ====================================================

        torch.save(
            {
                "epoch": epoch + 1,
                "model_state_dict":
                    model.state_dict(),
                "optimizer_state_dict":
                    optimizer.state_dict(),
                "best_accuracy":
                    best_accuracy
            },
            "weights/video_v2_checkpoint.pth"
        )

        print(
            "✓ Checkpoint saved."
        )

    # ========================================================
    # FINISHED
    # ========================================================

    print("\n")
    print("=" * 70)
    print("V2 TRAINING COMPLETED")
    print("=" * 70)

    print(
        f"\nBest Validation Accuracy: "
        f"{best_accuracy * 100:.2f}%"
    )

    print(
        "\nBest model:"
        " weights/video_resnet_lstm_v2.pth"
    )

    print(
        "Checkpoint:"
        " weights/video_v2_checkpoint.pth"
    )


if __name__ == "__main__":

    main()
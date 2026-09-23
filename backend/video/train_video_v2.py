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
# VALIDATION
# ============================================================

def evaluate(
    model,
    loader,
    criterion
):

    model.eval()

    running_loss = 0.0

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

    if total == 0:

        return 0.0, 0.0

    loss = (
        running_loss / total
    )

    accuracy = (
        correct / total
    )

    return loss, accuracy


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
    # DATASETS
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
    # DATALOADERS
    # ========================================================

    train_loader = DataLoader(
        train_dataset,
        batch_size=config.BATCH_SIZE,
        shuffle=True,
        num_workers=0,
        pin_memory=config.PIN_MEMORY
    )

    validation_loader = DataLoader(
        validation_dataset,
        batch_size=config.BATCH_SIZE,
        shuffle=False,
        num_workers=0,
        pin_memory=config.PIN_MEMORY
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

    print(
        "\nCreating ResNet50 + LSTM..."
    )

    model = VideoResNetLSTM(
        hidden_size=config.LSTM_HIDDEN_SIZE,
        num_layers=config.LSTM_NUM_LAYERS,
        dropout=config.LSTM_DROPOUT
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
        lr=config.LEARNING_RATE,
        weight_decay=config.WEIGHT_DECAY
    )

    # ========================================================
    # SCHEDULER
    # ========================================================

    scheduler = optim.lr_scheduler.ReduceLROnPlateau(
        optimizer,
        mode="max",
        factor=0.5,
        patience=2
    )

    # ========================================================
    # SAVE DIRECTORY
    # ========================================================

    os.makedirs(
        os.path.dirname(
            config.VIDEO_V2_MODEL_PATH
        ),
        exist_ok=True
    )

    # ========================================================
    # BEST MODEL
    # ========================================================

    best_accuracy = 0.0

    # ========================================================
    # TRAINING
    # ========================================================

    for epoch in range(
        config.EPOCHS
    ):

        start_time = time.time()

        print("\n")
        print("=" * 70)
        print(
            f"EPOCH {epoch + 1}/{config.EPOCHS}"
        )
        print("=" * 70)

        model.train()

        running_loss = 0.0

        correct = 0

        total = 0

        # ====================================================
        # TRAINING LOOP
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

            optimizer.zero_grad(
                set_to_none=True
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
            loss.backward()

            # Gradient clipping
            torch.nn.utils.clip_grad_norm_(
                model.parameters(),
                max_norm=1.0
            )

            # Update
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

            # Progress
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

        val_loss, val_accuracy = evaluate(
            model,
            validation_loader,
            criterion
        )

        # ====================================================
        # SCHEDULER
        # ====================================================

        scheduler.step(
            val_accuracy
        )

        # ====================================================
        # TIME
        # ====================================================

        elapsed = (
            time.time()
            - start_time
        )

        # ====================================================
        # RESULTS
        # ====================================================

        print("\n")

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
            f"{val_loss:.4f}"
        )

        print(
            f"Val Accuracy   : "
            f"{val_accuracy * 100:.2f}%"
        )

        print(
            f"Learning Rate  : "
            f"{optimizer.param_groups[0]['lr']:.7f}"
        )

        print(
            f"Epoch Time     : "
            f"{elapsed / 60:.2f} minutes"
        )

        # ====================================================
        # SAVE BEST MODEL
        # ====================================================

        if val_accuracy > best_accuracy:

            best_accuracy = val_accuracy

            torch.save(
                model.state_dict(),
                config.VIDEO_V2_MODEL_PATH
            )

            print(
                "\nBest V2 model saved!"
            )

            print(
                "Path:",
                config.VIDEO_V2_MODEL_PATH
            )

    # ========================================================
    # COMPLETED
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
    )

    print(
        config.VIDEO_V2_MODEL_PATH
    )


if __name__ == "__main__":
    main()
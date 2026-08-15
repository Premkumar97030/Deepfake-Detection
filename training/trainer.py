import os
import torch
import torch.nn as nn
import torch.optim as optim

from tqdm import tqdm

import config
from models.resnet import ImageClassifier
from training.dataloader import (
    train_loader,
    validation_loader
)


def train_one_epoch(model, loader, criterion, optimizer):

    model.train()

    running_loss = 0.0
    correct = 0
    total = 0

    progress = tqdm(
        loader,
        desc="Training",
        leave=False
    )

    for images, labels in progress:

        images = images.to(
            config.DEVICE,
            non_blocking=True
        )

        labels = labels.to(
            config.DEVICE,
            non_blocking=True
        )

        # Clear gradients
        optimizer.zero_grad()

        # Forward pass
        outputs = model(images)

        # Calculate loss
        loss = criterion(
            outputs,
            labels
        )

        # Backpropagation
        loss.backward()

        # Update weights
        optimizer.step()

        # Statistics
        running_loss += (
            loss.item() * images.size(0)
        )

        predictions = torch.argmax(
            outputs,
            dim=1
        )

        correct += (
            (predictions == labels)
            .sum()
            .item()
        )

        total += labels.size(0)

        progress.set_postfix(
            loss=f"{loss.item():.4f}"
        )

    epoch_loss = running_loss / total
    epoch_accuracy = correct / total

    return epoch_loss, epoch_accuracy


def validate(model, loader, criterion):

    model.eval()

    running_loss = 0.0
    correct = 0
    total = 0

    with torch.no_grad():

        progress = tqdm(
            loader,
            desc="Validation",
            leave=False
        )

        for images, labels in progress:

            images = images.to(
                config.DEVICE,
                non_blocking=True
            )

            labels = labels.to(
                config.DEVICE,
                non_blocking=True
            )

            outputs = model(images)

            loss = criterion(
                outputs,
                labels
            )

            running_loss += (
                loss.item() * images.size(0)
            )

            predictions = torch.argmax(
                outputs,
                dim=1
            )

            correct += (
                (predictions == labels)
                .sum()
                .item()
            )

            total += labels.size(0)

    epoch_loss = running_loss / total
    epoch_accuracy = correct / total

    return epoch_loss, epoch_accuracy


def main():

    print("=" * 70)
    print("3-CLASS IMAGE CLASSIFICATION")
    print("=" * 70)

    print("\nClasses:")
    print(config.CLASS_NAMES)

    print("\nDevice:")
    print(config.DEVICE)

    if torch.cuda.is_available():

        print(
            "GPU:",
            torch.cuda.get_device_name(0)
        )

    # ======================================================
    # MODEL
    # ======================================================

    model = ImageClassifier()

    model = model.to(
        config.DEVICE
    )

    print(
        "\nModel device:",
        next(model.parameters()).device
    )

    # ======================================================
    # LOSS
    # ======================================================

    criterion = nn.CrossEntropyLoss()

    # ======================================================
    # OPTIMIZER
    # ======================================================

    optimizer = optim.AdamW(
        model.parameters(),
        lr=config.LEARNING_RATE,
        weight_decay=1e-4
    )

    # ======================================================
    # SCHEDULER
    # ======================================================

    scheduler = optim.lr_scheduler.ReduceLROnPlateau(
        optimizer,
        mode="max",
        factor=0.5,
        patience=2
    )

    # ======================================================
    # BEST MODEL
    # ======================================================

    best_val_accuracy = 0.0

    os.makedirs(
        os.path.dirname(config.MODEL_PATH),
        exist_ok=True
    )

    # ======================================================
    # TRAINING
    # ======================================================

    for epoch in range(
        config.EPOCHS
    ):

        print("\n")
        print("=" * 70)
        print(
            f"Epoch {epoch + 1}/{config.EPOCHS}"
        )
        print("=" * 70)

        # ------------------------------
        # Training
        # ------------------------------

        train_loss, train_accuracy = train_one_epoch(
            model,
            train_loader,
            criterion,
            optimizer
        )

        # ------------------------------
        # Validation
        # ------------------------------

        val_loss, val_accuracy = validate(
            model,
            validation_loader,
            criterion
        )

        # ------------------------------
        # Scheduler
        # ------------------------------

        scheduler.step(
            val_accuracy
        )

        # ------------------------------
        # Results
        # ------------------------------

        print(
            f"\nTrain Loss      : {train_loss:.4f}"
        )

        print(
            f"Train Accuracy  : {train_accuracy * 100:.2f}%"
        )

        print(
            f"Val Loss        : {val_loss:.4f}"
        )

        print(
            f"Val Accuracy    : {val_accuracy * 100:.2f}%"
        )

        print(
            f"Learning Rate   : "
            f"{optimizer.param_groups[0]['lr']:.7f}"
        )

        # ------------------------------
        # Save best model
        # ------------------------------

        if val_accuracy > best_val_accuracy:

            best_val_accuracy = val_accuracy

            torch.save(
                model.state_dict(),
                config.MODEL_PATH
            )

            print(
                "\n✅ Best model saved!"
            )

            print(
                "Path:",
                config.MODEL_PATH
            )

    # ======================================================
    # FINISHED
    # ======================================================

    print("\n")
    print("=" * 70)
    print("TRAINING COMPLETED")
    print("=" * 70)

    print(
        f"\nBest Validation Accuracy: "
        f"{best_val_accuracy * 100:.2f}%"
    )

    print(
        "\nBest model:",
        config.MODEL_PATH
    )


if __name__ == "__main__":

    main()
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


# ============================================================
# TRAIN ONE EPOCH
# ============================================================

def train_one_epoch(
    model,
    loader,
    criterion,
    optimizer
):

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

        optimizer.zero_grad(
            set_to_none=True
        )

        outputs = model(
            images
        )

        loss = criterion(
            outputs,
            labels
        )

        loss.backward()

        optimizer.step()

        running_loss += (
            loss.item()
            * images.size(0)
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

    epoch_loss = (
        running_loss / total
    )

    epoch_accuracy = (
        correct / total
    )

    return epoch_loss, epoch_accuracy


# ============================================================
# VALIDATION
# ============================================================

def validate(
    model,
    loader,
    criterion
):

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

            outputs = model(
                images
            )

            loss = criterion(
                outputs,
                labels
            )

            running_loss += (
                loss.item()
                * images.size(0)
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

    epoch_loss = (
        running_loss / total
    )

    epoch_accuracy = (
        correct / total
    )

    return epoch_loss, epoch_accuracy


# ============================================================
# MAIN
# ============================================================

def main():

    print("=" * 70)
    print("3-CLASS RESNET50 FINE-TUNING")
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
        "Training Dataset:"
    )

    print(
        config.TRAIN_DIR
    )

    print()

    print(
        "Validation Dataset:"
    )

    print(
        config.VALIDATION_DIR
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
    # CREATE MODEL
    # ========================================================

    print()
    print("=" * 70)
    print("CREATING RESNET50")
    print("=" * 70)

    model = ImageClassifier()

    # ========================================================
    # LOAD EXISTING MODEL
    # ========================================================

    print()
    print("=" * 70)
    print("LOADING EXISTING MODEL")
    print("=" * 70)

    if not os.path.exists(
        config.MODEL_PATH
    ):

        raise FileNotFoundError(
            "\nExisting model not found:\n"
            f"{config.MODEL_PATH}\n\n"
            "Check MODEL_PATH in config.py."
        )

    print()

    print(
        "Existing Model:"
    )

    print(
        config.MODEL_PATH
    )

    checkpoint = torch.load(
        config.MODEL_PATH,
        map_location=config.DEVICE
    )

    # --------------------------------------------------------
    # Handle different checkpoint formats
    # --------------------------------------------------------

    if isinstance(
        checkpoint,
        dict
    ) and "state_dict" in checkpoint:

        state_dict = checkpoint[
            "state_dict"
        ]

    else:

        state_dict = checkpoint

    # --------------------------------------------------------
    # Remove possible "module." prefix
    # --------------------------------------------------------

    cleaned_state_dict = {}

    for key, value in state_dict.items():

        if key.startswith(
            "module."
        ):

            key = key[
                len("module.") :
            ]

        cleaned_state_dict[
            key
        ] = value

    # --------------------------------------------------------
    # Load weights
    # --------------------------------------------------------

    try:

        model.load_state_dict(
            cleaned_state_dict,
            strict=True
        )

    except RuntimeError as error:

        print()
        print(
            "ERROR: Existing model architecture "
            "does not match ImageClassifier."
        )

        print()
        print(error)

        raise

    print()

    print(
        "Existing ResNet50 weights "
        "loaded successfully."
    )

    # ========================================================
    # MOVE MODEL TO DEVICE
    # ========================================================

    model = model.to(
        config.DEVICE
    )

    print()

    print(
        "Model device:",
        next(
            model.parameters()
        ).device
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
    # SCHEDULER
    # ========================================================

    scheduler = optim.lr_scheduler.ReduceLROnPlateau(

        optimizer,

        mode="max",

        factor=0.5,

        patience=2
    )

    # ========================================================
    # BEST MODEL
    # ========================================================

    best_val_accuracy = 0.0

    os.makedirs(

        os.path.dirname(
            config.NEW_MODEL_PATH
        ),

        exist_ok=True
    )

    # ========================================================
    # TRAINING
    # ========================================================

    for epoch in range(
        config.EPOCHS
    ):

        print()
        print("=" * 70)

        print(
            f"Epoch {epoch + 1}/"
            f"{config.EPOCHS}"
        )

        print("=" * 70)

        # ----------------------------------------------------
        # TRAIN
        # ----------------------------------------------------

        train_loss, train_accuracy = (
            train_one_epoch(

                model,

                train_loader,

                criterion,

                optimizer
            )
        )

        # ----------------------------------------------------
        # VALIDATE
        # ----------------------------------------------------

        val_loss, val_accuracy = (
            validate(

                model,

                validation_loader,

                criterion
            )
        )

        # ----------------------------------------------------
        # SCHEDULER
        # ----------------------------------------------------

        scheduler.step(
            val_accuracy
        )

        # ----------------------------------------------------
        # RESULTS
        # ----------------------------------------------------

        print()

        print(
            f"Train Loss      : "
            f"{train_loss:.4f}"
        )

        print(
            f"Train Accuracy  : "
            f"{train_accuracy * 100:.2f}%"
        )

        print(
            f"Val Loss        : "
            f"{val_loss:.4f}"
        )

        print(
            f"Val Accuracy    : "
            f"{val_accuracy * 100:.2f}%"
        )

        print(
            f"Learning Rate   : "
            f"{optimizer.param_groups[0]['lr']:.7f}"
        )

        # ----------------------------------------------------
        # SAVE BEST MODEL
        # ----------------------------------------------------

        if val_accuracy > best_val_accuracy:

            best_val_accuracy = (
                val_accuracy
            )

            torch.save(

                model.state_dict(),

                config.NEW_MODEL_PATH
            )

            print()

            print(
                "Best fine-tuned model saved!"
            )

            print(
                "Path:",
                config.NEW_MODEL_PATH
            )

    # ========================================================
    # COMPLETED
    # ========================================================

    print()
    print("=" * 70)
    print("FINE-TUNING COMPLETED")
    print("=" * 70)

    print()

    print(
        f"Best Validation Accuracy: "
        f"{best_val_accuracy * 100:.2f}%"
    )

    print()

    print(
        "Original Model:"
    )

    print(
        config.MODEL_PATH
    )

    print()

    print(
        "New Fine-Tuned Model:"
    )

    print(
        config.NEW_MODEL_PATH
    )


# ============================================================
# WINDOWS ENTRY POINT
# ============================================================

if __name__ == "__main__":

    main()
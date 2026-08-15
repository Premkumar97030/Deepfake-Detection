import torch
import torch.nn as nn
import torch.optim as optim

import config

from models.resnet import DeepFakeDetector
from training.dataloader import train_loader, val_loader
from training.trainer import Trainer


def main():

    print("=" * 60)
    print("DeepFake Detection Training")
    print("=" * 60)

    model = DeepFakeDetector()

    criterion = nn.CrossEntropyLoss()

    optimizer = optim.Adam(
        model.parameters(),
        lr=config.LEARNING_RATE
    )

    trainer = Trainer(
        model=model,
        train_loader=train_loader,
        val_loader=val_loader,
        optimizer=optimizer,
        criterion=criterion
    )

    trainer.fit(config.EPOCHS)

    print("\nTraining Completed Successfully.")


if __name__ == "__main__":
    main()
    
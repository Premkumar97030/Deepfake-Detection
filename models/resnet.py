import torch
import torch.nn as nn
from torchvision import models

import config


class ImageClassifier(nn.Module):

    def __init__(self):
        super().__init__()

        # Pretrained ResNet50
        self.model = models.resnet50(
            weights=models.ResNet50_Weights.DEFAULT
        )

        # Get the number of features from the original classifier
        in_features = self.model.fc.in_features

        # Replace classifier with 3-class classifier
        self.model.fc = nn.Linear(
            in_features,
            config.NUM_CLASSES
        )

    def forward(self, x):
        return self.model(x)


if __name__ == "__main__":

    print("=" * 60)
    print("TESTING 3-CLASS RESNET50")
    print("=" * 60)

    model = ImageClassifier()

    print("\nClasses:")
    print(config.CLASS_NAMES)

    print("\nNumber of classes:")
    print(config.NUM_CLASSES)

    # Test input
    x = torch.randn(
        1,
        3,
        config.IMAGE_SIZE,
        config.IMAGE_SIZE
    )

    # Forward pass
    output = model(x)

    print("\nInput Shape:")
    print(x.shape)

    print("\nOutput Shape:")
    print(output.shape)

    print("\nExpected:")
    print("torch.Size([1, 3])")

    print("\nResNet50 test successful.")
import torch
import torch.nn as nn
from torchvision import models

try:
    from backend import config
except ImportError:
    import config


class ImageClassifier(nn.Module):
    def __init__(self, num_classes=None, pretrained=False):
        super().__init__()
        # Initialize ResNet50 backbone (weights loaded separately from checkpoint)
        weights = models.ResNet50_Weights.DEFAULT if pretrained else None
        self.model = models.resnet50(weights=weights)
        in_features = self.model.fc.in_features
        target_classes = num_classes if num_classes is not None else getattr(config, "NUM_CLASSES", 3)
        self.model.fc = nn.Linear(in_features, target_classes)

    def forward(self, x):
        return self.model(x)


if __name__ == "__main__":
    print("Testing 3-Class ResNet50 Classifier")
    model = ImageClassifier()
    x = torch.randn(1, 3, config.IMAGE_SIZE, config.IMAGE_SIZE)
    out = model(x)
    print(f"Output shape: {out.shape}")

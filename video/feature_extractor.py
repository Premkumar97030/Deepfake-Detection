import torch
import torch.nn as nn

from models.resnet import ImageClassifier

from video import config

class ResNetFeatureExtractor(
    nn.Module
):

    def __init__(self):

        super().__init__()

        classifier = ImageClassifier()

        checkpoint = torch.load(
            config.IMAGE_MODEL_PATH,
            map_location=config.DEVICE
        )

        classifier.load_state_dict(
            checkpoint
        )

        # Remove final classification layer
        self.backbone = nn.Sequential(
            *list(
                classifier.model.children()
            )[:-1]
        )

        # Freeze ResNet
        for parameter in self.backbone.parameters():

            parameter.requires_grad = False

    def forward(self, x):

        features = self.backbone(
            x
        )

        features = torch.flatten(
            features,
            start_dim=1
        )

        return features
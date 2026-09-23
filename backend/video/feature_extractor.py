import torch
import torch.nn as nn

from models.resnet import ImageClassifier

from video import config


class ResNetFeatureExtractor(nn.Module):

    def __init__(self):

        super().__init__()

        print("=" * 70)
        print("LOADING RESNET50 FEATURE EXTRACTOR")
        print("=" * 70)

        print()
        print(
            "Image model:",
            config.IMAGE_MODEL_PATH
        )

        # ----------------------------------------------------
        # Create the same 3-class ResNet50 architecture
        # ----------------------------------------------------

        classifier = ImageClassifier()

        # ----------------------------------------------------
        # Load your newly trained image model
        # ----------------------------------------------------

        checkpoint = torch.load(
            config.IMAGE_MODEL_PATH,
            map_location=config.DEVICE
        )

        # ----------------------------------------------------
        # Load weights
        # ----------------------------------------------------

        classifier.load_state_dict(
            checkpoint
        )

        # ----------------------------------------------------
        # Extract ResNet50 backbone
        #
        # Original:
        #
        # ResNet50
        # ├── convolution layers
        # ├── residual blocks
        # └── FC → AI / CGI / REAL
        #
        # We remove FC.
        #
        # Output = 2048 features
        # ----------------------------------------------------

        self.backbone = nn.Sequential(
            *list(
                classifier.model.children()
            )[:-1]
        )

        # ----------------------------------------------------
        # Freeze backbone
        # ----------------------------------------------------

        for parameter in (
            self.backbone.parameters()
        ):

            parameter.requires_grad = False

        # ----------------------------------------------------
        # Device
        # ----------------------------------------------------

        self.backbone = self.backbone.to(
            config.DEVICE
        )

        self.backbone.eval()

        print()
        print(
            "ResNet50 backbone loaded successfully."
        )

        print(
            "Feature size:",
            config.FEATURE_SIZE
        )

        print(
            "Device:",
            config.DEVICE
        )


    def forward(self, x):

        # ----------------------------------------------------
        # ResNet50 feature extraction
        # ----------------------------------------------------

        features = self.backbone(
            x
        )

        # ----------------------------------------------------
        # [B, 2048, 1, 1]
        #         ↓
        # [B, 2048]
        # ----------------------------------------------------

        features = torch.flatten(
            features,
            start_dim=1
        )

        return features
import torch
import torch.nn as nn
from torchvision import models


class VideoResNetLSTM(nn.Module):

    def __init__(
        self,
        hidden_size=128,
        num_layers=1,
        dropout=0.5
    ):

        super().__init__()

        # ====================================================
        # RESNET50
        # ====================================================

        self.resnet = models.resnet50(
            weights=models.ResNet50_Weights.DEFAULT
        )

        # ResNet50 feature size
        feature_size = self.resnet.fc.in_features

        # Remove ImageNet classifier
        self.resnet.fc = nn.Identity()

        # ====================================================
        # FREEZE MOST RESNET LAYERS
        # ====================================================

        for parameter in self.resnet.parameters():

            parameter.requires_grad = False

        # Fine-tune the final ResNet block
        for parameter in self.resnet.layer4.parameters():

            parameter.requires_grad = True

        # ====================================================
        # LSTM
        # ====================================================

        self.lstm = nn.LSTM(

            input_size=feature_size,

            hidden_size=hidden_size,

            num_layers=num_layers,

            batch_first=True,

            dropout=0.0
        )

        # ====================================================
        # DROPOUT
        # ====================================================

        self.dropout = nn.Dropout(
            dropout
        )

        # ====================================================
        # CLASSIFIER
        # ====================================================

        # 0 = FAKE
        # 1 = REAL

        self.classifier = nn.Linear(
            hidden_size,
            2
        )

    def forward(self, x):

        # x:
        # [batch, sequence, channels, height, width]

        batch_size = x.size(0)

        sequence_length = x.size(1)

        channels = x.size(2)

        height = x.size(3)

        width = x.size(4)

        # ====================================================
        # MERGE BATCH + SEQUENCE
        # ====================================================

        x = x.view(
            batch_size * sequence_length,
            channels,
            height,
            width
        )

        # ====================================================
        # RESNET50
        # ====================================================

        features = self.resnet(x)

        # [batch * sequence, 2048]

        # ====================================================
        # RESTORE SEQUENCE
        # ====================================================

        features = features.view(
            batch_size,
            sequence_length,
            -1
        )

        # [batch, sequence, 2048]

        # ====================================================
        # LSTM
        # ====================================================

        output, (hidden, cell) = self.lstm(
            features
        )

        # Last timestep
        last_output = output[:, -1, :]

        # ====================================================
        # DROPOUT
        # ====================================================

        last_output = self.dropout(
            last_output
        )

        # ====================================================
        # CLASSIFIER
        # ====================================================

        logits = self.classifier(
            last_output
        )

        return logits
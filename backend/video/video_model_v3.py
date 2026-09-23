import torch
import torch.nn as nn

from video import config


class VideoLSTM(nn.Module):

    def __init__(self):

        super().__init__()

        self.lstm = nn.LSTM(
            input_size=config.FEATURE_SIZE,
            hidden_size=config.LSTM_HIDDEN_SIZE,
            num_layers=config.LSTM_NUM_LAYERS,
            batch_first=True,
            dropout=config.LSTM_DROPOUT
            if config.LSTM_NUM_LAYERS > 1
            else 0.0
        )

        self.classifier = nn.Sequential(

            nn.Linear(
                config.LSTM_HIDDEN_SIZE,
                64
            ),

            nn.ReLU(),

            nn.Dropout(0.3),

            nn.Linear(
                64,
                config.NUM_CLASSES
            )
        )

    def forward(
        self,
        x
    ):

        output, (
            hidden,
            cell
        ) = self.lstm(x)

        # Last temporal output
        last_output = output[:, -1, :]

        logits = self.classifier(
            last_output
        )

        return logits
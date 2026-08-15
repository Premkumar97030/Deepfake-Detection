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
            dropout=0.0
        )

        self.dropout = nn.Dropout(
            config.LSTM_DROPOUT
        )

        # 2 outputs:
        # 0 = FAKE
        # 1 = REAL
        self.classifier = nn.Linear(
            config.LSTM_HIDDEN_SIZE,
            config.NUM_CLASSES
        )

    def forward(self, x):

        # x shape:
        # [batch, 16, 2048]

        output, (hidden, cell) = self.lstm(x)

        # Take the final time step
        last_output = output[:, -1, :]

        last_output = self.dropout(
            last_output
        )

        logits = self.classifier(
            last_output
        )

        return logits
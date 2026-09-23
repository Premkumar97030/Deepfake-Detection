import torch
import torch.nn as nn


class VideoLSTM(nn.Module):
    def __init__(
        self,
        feature_size: int = 2048,
        hidden_size: int = 128,
        num_layers: int = 1,
        dropout: float = 0.0,
        num_classes: int = 3,
    ):
        super().__init__()
        self.lstm = nn.LSTM(
            input_size=feature_size,
            hidden_size=hidden_size,
            num_layers=num_layers,
            batch_first=True,
            dropout=dropout if num_layers > 1 else 0.0,
        )
        self.classifier = nn.Sequential(
            nn.Linear(hidden_size, 64),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(64, num_classes),
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        output, (hidden, cell) = self.lstm(x)
        last_output = output[:, -1, :]
        return self.classifier(last_output)

from pathlib import Path

import torch
from torch.utils.data import Dataset

from video import config


class FeatureDatasetV3(Dataset):

    def __init__(
        self,
        root
    ):

        self.root = Path(root)

        self.samples = []

        for class_index, class_name in enumerate(
            config.CLASS_NAMES
        ):

            class_dir = (
                self.root / class_name
            )

            if not class_dir.exists():

                continue

            for feature_file in class_dir.glob(
                "*.pt"
            ):

                self.samples.append(
                    (
                        feature_file,
                        class_index
                    )
                )

        self.samples.sort(
            key=lambda item: str(item[0])
        )

    def __len__(self):

        return len(self.samples)

    def __getitem__(
        self,
        index
    ):

        feature_file, label = (
            self.samples[index]
        )

        features = torch.load(
            feature_file,
            map_location="cpu",
            weights_only=True
        )

        features = features.float()

        return (
            features,
            torch.tensor(
                label,
                dtype=torch.long
            )
        )
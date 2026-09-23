import os

import torch

from torch.utils.data import Dataset

from video import config


class VideoFeatureDataset(Dataset):

    def __init__(self, root):

        self.samples = []

        self.class_to_index = {
            "fake": 0,
            "real": 1
        }

        for class_name in config.CLASS_NAMES:

            folder = os.path.join(
                root,
                class_name
            )

            if not os.path.exists(folder):
                continue

            for filename in sorted(
                os.listdir(folder)
            ):

                if filename.lower().endswith(".pt"):

                    path = os.path.join(
                        folder,
                        filename
                    )

                    label = self.class_to_index[
                        class_name
                    ]

                    self.samples.append(
                        (path, label)
                    )

    def __len__(self):

        return len(self.samples)

    def __getitem__(self, index):

        feature_path, label = self.samples[index]

        features = torch.load(
            feature_path,
            map_location="cpu",
            weights_only=True
        )

        expected_shape = (
            config.SEQUENCE_LENGTH,
            config.FEATURE_SIZE
        )

        if features.shape != expected_shape:

            raise ValueError(
                f"Invalid feature shape: "
                f"{features.shape}\n"
                f"Expected: {expected_shape}\n"
                f"File: {feature_path}"
            )

        return (
            features.float(),
            torch.tensor(
                label,
                dtype=torch.long
            )
        )
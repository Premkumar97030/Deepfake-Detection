import os
import cv2
import numpy as np
import torch

from torch.utils.data import Dataset
from torchvision import transforms

from video import config


# ============================================================
# IMAGE TRANSFORM
# ============================================================

transform = transforms.Compose([

    transforms.ToPILImage(),

    transforms.Resize(
        (224, 224)
    ),

    transforms.ToTensor(),

    transforms.Normalize(
        mean=[
            0.485,
            0.456,
            0.406
        ],
        std=[
            0.229,
            0.224,
            0.225
        ]
    )
])


# ============================================================
# VIDEO DATASET
# ============================================================

class VideoDatasetV2(Dataset):

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

                if filename.lower().endswith(
                    config.VIDEO_EXTENSIONS
                ):

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

    # ========================================================
    # SEQUENTIAL FRAME SAMPLING
    # ========================================================

    def sample_frames(self, video_path):

        capture = cv2.VideoCapture(
            video_path
        )

        if not capture.isOpened():

            raise RuntimeError(
                f"Could not open video:\n"
                f"{video_path}"
            )

        total_frames = int(
            capture.get(
                cv2.CAP_PROP_FRAME_COUNT
            )
        )

        if total_frames <= 0:

            capture.release()

            raise RuntimeError(
                f"Invalid frame count:\n"
                f"{video_path}"
            )

        # Select evenly spaced frame numbers
        target_indices = np.linspace(
            0,
            total_frames - 1,
            config.SEQUENCE_LENGTH
        ).astype(int)

        target_set = set(
            target_indices.tolist()
        )

        frames = []

        current_index = 0

        while True:

            success, frame = capture.read()

            if not success:
                break

            if current_index in target_set:

                frame = cv2.cvtColor(
                    frame,
                    cv2.COLOR_BGR2RGB
                )

                frame = transform(
                    frame
                )

                frames.append(
                    frame
                )

                if len(frames) >= config.SEQUENCE_LENGTH:
                    break

            current_index += 1

        capture.release()

        # ====================================================
        # HANDLE MISSING FRAMES
        # ====================================================

        if len(frames) == 0:

            raise RuntimeError(
                f"No frames extracted:\n"
                f"{video_path}"
            )

        while len(frames) < config.SEQUENCE_LENGTH:

            frames.append(
                frames[-1].clone()
            )

        return torch.stack(
            frames[:config.SEQUENCE_LENGTH]
        )

    # ========================================================
    # GET ITEM
    # ========================================================

    def __getitem__(self, index):

        video_path, label = (
            self.samples[index]
        )

        try:

            frames = self.sample_frames(
                video_path
            )

        except Exception as e:

            print(
                f"\nERROR reading video:"
            )

            print(video_path)

            raise e

        return (
            frames,
            torch.tensor(
                label,
                dtype=torch.long
            )
        )
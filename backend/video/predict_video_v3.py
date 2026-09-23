import sys

from pathlib import Path

import torch
import torch.nn.functional as F

from video import config

from video.video_model_v3 import (
    VideoLSTM
)

from video.extract_features_v3 import (
    create_resnet,
    extract_video_features
)


def predict(video_path):

    video_path = Path(
        video_path
    )

    if not video_path.exists():

        raise FileNotFoundError(
            f"Video not found: "
            f"{video_path}"
        )

    print("=" * 70)

    print(
        "VIDEO DEEPFAKE PREDICTION"
    )

    print(
        "Classes: FAKE / REAL"
    )

    print("=" * 70)

    print(
        "\nVideo:",
        video_path
    )

    print(
        "\nDevice:",
        config.DEVICE
    )

    # ========================================================
    # RESNET
    # ========================================================

    resnet = create_resnet()

    # ========================================================
    # EXTRACT FEATURES
    # ========================================================

    print(
        "\nExtracting video features..."
    )

    features = extract_video_features(
        resnet,
        video_path
    )

    if features is None:

        raise RuntimeError(
            "Could not extract features."
        )

    # ========================================================
    # LSTM
    # ========================================================

    model = VideoLSTM()

    model.load_state_dict(
        torch.load(
            config.VIDEO_MODEL_PATH,
            map_location=config.DEVICE,
            weights_only=True
        )
    )

    model = model.to(
        config.DEVICE
    )

    model.eval()

    # ========================================================
    # PREDICTION
    # ========================================================

    features = features.unsqueeze(
        0
    )

    features = features.to(
        config.DEVICE
    )

    with torch.no_grad():

        outputs = model(
            features
        )

        probabilities = F.softmax(
            outputs,
            dim=1
        )

        confidence, prediction = (
            torch.max(
                probabilities,
                dim=1
            )
        )

    predicted_class = (
        config.CLASS_NAMES[
            prediction.item()
        ]
    )

    confidence = (
        confidence.item() * 100
    )

    print(
        "\nPrediction :",
        predicted_class.upper()
    )

    print(
        f"Confidence : "
        f"{confidence:.2f}%"
    )

    print(
        "\nClass probabilities:"
    )

    for index, class_name in enumerate(
        config.CLASS_NAMES
    ):

        print(
            f"{class_name.upper():5} : "
            f"{probabilities[0][index].item() * 100:.2f}%"
        )

    print("\nPrediction completed.")

    return (
        predicted_class,
        confidence
    )


if __name__ == "__main__":

    if len(sys.argv) != 2:

        print(
            "\nUsage:"
        )

        print(
            "python -m video.predict_video_v3 "
            "\"path\\to\\video.mp4\""
        )

        sys.exit(1)

    predict(
        sys.argv[1]
    )
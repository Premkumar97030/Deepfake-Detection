import torch

from video import config

from video.frame_sampler import (
    sample_frames
)

from video.preprocessing import (
    video_transform
)

from video.feature_extractor import (
    ResNetFeatureExtractor
)

from video.video_lstm import (
    VideoLSTM
)


def load_models():

    feature_extractor = (
        ResNetFeatureExtractor()
    )

    feature_extractor = (
        feature_extractor.to(
            config.DEVICE
        )
    )

    feature_extractor.eval()

    lstm = VideoLSTM()

    lstm.load_state_dict(
        torch.load(
            config.VIDEO_MODEL_PATH,
            map_location=config.DEVICE,
            weights_only=True
        )
    )

    lstm = lstm.to(
        config.DEVICE
    )

    lstm.eval()

    return feature_extractor, lstm


def predict_video(
    video_path,
    feature_extractor,
    lstm
):

    frames = sample_frames(
        video_path,
        config.SEQUENCE_LENGTH
    )

    processed_frames = []

    for frame in frames:

        tensor = video_transform(
            frame
        )

        processed_frames.append(
            tensor
        )

    frames_tensor = torch.stack(
        processed_frames
    )

    frames_tensor = frames_tensor.to(
        config.DEVICE
    )

    with torch.no_grad():

        # ResNet50
        features = feature_extractor(
            frames_tensor
        )

        # [16, 2048]
        features = features.unsqueeze(0)

        # [1, 16, 2048]
        outputs = lstm(
            features
        )

        probabilities = torch.softmax(
            outputs,
            dim=1
        )[0]

        confidence, prediction = torch.max(
            probabilities,
            dim=0
        )

    label = config.CLASS_NAMES[
        prediction.item()
    ]

    return {
        "label": label,
        "confidence": confidence.item(),
        "fake_probability": probabilities[0].item(),
        "real_probability": probabilities[1].item()
    }


if __name__ == "__main__":

    import sys

    if len(sys.argv) != 2:

        print(
            "Usage:"
        )

        print(
            'python -m video.predict_video "video.mp4"'
        )

        raise SystemExit

    video_path = sys.argv[1]

    feature_extractor, lstm = (
        load_models()
    )

    result = predict_video(
        video_path,
        feature_extractor,
        lstm
    )

    print("\n" + "=" * 60)
    print("VIDEO PREDICTION")
    print("=" * 60)

    print(
        "\nVideo:",
        video_path
    )

    print(
        "Prediction:",
        result["label"].upper()
    )

    print(
        f"Confidence: "
        f"{result['confidence'] * 100:.2f}%"
    )

    print(
        f"\nFAKE: "
        f"{result['fake_probability'] * 100:.2f}%"
    )

    print(
        f"REAL: "
        f"{result['real_probability'] * 100:.2f}%"
    )
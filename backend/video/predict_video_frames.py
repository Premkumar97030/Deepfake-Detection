import os
import cv2
import torch
import torch.nn as nn

from PIL import Image
from torchvision import models, transforms


# ============================================================
# CONFIGURATION
# ============================================================

MODEL_PATH = "weights/image_resnet50_best.pth"

VIDEO_PATH = "test_video.mp4"

NUM_FRAMES = 16

IMAGE_SIZE = 224

DEVICE = torch.device(
    "cuda" if torch.cuda.is_available() else "cpu"
)

# IMPORTANT:
# Change these only if your image model used a different
# class order during training.
CLASS_NAMES = [
    "fake",
    "real"
]


# ============================================================
# IMAGE TRANSFORMATION
# ============================================================

transform = transforms.Compose([
    transforms.Resize((IMAGE_SIZE, IMAGE_SIZE)),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225]
    )
])


# ============================================================
# LOAD IMAGE MODEL
# ============================================================

def load_model():

    print("\nLoading image model...")

    model = models.resnet50(
        weights=None
    )

    model.fc = nn.Linear(
        model.fc.in_features,
        3
    )

    checkpoint = torch.load(
        MODEL_PATH,
        map_location=DEVICE
    )

    # Handle different checkpoint formats
    if isinstance(checkpoint, dict):

        if "model_state_dict" in checkpoint:

            state_dict = checkpoint[
                "model_state_dict"
            ]

        elif "state_dict" in checkpoint:

            state_dict = checkpoint[
                "state_dict"
            ]

        else:

            state_dict = checkpoint

    else:

        state_dict = checkpoint

    model.load_state_dict(
        state_dict
    )

    model = model.to(
        DEVICE
    )

    model.eval()

    print("Image model loaded successfully.")

    return model


# ============================================================
# SAMPLE VIDEO FRAMES
# ============================================================

def sample_frames(
    video_path,
    num_frames=16
):

    cap = cv2.VideoCapture(
        video_path
    )

    if not cap.isOpened():

        raise RuntimeError(
            f"Could not open video:\n{video_path}"
        )

    total_frames = int(
        cap.get(
            cv2.CAP_PROP_FRAME_COUNT
        )
    )

    fps = cap.get(
        cv2.CAP_PROP_FPS
    )

    duration = (
        total_frames / fps
        if fps > 0
        else 0
    )

    print("\nVideo information")
    print("-" * 60)
    print(
        "Total frames :",
        total_frames
    )
    print(
        "FPS          :",
        round(fps, 2)
    )
    print(
        "Duration     :",
        round(duration, 2),
        "seconds"
    )

    if total_frames <= 0:

        cap.release()

        raise RuntimeError(
            "Video contains no readable frames."
        )

    # If video has fewer frames than requested,
    # sample all available frames.
    actual_num_frames = min(
        num_frames,
        total_frames
    )

    frame_indices = torch.linspace(
        0,
        total_frames - 1,
        actual_num_frames
    ).long().tolist()

    frames = []

    for frame_index in frame_indices:

        cap.set(
            cv2.CAP_PROP_POS_FRAMES,
            frame_index
        )

        success, frame = cap.read()

        if not success:
            continue

        frame = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2RGB
        )

        image = Image.fromarray(
            frame
        )

        frames.append(
            (
                frame_index,
                image
            )
        )

    cap.release()

    print(
        "Frames sampled:",
        len(frames)
    )

    return frames


# ============================================================
# PREDICT FRAMES
# ============================================================

def predict_frames(
    model,
    frames
):

    tensors = []

    valid_indices = []

    for frame_index, image in frames:

        tensor = transform(
            image
        )

        tensors.append(
            tensor
        )

        valid_indices.append(
            frame_index
        )

    if not tensors:

        raise RuntimeError(
            "No valid frames found."
        )

    batch = torch.stack(
        tensors
    )

    batch = batch.to(
        DEVICE
    )

    with torch.no_grad():

        outputs = model(
            batch
        )

        probabilities = torch.softmax(
            outputs,
            dim=1
        )

    return (
        valid_indices,
        probabilities
    )


# ============================================================
# VIDEO DECISION
# ============================================================

def classify_video(
    probabilities
):

    # Image model:
    #
    # class 0 = AI
    # class 1 = CGI
    # class 2 = REAL
    #
    # For video we only want:
    #
    # AI/CGI -> FAKE
    # REAL   -> REAL

    fake_probability = (
        probabilities[:, 0]
        +
        probabilities[:, 1]
    )

    real_probability = (
        probabilities[:, 2]
    )

    # Average probability across frames
    average_fake = (
        fake_probability.mean().item()
    )

    average_real = (
        real_probability.mean().item()
    )

    # Frame-level predictions
    frame_predictions = torch.where(
        fake_probability >= real_probability,
        torch.tensor(0, device=DEVICE),
        torch.tensor(1, device=DEVICE)
    )

    fake_frames = (
        frame_predictions == 0
    ).sum().item()

    real_frames = (
        frame_predictions == 1
    ).sum().item()

    total_frames = (
        len(frame_predictions)
    )

    fake_ratio = (
        fake_frames / total_frames
    )

    real_ratio = (
        real_frames / total_frames
    )

    # --------------------------------------------------------
    # FINAL DECISION
    # --------------------------------------------------------

    # Combine probability and majority voting.
    #
    # Probability gets more weight because it uses
    # the model confidence rather than only argmax.

    final_fake_score = (
        0.70 * average_fake
        +
        0.30 * fake_ratio
    )

    final_real_score = (
        0.70 * average_real
        +
        0.30 * real_ratio
    )

    if final_fake_score >= final_real_score:

        prediction = "FAKE"

        confidence = (
            final_fake_score
        )

    else:

        prediction = "REAL"

        confidence = (
            final_real_score
        )

    return {
        "prediction": prediction,
        "confidence": confidence,
        "average_fake": average_fake,
        "average_real": average_real,
        "fake_frames": fake_frames,
        "real_frames": real_frames,
        "fake_ratio": fake_ratio,
        "real_ratio": real_ratio
    }


# ============================================================
# MAIN
# ============================================================

def main():

    print("=" * 70)

    print(
        "VIDEO DEEPFAKE DETECTOR"
    )

    print(
        "Frame-based ResNet50"
    )

    print(
        "Video Classes: FAKE / REAL"
    )

    print("=" * 70)

    print(
        "\nDevice:",
        DEVICE
    )

    if torch.cuda.is_available():

        print(
            "GPU:",
            torch.cuda.get_device_name(0)
        )

    # --------------------------------------------------------
    # CHECK MODEL
    # --------------------------------------------------------

    if not os.path.exists(
        MODEL_PATH
    ):

        print(
            "\nERROR: Model not found:"
        )

        print(
            MODEL_PATH
        )

        return

    # --------------------------------------------------------
    # CHECK VIDEO
    # --------------------------------------------------------

    if not os.path.exists(
        VIDEO_PATH
    ):

        print(
            "\nERROR: Video not found:"
        )

        print(
            VIDEO_PATH
        )

        print(
            "\nPut the video in the project root"
        )

        print(
            "or change VIDEO_PATH at the top of"
        )

        print(
            "predict_video_frames.py"
        )

        return

    # --------------------------------------------------------
    # LOAD MODEL
    # --------------------------------------------------------

    model = load_model()

    # --------------------------------------------------------
    # SAMPLE FRAMES
    # --------------------------------------------------------

    frames = sample_frames(
        VIDEO_PATH,
        NUM_FRAMES
    )

    # --------------------------------------------------------
    # PREDICT
    # --------------------------------------------------------

    print(
        "\nRunning frame predictions..."
    )

    indices, probabilities = predict_frames(
        model,
        frames
    )

    # --------------------------------------------------------
    # SHOW FRAME RESULTS
    # --------------------------------------------------------

    print("\n" + "=" * 70)

    print(
        "FRAME PREDICTIONS"
    )

    print("=" * 70)

    for i, frame_index in enumerate(
        indices
    ):

        ai = (
            probabilities[i][0]
            .item()
        )

        cgi = (
            probabilities[i][1]
            .item()
        )

        real = (
            probabilities[i][2]
            .item()
        )

        fake = ai + cgi

        if fake >= real:

            prediction = "FAKE"

            confidence = fake

        else:

            prediction = "REAL"

            confidence = real

        print(
            f"Frame {frame_index:6d} | "
            f"{prediction:4s} | "
            f"Fake: {fake * 100:6.2f}% | "
            f"Real: {real * 100:6.2f}%"
        )

    # --------------------------------------------------------
    # VIDEO CLASSIFICATION
    # --------------------------------------------------------

    result = classify_video(
        probabilities
    )

    print("\n" + "=" * 70)

    print(
        "FINAL VIDEO RESULT"
    )

    print("=" * 70)

    print(
        "\nVideo:",
        VIDEO_PATH
    )

    print(
        "\nPrediction:",
        result["prediction"]
    )

    print(
        "Confidence:",
        f"{result['confidence'] * 100:.2f}%"
    )

    print(
        "\nAverage Fake Probability:",
        f"{result['average_fake'] * 100:.2f}%"
    )

    print(
        "Average Real Probability:",
        f"{result['average_real'] * 100:.2f}%"
    )

    print(
        "\nFake Frames:",
        result["fake_frames"]
    )

    print(
        "Real Frames:",
        result["real_frames"]
    )

    print(
        "Fake Frame Ratio:",
        f"{result['fake_ratio'] * 100:.2f}%"
    )

    print(
        "Real Frame Ratio:",
        f"{result['real_ratio'] * 100:.2f}%"
    )

    print(
        "\nVideo classification completed."
    )


if __name__ == "__main__":

    main()
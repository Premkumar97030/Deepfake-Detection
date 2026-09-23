"""Shared inference service for image and frame-based video classification."""

from __future__ import annotations

import time
from pathlib import Path

import cv2
import torch
from PIL import Image
from torchvision import transforms

try:
    from backend import config
    from backend.models.resnet import ImageClassifier
except ImportError:
    import config
    from models.resnet import ImageClassifier


class PredictionService:
    """Loads the trained image model once and exposes image/video predictions."""

    def __init__(self) -> None:
        self.device = config.DEVICE
        self.transform = transforms.Compose([
            transforms.Resize((config.IMAGE_SIZE, config.IMAGE_SIZE)),
            transforms.ToTensor(),
            transforms.Normalize(
                mean=[0.485, 0.456, 0.406],
                std=[0.229, 0.224, 0.225],
            ),
        ])
        self.model = self._load_model()

    def _load_model(self) -> ImageClassifier:
        model = ImageClassifier()
        weights_path = config.NEW_MODEL_PATH if Path(config.NEW_MODEL_PATH).exists() else config.MODEL_PATH
        if not Path(weights_path).exists():
            raise FileNotFoundError(f"Model weights file not found at: {weights_path}")
        
        checkpoint = torch.load(weights_path, map_location=self.device)
        state_dict = checkpoint.get("state_dict", checkpoint) if isinstance(checkpoint, dict) else checkpoint
        cleaned_state_dict = {
            key.removeprefix("module."): value for key, value in state_dict.items()
        }
        model.load_state_dict(cleaned_state_dict)
        return model.to(self.device).eval()

    def _probabilities_for_images(self, images: list[Image.Image]) -> torch.Tensor:
        batch = torch.stack([self.transform(image.convert("RGB")) for image in images]).to(self.device)
        with torch.inference_mode():
            return torch.softmax(self.model(batch), dim=1).cpu()

    @staticmethod
    def _percentage_probabilities(probabilities: torch.Tensor) -> dict[str, float]:
        return {
            class_name: round(float(probabilities[index]) * 100, 2)
            for index, class_name in enumerate(config.CLASS_NAMES)
        }

    def predict_image(self, image: Image.Image) -> dict:
        started_at = time.perf_counter()
        probabilities = self._probabilities_for_images([image])[0]
        prediction_index = int(torch.argmax(probabilities))
        prediction = config.CLASS_NAMES[prediction_index]
        return {
            "media_type": "image",
            "prediction": prediction,
            "display_label": {"ai": "AI Generated", "cgi": "CGI", "real": "Real"}.get(prediction, prediction),
            "confidence": round(float(probabilities[prediction_index]) * 100, 2),
            "probabilities": self._percentage_probabilities(probabilities),
            "model": "Fine-tuned ResNet50",
            "processing_time_ms": round((time.perf_counter() - started_at) * 1000),
        }

    def predict_video(self, video_path: Path, num_frames: int = 16) -> dict:
        started_at = time.perf_counter()
        capture = cv2.VideoCapture(str(video_path))
        if not capture.isOpened():
            raise ValueError("The uploaded file could not be read as a video.")

        total_frames = int(capture.get(cv2.CAP_PROP_FRAME_COUNT))
        fps = float(capture.get(cv2.CAP_PROP_FPS) or 0)
        if total_frames <= 0:
            capture.release()
            raise ValueError("The video does not contain any readable frames.")

        indices = torch.linspace(0, total_frames - 1, min(num_frames, total_frames)).long().tolist()
        frames: list[Image.Image] = []
        for index in indices:
            capture.set(cv2.CAP_PROP_POS_FRAMES, index)
            success, frame = capture.read()
            if success:
                frames.append(Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)))
        capture.release()
        if not frames:
            raise ValueError("No frames could be extracted from the video.")

        frame_probabilities = self._probabilities_for_images(frames)
        fake_probabilities = frame_probabilities[:, 0] + frame_probabilities[:, 1]
        real_probabilities = frame_probabilities[:, 2]
        fake_frames = int((fake_probabilities >= real_probabilities).sum())
        real_frames = len(frames) - fake_frames
        average_fake = float(fake_probabilities.mean())
        average_real = float(real_probabilities.mean())

        # Frame-based score: confidence plus majority vote
        fake_score = 0.70 * average_fake + 0.30 * (fake_frames / len(frames))
        real_score = 0.70 * average_real + 0.30 * (real_frames / len(frames))
        prediction = "fake" if fake_score >= real_score else "real"
        confidence = fake_score if prediction == "fake" else real_score

        return {
            "media_type": "video",
            "prediction": prediction,
            "display_label": "Manipulated / Fake" if prediction == "fake" else "Real",
            "confidence": round(confidence * 100, 2),
            "probabilities": {"fake": round(fake_score * 100, 2), "real": round(real_score * 100, 2)},
            "model": "Fine-tuned ResNet50 (16-frame aggregation)",
            "processing_time_ms": round((time.perf_counter() - started_at) * 1000),
            "sampled_frames": len(frames),
            "video_duration_seconds": round(total_frames / fps, 2) if fps else None,
            "frame_summary": {"fake_frames": fake_frames, "real_frames": real_frames},
        }

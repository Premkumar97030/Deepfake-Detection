"""Backend Model Architectures."""
from .resnet import ImageClassifier
from .lstm import VideoLSTM

__all__ = ["ImageClassifier", "VideoLSTM"]

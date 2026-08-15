import cv2
import numpy as np


def sample_frames(
    video_path,
    sequence_length=16
):

    capture = cv2.VideoCapture(
        video_path
    )

    if not capture.isOpened():

        raise RuntimeError(
            f"Could not open video: {video_path}"
        )

    total_frames = int(
        capture.get(
            cv2.CAP_PROP_FRAME_COUNT
        )
    )

    if total_frames <= 0:

        capture.release()

        raise RuntimeError(
            f"No frames found: {video_path}"
        )

    frame_indices = np.linspace(
        0,
        total_frames - 1,
        sequence_length
    ).astype(int)

    frames = []

    for frame_index in frame_indices:

        capture.set(
            cv2.CAP_PROP_POS_FRAMES,
            int(frame_index)
        )

        success, frame = capture.read()

        if not success:
            continue

        frame = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2RGB
        )

        frames.append(
            frame
        )

    capture.release()

    if len(frames) == 0:

        raise RuntimeError(
            f"Could not extract frames: {video_path}"
        )

    # Fill missing frames if necessary
    while len(frames) < sequence_length:

        frames.append(
            frames[-1].copy()
        )

    return frames[:sequence_length]
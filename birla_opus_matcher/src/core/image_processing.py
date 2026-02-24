from __future__ import annotations

import numpy as np
import cv2


class InvalidImageError(ValueError):
    pass


def decode_image(file_bytes: bytes) -> np.ndarray:
    arr = np.frombuffer(file_bytes, dtype=np.uint8)
    img = cv2.imdecode(arr, cv2.IMREAD_COLOR)
    if img is None:
        raise InvalidImageError("Invalid or unsupported image.")
    return img


def extract_dominant_rgb(img_bgr: np.ndarray) -> tuple[int, int, int]:
    """
    Deterministic extraction:
    - take center crop region
    - apply median blur
    - compute mean RGB
    """
    h, w = img_bgr.shape[:2]
    if h < 20 or w < 20:
        raise InvalidImageError("Image too small to analyze.")

    # center crop 50%
    ch, cw = int(h * 0.5), int(w * 0.5)
    y1 = (h - ch) // 2
    x1 = (w - cw) // 2
    crop = img_bgr[y1:y1 + ch, x1:x1 + cw]

    crop = cv2.medianBlur(crop, 5)
    mean_bgr = crop.reshape(-1, 3).mean(axis=0)

    b, g, r = mean_bgr
    return (int(round(r)), int(round(g)), int(round(b)))

from __future__ import annotations
import math


def confidence_from_delta_e(delta_e: float) -> float:
    """
    Convert ΔE00 into a confidence score in [0, 1].
    Deterministic mapping.

    ΔE00 reference:
    - < 1: imperceptible
    - 1-2: perceptible
    - 2-5: noticeable
    - > 10: very different
    """
    # sigmoid-like curve tuned for paint shade matching
    x = max(0.0, delta_e)
    score = 1.0 / (1.0 + math.exp((x - 3.0) / 1.2))
    return float(max(0.0, min(1.0, score)))

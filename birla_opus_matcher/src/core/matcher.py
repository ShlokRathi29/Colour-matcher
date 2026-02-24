from __future__ import annotations

import numpy as np

from src.core.color_math import rgb_to_lab, ciede2000
from src.core.shade_database import ShadeDatabase, Shade
from src.core.confidence import confidence_from_delta_e


class BirlaOpusMatcher:
    def __init__(self, db: ShadeDatabase):
        self.db = db

    def _match_lab_topk(self, lab: np.ndarray, top_k: int) -> list[tuple[Shade, float]]:
        scored: list[tuple[Shade, float]] = []

        for shade in self.db.shades:
            de = ciede2000(lab, shade.lab)
            scored.append((shade, de))

        scored.sort(key=lambda x: x[1])
        return scored[:top_k]

    def match_rgb(self, rgb: tuple[int, int, int], top_k: int = 5) -> dict:
        r, g, b = rgb
        lab = np.array(rgb_to_lab(r, g, b), dtype=np.float64)

        if not self.db.shades:
            raise RuntimeError("Shade database is empty.")

        top_k = max(1, min(int(top_k), 20))  # safety cap
        best_list = self._match_lab_topk(lab, top_k=top_k)

        matches = []
        for shade, de in best_list:
            matches.append(
                {
                    "shade_id": shade.shade_id,
                    "shade_name": shade.shade_name,
                    "rgb": {"r": shade.rgb[0], "g": shade.rgb[1], "b": shade.rgb[2]},
                    "delta_e_2000": float(de),
                    "confidence": float(confidence_from_delta_e(de)),
                    "shade_url": shade.shade_url,
                }
            )

        return {
            "input_rgb": {"r": r, "g": g, "b": b},
            "input_lab": {"L": float(lab[0]), "a": float(lab[1]), "b": float(lab[2])},
            "best_match": matches[0],
            "top_matches": matches,
        }

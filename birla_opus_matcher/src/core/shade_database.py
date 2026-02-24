from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import pandas as pd
import numpy as np


@dataclass(frozen=True)
class Shade:
    shade_id: str
    shade_name: str
    rgb: tuple[int, int, int]
    lab: np.ndarray
    shade_url: str | None = None


class ShadeDatabase:
    def __init__(self, csv_path: Path):
        self.csv_path = csv_path
        self._shades: list[Shade] = []

    def load(self) -> None:
        if not self.csv_path.exists():
            raise FileNotFoundError(f"Shade LAB CSV not found: {self.csv_path}")

        df = pd.read_csv(self.csv_path)

        required = {"shade_id", "shade_name", "R", "G", "B", "L", "a", "b"}
        missing = required - set(df.columns)
        if missing:
            raise ValueError(f"Missing columns in LAB dataset: {sorted(missing)}")

        shades: list[Shade] = []
        for _, row in df.iterrows():
            shades.append(
                Shade(
                    shade_id=str(row["shade_id"]),
                    shade_name=str(row["shade_name"]),
                    rgb=(int(row["R"]), int(row["G"]), int(row["B"])),
                    lab=np.array([float(row["L"]), float(row["a"]), float(row["b"])], dtype=np.float64),
                    shade_url=str(row["shade_url"]) if "shade_url" in df.columns else None,
                )
            )

        self._shades = shades

    @property
    def shades(self) -> list[Shade]:
        return self._shades

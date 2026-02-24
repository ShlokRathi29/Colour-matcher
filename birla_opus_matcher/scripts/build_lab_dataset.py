from __future__ import annotations

import pandas as pd
import numpy as np
from pathlib import Path

from config import AppConfig
from src.core.color_math import rgb_to_lab


def main() -> None:
    cfg = AppConfig()
    in_path: Path = cfg.raw_shades_csv
    out_path: Path = cfg.shades_lab_csv

    if not in_path.exists():
        raise FileNotFoundError(f"Raw dataset not found: {in_path}")

    df = pd.read_csv(in_path)

    required_cols = {"shade_id", "shade_name", "R", "G", "B"}
    missing = required_cols - set(df.columns)
    if missing:
        raise ValueError(f"Missing required cols in dataset: {sorted(missing)}")

    labs = []
    for r, g, b in df[["R", "G", "B"]].to_numpy():
        lab = rgb_to_lab(int(r), int(g), int(b))
        labs.append(lab)

    labs = np.array(labs, dtype=np.float64)
    df["L"] = labs[:, 0]
    df["a"] = labs[:, 1]
    df["b"] = labs[:, 2]

    df.to_csv(out_path, index=False, encoding="utf-8")
    print(f"Saved LAB dataset: {out_path} ({len(df)} rows)")


if __name__ == "__main__":
    main()

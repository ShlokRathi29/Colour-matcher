from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class AppConfig:
    base_dir: Path = Path(__file__).resolve().parent
    data_dir: Path = base_dir / "data"
    raw_shades_csv: Path = data_dir / "birla_opus_shades_full.csv"
    shades_lab_csv: Path = data_dir / "birla_opus_shades_lab.csv"

    max_upload_mb: int = 10

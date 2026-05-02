from dataclasses import dataclass
from pathlib import Path

import yaml

ROOT_DIR = Path(__file__).parent.parent.parent
CONFIG_PATH = ROOT_DIR / "config.yaml"


@dataclass
class Config:
    map: str


def load_config(path: Path = CONFIG_PATH) -> Config:
    with open(path, "r") as f:
        data = yaml.safe_load(f)

    try:
        return Config(**data)
    except TypeError as e:
        raise ValueError(f"Invalid config format: {e}")

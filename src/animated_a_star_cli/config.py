from dataclasses import dataclass
from pathlib import Path

import yaml

ROOT_DIR = Path(__file__).parent.parent.parent
CONFIG_PATH = ROOT_DIR / "config.yaml"


@dataclass
class Config:
    map: str


class ConfigError(Exception):
    pass


def load_config(path: Path = CONFIG_PATH) -> Config:
    with open(path, "r") as f:
        content = f.read()

    if not content.strip():
        raise ConfigError("config file is empty")

    data = yaml.safe_load(content)

    if not isinstance(data, dict):
        raise ConfigError("invalid config format")

    try:
        return Config(**data)
    except TypeError:
        raise ConfigError("missing required config fields")

from pathlib import Path

import numpy as np
import yaml

from animated_a_star_cli.core.config import Config
from animated_a_star_cli.core.map import Map

ROOT_DIR = Path(__file__).parent.parent.parent.parent
CONFIG_PATH = ROOT_DIR / "config.yaml"


class ParserError(Exception):
    pass


def load_config(path: Path = CONFIG_PATH) -> Config:
    with open(path, "r") as f:
        content = f.read()

    if not content.strip():
        raise ParserError("config file is empty")

    data = yaml.safe_load(content)

    if not isinstance(data, dict):
        raise ParserError("invalid config format. expected a dictionary")

    return _parse_config(data)


def _parse_config(data: dict) -> Config:
    if "map" not in data:
        raise ParserError("missing required 'map' field in config")

    map, source, dest = _parse_map(data["map"])
    return Config(map=map, source=source, dest=dest)


def _parse_map(map_str: str) -> tuple[Map, tuple[int, int], tuple[int, int]]:
    map_array, source, dest = _check_valid_map(map_str)
    clean_map = map_array.copy()
    clean_map[(clean_map == "o") | (clean_map == "x")] = " "
    return Map(clean_map), source, dest


def _check_valid_map(
    map_str: str,
) -> tuple[np.ndarray, tuple[int, int], tuple[int, int]]:
    if not map_str.strip():
        raise ParserError("map string is empty")

    map_lines = [list(row) for row in map_str.splitlines()]

    if any(len(row) != len(map_lines[0]) for row in map_lines):
        raise ParserError("map must be rectangular")

    map_array = np.array(map_lines)

    if map_array.ndim != 2:
        raise ParserError("map string must be 2D")

    if map_array.shape[0] < 3 or map_array.shape[1] < 3:
        raise ParserError("map must be at least 3x3")

    if not np.isin(map_array, [" ", "#", "o", "x"]).all():
        raise ParserError("map contains invalid characters")

    if np.sum(map_array == "o") != 1:
        raise ParserError("map must contain exactly one source 'o'")

    if np.sum(map_array == "x") != 1:
        raise ParserError("map must contain exactly one destination 'x'")

    source = np.argwhere(map_array == "o")[0]
    dest = np.argwhere(map_array == "x")[0]

    return map_array, tuple(source), tuple(dest)

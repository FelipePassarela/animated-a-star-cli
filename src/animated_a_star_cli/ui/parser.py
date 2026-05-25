from pathlib import Path

import numpy as np
import yaml

from animated_a_star_cli import ROOT_DIR
from animated_a_star_cli.core.config import Config
from animated_a_star_cli.core.heuristic import euclidean, manhattan
from animated_a_star_cli.core.map import Map
from animated_a_star_cli.ui.render.theme import THEMES

CONFIG_PATH = ROOT_DIR / "config.yaml"


class ParserError(Exception):
    pass


def load_config(path: Path = CONFIG_PATH) -> Config:
    with open(path, "r") as f:
        content = f.read()

    if not content.strip():
        raise ParserError("config file is empty")

    try:
        data = yaml.safe_load(content)
    except yaml.YAMLError:
        raise ParserError("invalid YAML format.")

    if not isinstance(data, dict):
        raise ParserError("invalid config format. expected a dictionary")

    return _parse_config(data)


def _parse_config(data: dict) -> Config:
    for field in ["map", "heuristic", "delay", "theme"]:
        if field not in data:
            raise ParserError(f"missing required '{field}' field in config")

    map, source, dest = _parse_map(data["map"])
    delay = _check_valid_delay(data["delay"])

    match data["heuristic"]:
        case "euclidean":
            data["heuristic"] = euclidean
        case "manhattan":
            data["heuristic"] = manhattan
        case _:
            raise ParserError(f"unsupported heuristic '{data['heuristic']}'")

    theme = THEMES.get(data["theme"].lower())
    if theme is None:
        supported_themes = ", ".join(THEMES.keys())
        raise ParserError(
            f"unsupported theme '{data['theme']}'. Supported themes: {supported_themes}"
        )

    return Config(
        map=map,
        source=source,
        dest=dest,
        delay=delay,
        heuristic=data["heuristic"],
        theme=theme,
    )


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


def _check_valid_delay(delay: int | str) -> int:
    if not isinstance(delay, int):
        raise ParserError("delay must be an integer")
    if delay < 0:
        raise ParserError("delay must be non-negative")
    return delay

import numpy as np

from animated_a_star_cli.core.map import Map


class ParserError(Exception):
    pass


def parse_map(map_str: str) -> tuple[Map, tuple[int, int], tuple[int, int]]:
    map_array = _check_valid_map(map_str)

    source = np.argwhere(map_array == "o")[0]
    dest = np.argwhere(map_array == "x")[0]
    map_array[(map_array == "o") | (map_array == "x")] = " "

    return Map(map_array), tuple(source), tuple(dest)


def _check_valid_map(map_str: str) -> np.ndarray:
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

    return map_array

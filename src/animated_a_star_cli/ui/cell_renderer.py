_WALL_DRAWING = {
    (False, False, False, False): "─",
    (False, False, False, True): "─",
    (False, False, True, False): "─",
    (False, False, True, True): "─",
    (True, True, False, False): "│",
    (False, True, False, True): "┌",
    (False, True, True, False): "┐",
    (True, False, False, True): "└",
    (True, False, True, False): "┘",
    (True, True, True, False): "┤",
    (True, True, False, True): "├",
    (True, False, True, True): "┴",
    (False, True, True, True): "┬",
    (True, True, True, True): "┼",
    (True, False, False, False): "│",
    (False, True, False, False): "│",
}
_PATH_DRAWING = {
    (False, False, True, True): "═",
    (True, True, False, False): "║",
    (False, True, False, True): "╔",
    (False, True, True, False): "╗",
    (True, False, False, True): "╚",
    (True, False, True, False): "╝",
    # For heads, we only consider the case where there's exactly one neigh is a path,
    # since the other cases are either handled by the body drawing or are invalid.
    (True, False, False, False): "↓",
    (False, True, False, False): "↑",
    (False, False, True, False): "→",
    (False, False, False, True): "←",
}


def glyph_from_neighs(
    center: str,
    up: str | None,
    down: str | None,
    left: str | None,
    right: str | None,
) -> str:
    if center == "#":
        return _from_wall(up, down, left, right)
    elif center == "*":
        return _from_path(up, down, left, right)
    else:
        return center


def _from_wall(
    up: str | None,
    down: str | None,
    left: str | None,
    right: str | None,
) -> str:
    up_is_wall = up == "#"
    down_is_wall = down == "#"
    left_is_wall = left == "#"
    right_is_wall = right == "#"
    return _WALL_DRAWING.get(
        (up_is_wall, down_is_wall, left_is_wall, right_is_wall), "?"
    )


def _from_path(
    up: str | None,
    down: str | None,
    left: str | None,
    right: str | None,
) -> str:
    up_is_path = up == "*"
    down_is_path = down == "*"
    left_is_path = left == "*"
    right_is_path = right == "*"
    return _PATH_DRAWING.get(
        (up_is_path, down_is_path, left_is_path, right_is_path), "?"
    )

from collections.abc import Callable

import numpy as np

from animated_a_star_cli.core.heuristic import euclidean, manhattan
from animated_a_star_cli.core.map import Map
from animated_a_star_cli.ui.render_context import RenderContext


def draw(ctx: RenderContext):
    print(draw_to_string(ctx))


def draw_to_string(ctx: RenderContext) -> str:
    config = ctx.cfg
    map_grid = _formatted_map(config.map)

    closed = ctx.astar_state.closed_cells
    path = ctx.astar_state.path
    if closed:
        rows, cols = zip(*closed)
        map_grid[rows, cols] = "."
    _draw_path(path, map_grid)

    map_grid[config.source] = "o"
    map_grid[config.dest] = "x"

    sprite = "\n".join("".join(row) for row in map_grid) + "\n"
    sprite += _formatted_steps(ctx.astar_state.current_step)
    sprite += " " + _formatted_heuristic(config.heuristic)

    return sprite


def _draw_path(path: list[tuple[int, int]], canva: np.ndarray):
    PATH_DRAWING = {
        (False, False, True, True): "═",
        (True, True, False, False): "║",
        (False, True, False, True): "╔",
        (False, True, True, False): "╗",
        (True, False, False, True): "╚",
        (True, False, True, False): "╝",
    }
    ARROW_DRAWING = {
        (-1, 0): "↑",
        (1, 0): "↓",
        (0, -1): "←",
        (0, 1): "→",
    }

    path_cells = set(path)

    for row, col in path_cells:
        up = (row - 1, col) in path_cells
        down = (row + 1, col) in path_cells
        left = (row, col - 1) in path_cells
        right = (row, col + 1) in path_cells

        canva[row, col] = PATH_DRAWING.get((up, down, left, right), "?")

    # Head should be an arrow pointing to forward direction
    if len(path) >= 2:
        head = path[-1]
        tail = path[-2]

        dr = head[0] - tail[0]
        dc = head[1] - tail[1]
        canva[head] = ARROW_DRAWING.get((dr, dc), "?")


def _formatted_map(map: Map) -> np.ndarray:
    WALL_DRAWING = {
        (False, False, True, True): "═",
        (True, True, False, False): "║",
        (False, True, False, True): "╔",
        (False, True, True, False): "╗",
        (True, False, False, True): "╚",
        (True, False, True, False): "╝",
        (True, True, True, False): "╣",
        (True, True, False, True): "╠",
        (True, False, True, True): "╩",
        (False, True, True, True): "╦",
        (True, True, True, True): "╬",
        (False, False, False, True): "═",
        (False, False, True, False): "═",
        (True, False, False, False): "║",
        (False, True, False, False): "║",
    }

    rows, cols = map.grid.shape
    render = np.full((rows, cols), " ", dtype="<U1")

    for row in range(rows):
        for col in range(cols):
            if map.at(row, col) != "#":
                render[row, col] = map.at(row, col)
                continue

            up = map.is_wall(row - 1, col)
            down = map.is_wall(row + 1, col)
            left = map.is_wall(row, col - 1)
            right = map.is_wall(row, col + 1)

            render[row, col] = WALL_DRAWING.get((up, down, left, right), "?")

    return render


def _formatted_heuristic(h: Callable) -> str:
    if h is euclidean:
        return "Heuristic: Euclidean"
    elif h is manhattan:
        return "Heuristic: Manhattan"
    return "Heuristic: Unknown"


def _formatted_steps(current_step: int) -> str:
    return f"Steps: {current_step}"

from collections.abc import Callable

import numpy as np

from animated_a_star_cli.core.heuristic import euclidean, manhattan
from animated_a_star_cli.ui.cell_renderer import glyph_from_neighs
from animated_a_star_cli.ui.render_context import RenderContext


def draw(ctx: RenderContext):
    print(draw_to_string(ctx))


def draw_to_string(ctx: RenderContext) -> str:
    config = ctx.cfg
    filled_map = _filled_map(ctx)
    formatted_map = _renderable_map(filled_map)

    sprite = "\n".join("".join(row) for row in formatted_map) + "\n"
    sprite += _formatted_steps(ctx.astar_state.current_step)
    sprite += " " + _formatted_heuristic(config.heuristic)

    return sprite


def _renderable_map(filled_map: np.ndarray) -> np.ndarray:
    formatted_map = np.array(filled_map, dtype=str)

    rows, cols = filled_map.shape
    for i in range(rows):
        for j in range(cols):
            center = filled_map[i, j]

            up = filled_map[i - 1, j] if i > 0 else None
            down = filled_map[i + 1, j] if i < rows - 1 else None
            left = filled_map[i, j - 1] if j > 0 else None
            right = filled_map[i, j + 1] if j < cols - 1 else None

            glyph = glyph_from_neighs(center, up, down, left, right)
            formatted_map[i, j] = glyph

    return formatted_map


def _filled_map(ctx: RenderContext) -> np.ndarray:
    config = ctx.cfg
    map_grid = np.array(config.map.grid, dtype=str)

    closed = ctx.astar_state.closed_cells
    path = ctx.astar_state.path
    if closed:
        rows, cols = zip(*closed)
        map_grid[rows, cols] = "."
    if path:
        rows, cols = zip(*path)
        map_grid[rows, cols] = "*"

    map_grid[config.source] = "o"
    map_grid[config.dest] = "x"

    return map_grid


def _formatted_heuristic(h: Callable) -> str:
    if h is euclidean:
        return "Heuristic: Euclidean"
    elif h is manhattan:
        return "Heuristic: Manhattan"
    return "Heuristic: Unknown"


def _formatted_steps(current_step: int) -> str:
    return f"Steps: {current_step}"

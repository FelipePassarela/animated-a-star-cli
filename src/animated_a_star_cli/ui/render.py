from collections.abc import Callable

from animated_a_star_cli.core.heuristic import euclidean, manhattan
from animated_a_star_cli.ui.render_context import RenderContext


def draw(ctx: RenderContext):
    print(draw_to_string(ctx))


def draw_to_string(ctx: RenderContext) -> str:
    config = ctx.cfg
    map_grid = config.map.grid.copy()

    if ctx.astar_state is not None:
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

    sprite = "\n".join("".join(row) for row in map_grid) + "\n"
    if ctx.astar_state is not None:
        sprite += _formatted_steps(ctx.astar_state.current_step)
        sprite += " " + _formatted_heuristic(config.heuristic)

    return sprite


def _formatted_heuristic(h: Callable) -> str:
    if h is euclidean:
        return "Heuristic: Euclidean"
    elif h is manhattan:
        return "Heuristic: Manhattan"
    return "Heuristic: Unknown"


def _formatted_steps(current_step: int) -> str:
    return f"Steps: {current_step}"

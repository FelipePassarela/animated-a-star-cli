from collections.abc import Callable

from animated_a_star_cli.core.heuristic import euclidean, manhattan
from animated_a_star_cli.ui.render_context import RenderContext


def draw(ctx: RenderContext):
    config = ctx.cfg
    grid = config.map.grid.copy()

    if ctx.astar_state is not None:
        closed = ctx.astar_state.closed_cells
        path = ctx.astar_state.path
        if closed:
            rows, cols = zip(*closed)
            grid[rows, cols] = "."
        if path:
            rows, cols = zip(*path)
            grid[rows, cols] = "*"

    grid[config.source] = "o"
    grid[config.dest] = "x"

    sprite = "\n".join("".join(row) for row in grid) + "\n"
    sprite += _heuristic_to_string(config.heuristic)

    print(sprite)


def _heuristic_to_string(h: Callable) -> str:
    if h is euclidean:
        return "Heuristic: Euclidean"
    elif h is manhattan:
        return "Heuristic: Manhattan"
    return "Heuristic: Unknown"

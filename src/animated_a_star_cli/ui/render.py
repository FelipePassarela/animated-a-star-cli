from animated_a_star_cli.ui.render_context import RenderContext


def draw(ctx: RenderContext):
    config = ctx.cfg

    grid = config.map.grid
    grid[config.source] = "o"
    grid[config.dest] = "x"

    sprite = "\n".join("".join(row) for row in grid) + "\n"
    print(sprite)

from animated_a_star_cli.ui.render_context import RenderContext


def draw(ctx: RenderContext):
    grid = ctx.map.grid
    grid[ctx.src] = "o"
    grid[ctx.dst] = "x"
    sprite = "\n".join("".join(row) for row in grid) + "\n"
    print(sprite)

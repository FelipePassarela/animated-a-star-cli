import pytest

from animated_a_star_cli.core.config import Config
from animated_a_star_cli.core.map import Map
from animated_a_star_cli.ui.render import draw
from animated_a_star_cli.ui.render_context import RenderContext


def test_draw_renders_map_with_source_and_destination(
    capsys: pytest.CaptureFixture[str],
):
    grid = [
        ["#", "#", "#", "#", "#"],
        ["#", " ", " ", " ", "#"],
        ["#", " ", "#", " ", "#"],
        ["#", "#", "#", "#", "#"],
    ]

    map_obj = Map(grid)
    config = Config(map=map_obj, source=(1, 1), dest=(2, 3))
    ctx = RenderContext(cfg=config)

    draw(ctx)

    captured = capsys.readouterr()
    expected = (
        "#####\n"
        "#o  #\n"
        "# #x#\n"
        "#####\n"
        "\n"  # print() adds an extra newline
    )
    assert captured.out == expected

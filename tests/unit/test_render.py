import textwrap

import pytest

from animated_a_star_cli.core.astar_state import AStarState
from animated_a_star_cli.core.config import Config
from animated_a_star_cli.core.map import Map
from animated_a_star_cli.ui.render import draw
from animated_a_star_cli.ui.render_context import RenderContext

grid = [
    "######",
    "#o   #",
    "###  #",
    "#x ###",
    "######",
]


@pytest.fixture
def render_ctx():
    map_obj = Map(grid)
    config = Config(map=map_obj, source=(1, 1), dest=(3, 1))
    return RenderContext(cfg=config)


def test_draw_renders_map_with_source_and_destination(
    capsys: pytest.CaptureFixture[str], render_ctx: RenderContext
):
    draw(render_ctx)

    captured = capsys.readouterr()
    expected = textwrap.dedent("""\
        ######
        #o   #
        ###  #
        #x ###
        ######
    """)
    assert captured.out == expected


def test_draw_renders_closed_cells(
    capsys: pytest.CaptureFixture[str], render_ctx: RenderContext
):
    render_ctx.astar_state = AStarState(closed_cells={(1, 4), (2, 3)})
    draw(render_ctx)

    captured = capsys.readouterr()
    expected = textwrap.dedent("""\
        ######
        #o  .#
        ###. #
        #x ###
        ######
    """)
    assert captured.out == expected


def test_draw_renders_path(
    capsys: pytest.CaptureFixture[str], render_ctx: RenderContext
):
    render_ctx.astar_state = AStarState(path=[(1, 2), (1, 3), (2, 3), (3, 2)])

    draw(render_ctx)

    captured = capsys.readouterr()
    expected = textwrap.dedent("""\
        ######
        #o** #
        ###* #
        #x*###
        ######
    """)
    assert captured.out == expected


def test_path_cells_take_precedence_over_closed_cells(
    capsys: pytest.CaptureFixture[str], render_ctx: RenderContext
):
    render_ctx.astar_state = AStarState(
        closed_cells={(1, 2), (1, 3), (2, 3)},
        path=[(1, 2), (1, 3), (2, 3)],
    )

    draw(render_ctx)

    captured = capsys.readouterr()
    expected = textwrap.dedent("""\
        ######
        #o** #
        ###* #
        #x ###
        ######
    """)
    assert captured.out == expected


def test_source_and_dest_dont_get_overriden(
    capsys: pytest.CaptureFixture[str], render_ctx: RenderContext
):
    render_ctx.cfg.source = (1, 1)
    render_ctx.cfg.dest = (3, 1)
    render_ctx.astar_state = AStarState(
        closed_cells={(1, 1), (3, 1)},
        path=[(1, 1), (3, 1)],
    )

    draw(render_ctx)

    captured = capsys.readouterr()
    expected = textwrap.dedent("""\
        ######
        #o   #
        ###  #
        #x ###
        ######
    """)
    assert captured.out == expected


def test_draw_succeeds_with_none_astar_state(
    capsys: pytest.CaptureFixture[str], render_ctx: RenderContext
):
    render_ctx.astar_state = None
    draw(render_ctx)

    captured = capsys.readouterr()
    expected = textwrap.dedent("""\
        ######
        #o   #
        ###  #
        #x ###
        ######
    """)
    assert captured.out == expected

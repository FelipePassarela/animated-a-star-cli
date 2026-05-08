import textwrap
from collections.abc import Callable

import pytest

from animated_a_star_cli.core.astar_state import AStarState
from animated_a_star_cli.core.config import Config
from animated_a_star_cli.core.heuristic import euclidean, manhattan
from animated_a_star_cli.core.map import Map
from animated_a_star_cli.ui.render import draw_to_string
from animated_a_star_cli.ui.render_context import RenderContext

grid = [
    "######",
    "#o   #",
    "###  #",
    "#x ###",
    "######",
]

BASE_MAP_OUTPUT = textwrap.dedent("""\
    ######
    #o   #
    ###  #
    #x ###
    ######""")


def draw_and_assert(
    render_ctx: RenderContext,
    *,
    expected_map_output: str = BASE_MAP_OUTPUT,
    expected_heuristic: str = "Euclidean",
):
    output = draw_to_string(render_ctx)

    expected = f"{expected_map_output}\n"
    if render_ctx.astar_state is not None:
        expected += f"Steps: {render_ctx.astar_state.current_step}"
        expected += f" Heuristic: {expected_heuristic}"

    assert output == expected


@pytest.fixture
def render_ctx() -> RenderContext:
    map_obj = Map(grid)
    config = Config(
        map=map_obj, source=(1, 1), dest=(3, 1), heuristic=euclidean, delay=32
    )
    return RenderContext(cfg=config)


class TestStaticRendering:
    @staticmethod
    def test_draw_renders_map_with_source_and_destination(render_ctx: RenderContext):
        draw_and_assert(render_ctx)

    @pytest.mark.parametrize(
        "heuristic, expected_heuristic",
        [
            (euclidean, "Euclidean"),
            (manhattan, "Manhattan"),
            (lambda x, y: 0, "Unknown"),
        ],
    )
    @staticmethod
    def test_draw_renders_correct_heuristic_name(
        render_ctx: RenderContext,
        heuristic: Callable,
        expected_heuristic: str,
    ):
        render_ctx.cfg.heuristic = heuristic
        draw_and_assert(render_ctx, expected_heuristic=expected_heuristic)


class TestPathRendering:
    EXPECTED_PATH_OUTPUT = textwrap.dedent("""\
        ######
        #o** #
        ###* #
        #x*###
        ######""")
    EXPECTED_CLOSEDS_CELLS_OUTPUT = textwrap.dedent("""\
        ######
        #o  .#
        ###. #
        #x ###
        ######""")
    PATH_CELLS = [(1, 2), (1, 3), (2, 3), (3, 2)]

    def test_draw_renders_path(self, render_ctx: RenderContext):
        render_ctx.astar_state = AStarState(path=self.PATH_CELLS)
        draw_and_assert(render_ctx, expected_map_output=self.EXPECTED_PATH_OUTPUT)

    def test_draw_renders_closed_cells(self, render_ctx: RenderContext):
        render_ctx.astar_state = AStarState(closed_cells={(1, 4), (2, 3)})
        draw_and_assert(
            render_ctx, expected_map_output=self.EXPECTED_CLOSEDS_CELLS_OUTPUT
        )

    def test_path_cells_take_precedence_over_closed_cells(
        self, render_ctx: RenderContext
    ):
        render_ctx.astar_state = AStarState(
            closed_cells=set(self.PATH_CELLS),
            path=self.PATH_CELLS,
        )
        draw_and_assert(render_ctx, expected_map_output=self.EXPECTED_PATH_OUTPUT)

    def test_source_and_dest_dont_get_overriden(self, render_ctx: RenderContext):
        render_ctx.cfg.source = (1, 1)
        render_ctx.cfg.dest = (3, 1)
        render_ctx.astar_state = AStarState(
            closed_cells={(1, 1), (3, 1)},
            path=[(1, 1), (3, 1)],
        )
        draw_and_assert(render_ctx)


class TestEdgeCases:
    @staticmethod
    def test_draw_succeeds_with_none_astar_state(render_ctx: RenderContext):
        render_ctx.astar_state = None
        draw_and_assert(render_ctx)

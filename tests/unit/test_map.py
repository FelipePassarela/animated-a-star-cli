import textwrap

from animated_a_star_cli.core.map import Map

grid = [
    "####",
    "#  #",
    "## #",
    "####",
]


def test_str_serializes_successfully():
    expected_str = textwrap.dedent("""\
        ####
        #  #
        ## #
        ####""")
    m = Map(grid)
    assert str(m) == expected_str


def test_grid_returns_deep_copy():
    map = Map(grid)
    assert map.grid is not map._grid

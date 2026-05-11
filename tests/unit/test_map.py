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


def test_grid_returns_shallow_copy():
    map = Map(grid)
    assert map.grid is map._grid


def test_is_wall_returns_true_for_wall():
    map = Map(grid)
    assert map.is_wall(0, 0) is True


def test_is_wall_returns_false_for_non_wall():
    map = Map(grid)
    assert map.is_wall(1, 1) is False

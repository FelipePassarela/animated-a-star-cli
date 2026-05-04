import math

import pytest

from animated_a_star_cli.core.astar_algo import AStarAlgo
from animated_a_star_cli.core.astar_state import AStarState
from animated_a_star_cli.core.config import Config
from animated_a_star_cli.core.map import Map


@pytest.fixture()
def astar() -> AStarAlgo:
    grid = [
        "#####",
        "#o  #",
        "### #",
        "#x  #",
        "#####",
    ]
    map = Map(grid)
    config = Config(map=map, source=(1, 1), dest=(3, 1))
    return AStarAlgo(config)


@pytest.fixture()
def astar_no_path() -> AStarAlgo:
    """Grid where the destination is completely walled off."""
    grid = [
        "#####",
        "#o###",
        "#####",
        "###x#",
        "#####",
    ]
    map = Map(grid)
    config = Config(map=map, source=(1, 1), dest=(3, 3))
    return AStarAlgo(config)


@pytest.fixture()
def astar_single_cell() -> AStarAlgo:
    grid = [
        "###",
        "#o#",
        "###",
    ]
    map = Map(grid)
    config = Config(map=map, source=(1, 1), dest=(1, 1))
    astar = AStarAlgo(config)
    return astar


def run_astar(astar: AStarAlgo) -> AStarState:
    for _ in range(100):
        state = astar.step()
        if astar.finished:
            break
    return state


def test_finds_path_from_source_to_dest(astar: AStarAlgo):
    state = run_astar(astar)

    expected_path = [(1, 1), (1, 2), (1, 3), (2, 3), (3, 3), (3, 2), (3, 1)]

    assert astar.finished, "algorithm should have finished"
    assert state.path[0] == astar._source
    assert state.path[-1] == astar._dest
    assert state.path == expected_path


def test_path_properties(astar: AStarAlgo):
    state = run_astar(astar)

    for (i1, j1), (i2, j2) in zip(state.path, state.path[1:]):
        dist = math.sqrt((i2 - i1) ** 2 + (j2 - j1) ** 2)

        assert math.isclose(dist, 1.0), "path should only contain adjacent cells"
        assert astar.map.at(i2, j2) != "#", "path should not contain walls"


def test_no_path_finishes_gracefully_without_path(astar_no_path: AStarAlgo):
    """When no path exists the algorithm should terminate gracefully."""
    state = run_astar(astar_no_path)
    assert astar_no_path.finished
    assert state.path == [(1, 1)], (
        "when no path exists, the path should only contain the source cell"
    )


def test_step_after_finished_is_idempotent(astar: AStarAlgo):
    run_astar(astar)

    state_a = astar.step()
    state_b = astar.step()
    assert state_a.path == state_b.path


def test_step_returns_single_cell_path_when_source_equals_dest(
    astar_single_cell: AStarAlgo,
):
    state = astar_single_cell.step()
    assert state.path == [(1, 1)]

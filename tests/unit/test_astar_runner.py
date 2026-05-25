import math
import time

import pytest

from animated_a_star_cli.core.astar_runner import AStarRunner
from animated_a_star_cli.core.config import Config
from animated_a_star_cli.core.heuristic import euclidean
from animated_a_star_cli.core.map import Map
from animated_a_star_cli.ui.render import DEFAULT_THEME


@pytest.fixture()
def runner() -> AStarRunner:
    grid = [
        "#####",
        "#o  #",
        "### #",
        "#x  #",
        "#####",
    ]
    map = Map(grid)
    config = Config(
        map=map,
        source=(1, 1),
        dest=(3, 1),
        heuristic=euclidean,
        delay=32,
        theme=DEFAULT_THEME,
    )
    return AStarRunner(config)


def test_step_sleeps_for_configured_delay(runner: AStarRunner):
    start_time = time.time()
    runner.step()
    elapsed_time = time.time() - start_time
    expected = runner.delay / 1000
    assert math.isclose(elapsed_time, expected, rel_tol=0.05)

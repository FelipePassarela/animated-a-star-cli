import time

from animated_a_star_cli.core.astar_algo import AStarAlgo
from animated_a_star_cli.core.astar_state import AStarState
from animated_a_star_cli.core.config import Config


class AStarRunner:
    def __init__(self, config: Config):
        self._algo = AStarAlgo(config)
        self.delay = config.delay
        self._prev_time = time.perf_counter()

    def step(self) -> AStarState:
        now = time.perf_counter()
        dt = (now - self._prev_time) / 1000
        time.sleep(dt)
        self._prev_time = now

        return self._algo.step()

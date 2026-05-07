import time

from animated_a_star_cli.core.astar_algo import AStarAlgo
from animated_a_star_cli.core.astar_state import AStarState
from animated_a_star_cli.core.config import Config


class AStarRunner:
    def __init__(self, config: Config):
        self._algo = AStarAlgo(config)
        self.delay = config.delay

    def step(self) -> AStarState:
        time.sleep(self.delay / 1000)
        return self._algo.step()

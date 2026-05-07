from animated_a_star_cli.core.astar_algo import AStarAlgo
from animated_a_star_cli.core.astar_state import AStarState
from animated_a_star_cli.core.config import Config


class AStarRunner:
    def __init__(self, config: Config):
        self._algo = AStarAlgo(config)

    def step(self) -> AStarState:
        return self._algo.step()

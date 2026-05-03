from dataclasses import dataclass

from animated_a_star_cli.core.astar_state import AStarState
from animated_a_star_cli.core.config import Config


@dataclass
class RenderContext:
    cfg: Config
    astar_state: AStarState | None = None

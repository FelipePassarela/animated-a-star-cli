from dataclasses import dataclass, field

from animated_a_star_cli.core.astar_state import AStarState
from animated_a_star_cli.core.config import Config
from animated_a_star_cli.ui.theme import DEFAULT_THEME, Theme


@dataclass
class RenderContext:
    cfg: Config
    astar_state: AStarState
    theme: Theme | None = field(default_factory=lambda: DEFAULT_THEME)

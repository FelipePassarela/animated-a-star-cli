from dataclasses import dataclass, field
from typing import Callable

from animated_a_star_cli.core.astar_state import AStarState
from animated_a_star_cli.core.map import Map

from .theme import DEFAULT_THEME, Theme


@dataclass
class RenderContext:
    map: Map
    heuristic: Callable[[tuple[int, int], tuple[int, int]], float]
    astar_state: AStarState
    source: tuple[int, int]
    dest: tuple[int, int]
    theme: Theme | None = field(default_factory=lambda: DEFAULT_THEME)

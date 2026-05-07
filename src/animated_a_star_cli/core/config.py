from dataclasses import dataclass
from typing import Callable

from animated_a_star_cli.core.map import Map


@dataclass
class Config:
    map: Map
    source: tuple[int, int]
    dest: tuple[int, int]
    delay: int  # milliseconds
    heuristic: Callable[[tuple[int, int], tuple[int, int]], float]

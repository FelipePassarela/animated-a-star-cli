from dataclasses import dataclass
from typing import Callable

from animated_a_star_cli.core.heuristic import euclidean
from animated_a_star_cli.core.map import Map


@dataclass
class Config:
    map: Map
    source: tuple[int, int]
    dest: tuple[int, int]
    heuristic: Callable[[tuple[int, int], tuple[int, int]], float] = euclidean

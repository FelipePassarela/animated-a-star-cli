from dataclasses import dataclass

from animated_a_star_cli.core.map import Map


@dataclass
class Config:
    map: Map
    source: tuple[int, int]
    dest: tuple[int, int]

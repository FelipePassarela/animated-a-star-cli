from dataclasses import dataclass

from animated_a_star_cli.core.map import Map


@dataclass
class RenderContext:
    map: Map
    src: tuple[int, int]
    dst: tuple[int, int]

from dataclasses import dataclass, field


@dataclass
class AStarState:
    open_cells: list[tuple[int, int]] = field(default_factory=list)
    closed_cells: set[tuple[int, int]] = field(default_factory=set)
    path: list[tuple[int, int]] = field(default_factory=list)

from typing import Iterable

import numpy as np


class Map:
    def __init__(self, grid: Iterable[Iterable[str]]):
        self._grid = np.array(grid)

    def __str__(self):
        return "\n".join("".join(row) for row in self._grid)

    def at(self, i, j):
        return self._grid[i, j]

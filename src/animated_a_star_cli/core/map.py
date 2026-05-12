from typing import Iterable

import numpy as np


class Map:
    def __init__(self, grid: Iterable[Iterable[str]]):
        is_list_of_strings = all(isinstance(row, str) for row in grid)
        if is_list_of_strings:
            self._grid = np.array([list(s) for s in grid])
        else:
            self._grid = np.array(grid)

    def __str__(self):
        return "\n".join("".join(row) for row in self._grid)

    def at(self, i, j):
        return self._grid[i, j]

    @property
    def grid(self):
        return self._grid.copy()

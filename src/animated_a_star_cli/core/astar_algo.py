import heapq
from typing import Generator

import numpy as np

from animated_a_star_cli.core.astar_state import AStarState
from animated_a_star_cli.core.config import Config


class AStarAlgo:
    def __init__(self, config: Config):
        self._state = AStarState()
        self.map = config.map

        self._opens = self._state.open_cells
        self._closeds = self._state.closed_cells

        self._source = config.source
        self._dest = config.dest
        self._current: tuple[int, int] = self._source

        grid = self.map.grid

        self._g = np.full_like(grid, np.inf, dtype=np.float64)
        self._f = np.full_like(grid, np.inf, dtype=np.float64)
        self._h = config.heuristic
        self._parents = np.full((*grid.shape, 2), -1)

        self._g[self._source] = 0.0
        self._f[self._source] = self._h(self._source, self._dest)
        source_cost = (self._f[self._source], *self._source)
        heapq.heappush(self._opens, source_cost)

    def step(self) -> AStarState:
        if self._state.finished:
            return self._build_path(self._current)

        if not self._opens:
            self._state.finished = True
            return self._state

        _, i, j = heapq.heappop(self._opens)
        cell = (i, j)

        if cell in self._closeds:  # Skip if already visited with better cost
            return self._state

        self._current = cell
        self._closeds.add(self._current)

        if self._current == self._dest:
            self._state.finished = True
            return self._build_path(self._current)

        for neigh in self._neighbours(self._current):
            self._update_costs(neigh)
            neigh_cost = (self._f[neigh], *neigh)
            heapq.heappush(self._opens, neigh_cost)

        return self._build_path(self._current)

    def _update_costs(self, neigh: tuple[int, int]):
        new_g = self._g[self._current] + 1

        if new_g < self._g[neigh]:
            self._g[neigh] = new_g
            self._parents[neigh] = self._current

        self._f[neigh] = self._g[neigh] + self._h(neigh, self._dest)

    def _neighbours(self, cell: tuple[int, int]) -> Generator[tuple[int, int]]:
        adjacent_moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        for dx, dy in adjacent_moves:
            neigh = (cell[0] + dx, cell[1] + dy)
            if not self._walkable(neigh):
                continue
            yield neigh

    def _walkable(self, cell: tuple[int, int]) -> bool:
        map_w = self.map.grid.shape[0]
        map_h = self.map.grid.shape[1]

        return (
            cell[0] >= 0
            and cell[0] < map_w
            and cell[1] >= 0
            and cell[1] < map_h
            and self.map.at(*cell) != "#"
            and cell not in self._state.closed_cells
        )

    def _build_path(self, cell: tuple[int, int]) -> AStarState:
        path = [cell]
        queue = [cell]

        while queue:
            current = queue.pop()
            parent = tuple(self._parents[current].tolist())

            if parent == (-1, -1):
                break

            path.append(parent)
            queue.append(parent)

        path.reverse()
        self._state.path = path
        return self._state

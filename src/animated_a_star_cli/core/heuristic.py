def euclidean(cell1: tuple[int, int], cell2: tuple[int, int]) -> float:
    return ((cell1[0] - cell2[0]) ** 2 + (cell1[1] - cell2[1]) ** 2) ** 0.5


def manhattan(cell1: tuple[int, int], cell2: tuple[int, int]) -> float:
    return abs(cell1[0] - cell2[0]) + abs(cell1[1] - cell2[1])

from animated_a_star_cli.core.heuristic import euclidean, manhattan


def test_manhattan_distance():
    assert manhattan((0, 0), (3, 4)) == 7


def test_euclidean_distance():
    assert euclidean((0, 0), (3, 4)) == 5.0


def test_distance_is_zero_for_same_point():
    assert manhattan((1, 1), (1, 1)) == 0
    assert euclidean((1, 1), (1, 1)) == 0.0

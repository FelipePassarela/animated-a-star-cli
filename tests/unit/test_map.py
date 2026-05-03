from animated_a_star_cli.core.map import Map


def test_str_serializes_successfully():
    grid = [
        "####",
        "#  #",
        "## #",
        "####",
    ]
    # fmt: off
    expected_str = (
        "####\n"
        "#  #\n"
        "## #\n"
        "####"
    )
    # fmt: on
    m = Map(grid)
    assert str(m) == expected_str

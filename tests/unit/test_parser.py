import pytest

from animated_a_star_cli.core.map import Map
from animated_a_star_cli.ui.parser import ParserError, parse_map


def test_parse_map_succeeds_with_valid_str():
    # fmt: off
    map_str = (
        "#####\n"
        "#o  #\n"
        "# #x#\n"
        "#####\n"
    )
    # fmt: on
    parsed_map, src, dst = parse_map(map_str)

    assert isinstance(parsed_map, Map)
    assert isinstance(src, tuple)
    assert isinstance(dst, tuple)
    assert src == (1, 1)
    assert dst == (2, 3)


def test_parse_map_replaces_source_and_destination_with_spaces():
    # fmt: off
    map_str = (
        "#####\n"
        "#o  #\n"
        "# #x#\n"
        "#####\n"
    )
    # fmt: on
    parsed_map, src, dst = parse_map(map_str)

    assert src == (1, 1)
    assert dst == (2, 3)
    assert parsed_map.at(1, 1) == " "
    assert parsed_map.at(2, 3) == " "


# fmt: off
@pytest.mark.parametrize(
    "map_str, expected_error",
    [
        ("", "map string is empty"),
        ("   \n  ", "map string is empty"),
        (
            "###\n"
            "#o##\n",
            "map must be rectangular",
        ),
        (
            "##\n"
            "#o\n"
            "##\n",
            "map must be at least 3x3",
        ),
        (
            "#o#\n"
            "#x#\n",
            "map must be at least 3x3",
        ),
        (
            "###\n"
            "#o#\n"
            "#a#\n",
            "map contains invalid characters",
        ),
        (
            "###\n"
            "#oo\n"
            "#x#\n",
            "map must contain exactly one source 'o'",
        ),
        (
            "###\n"
            "#o#\n"
            "#xx\n",
            "map must contain exactly one destination 'x'",
        ),
        (
            "###\n"
            "# #\n"
            "# #\n",
            "map must contain exactly one source 'o'",
        ),
    ],
)
# fmt: on
def test_parse_map_raises_parser_error(map_str: str, expected_error: str):
    with pytest.raises(ParserError, match=expected_error):
        parse_map(map_str)

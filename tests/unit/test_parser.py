from pathlib import Path

import pytest

from animated_a_star_cli.config import Config
from animated_a_star_cli.core.map import Map
from animated_a_star_cli.ui.parser import (
    ParserError,
    _parse_config,
    _parse_map,
    load_config,
)

# fmt: off
MAP_STR = (
    "#####\n"
    "#o  #\n"
    "# #x#\n"
    "#####\n"
)
# fmt: on


def test_parse_config_succeeds_with_valid_data():
    data = {"map": MAP_STR}
    cfg = _parse_config(data)

    assert isinstance(cfg, Config)
    assert isinstance(cfg.map, Map)
    assert cfg.source == (1, 1)
    assert cfg.dest == (2, 3)


def test_parse_config_fails_with_missing_map_field():
    data = {"wrong_field": "value"}

    with pytest.raises(ParserError, match="missing required 'map' field in config"):
        _parse_config(data)


@pytest.mark.parametrize(
    "config_content, expected_error",
    [
        ("", "config file is empty"),
        ("   \n  ", "config file is empty"),
        ("- just a list\n- not a dict", "invalid config format. expected a dictionary"),
    ],
)
def test_load_config_fails_with_invalid_content(
    tmp_path: Path, config_content: str, expected_error: str
):
    path = tmp_path / "config.yaml"
    path.write_text(config_content)

    with pytest.raises(ParserError, match=expected_error):
        load_config(path)


def test_load_config_fails_with_missing_file(tmp_path: Path):
    path = tmp_path / "nonexistent_config.yaml"

    with pytest.raises(FileNotFoundError):
        load_config(path)


def test_parse_map_succeeds_with_valid_str():
    parsed_map, src, dst = _parse_map(MAP_STR)

    assert isinstance(parsed_map, Map)
    assert isinstance(src, tuple)
    assert isinstance(dst, tuple)
    assert src == (1, 1)
    assert dst == (2, 3)


def test_parse_map_replaces_source_and_destination_with_spaces():
    parsed_map, src, dst = _parse_map(MAP_STR)

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
        _parse_map(map_str)

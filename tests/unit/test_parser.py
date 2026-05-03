import textwrap
from pathlib import Path

import pytest

from animated_a_star_cli.core.config import Config
from animated_a_star_cli.core.map import Map
from animated_a_star_cli.ui.parser import (
    ParserError,
    _parse_config,
    _parse_map,
    load_config,
)

MAP_STR = textwrap.dedent("""\
    #####
    #o  #
    # #x#
    #####
""")


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


@pytest.mark.parametrize(
    "map_str, expected_error",
    [
        ("", "map string is empty"),
        ("   \n  ", "map string is empty"),
        (
            textwrap.dedent("""\
                ###
                #o##
            """),
            "map must be rectangular",
        ),
        (
            textwrap.dedent("""\
                ##
                #o
                ##
            """),
            "map must be at least 3x3",
        ),
        (
            textwrap.dedent("""\
                #o#
                #x#
            """),
            "map must be at least 3x3",
        ),
        (
            textwrap.dedent("""\
                ###
                #o#
                #a#
            """),
            "map contains invalid characters",
        ),
        (
            textwrap.dedent("""\
                ###
                #oo
                #x#
            """),
            "map must contain exactly one source 'o'",
        ),
        (
            textwrap.dedent("""\
                ###
                #o#
                #xx
            """),
            "map must contain exactly one destination 'x'",
        ),
        (
            textwrap.dedent("""\
                ###
                # #
                # #
            """),
            "map must contain exactly one source 'o'",
        ),
    ],
)
# fmt: on
def test_parse_map_raises_parser_error(map_str: str, expected_error: str):
    with pytest.raises(ParserError, match=expected_error):
        _parse_map(map_str)

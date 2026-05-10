import textwrap
from pathlib import Path

import pytest
import yaml

from animated_a_star_cli.core.config import Config
from animated_a_star_cli.core.heuristic import euclidean
from animated_a_star_cli.core.map import Map
from animated_a_star_cli.ui.parser import ParserError, load_config

MAP_STR = textwrap.dedent("""\
    #####
    #o  #
    # #x#
    #####
""")

valid_config_data = {
    "map": MAP_STR,
    "heuristic": "euclidean",
    "delay": 32,
}


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


def test_load_config_succeeds_with_valid_data(tmp_path: Path):
    path = tmp_path / "config.yaml"
    path.write_text(yaml.safe_dump(valid_config_data))

    cfg = load_config(path)

    assert isinstance(cfg, Config)
    assert isinstance(cfg.map, Map)
    assert isinstance(cfg.heuristic, type(lambda: None))
    assert isinstance(cfg.delay, int)
    assert isinstance(cfg.source, tuple)
    assert isinstance(cfg.dest, tuple)

    assert cfg.heuristic == euclidean
    assert cfg.delay == 32
    assert cfg.source == (1, 1)
    assert cfg.dest == (2, 3)


@pytest.mark.parametrize(
    "missing_field",
    [
        "map",
        "heuristic",
        "delay",
    ],
)
def test_load_config_fails_with_missing_fields(tmp_path: Path, missing_field: str):
    config_data = valid_config_data.copy()
    config_data.pop(missing_field)

    path = tmp_path / "config.yaml"
    path.write_text(yaml.safe_dump(config_data))

    with pytest.raises(ParserError) as exc:
        load_config(path)

    assert missing_field in str(exc.value)


@pytest.mark.parametrize(
    "delay, expected_error",
    [
        (-1, "delay must be non-negative"),
        (-999, "delay must be non-negative"),
        (-0.001, "delay must be an integer"),
        (32.3, "delay must be an integer"),
        ("not_a_number", "delay must be an integer"),
    ],
)
def test_load_config_fails_with_invalid_delay(
    tmp_path: Path, delay: int | float | str, expected_error: str
):
    config_data = valid_config_data.copy()
    config_data["delay"] = delay  # ty:ignore[invalid-assignment]

    path = tmp_path / "config.yaml"
    path.write_text(yaml.safe_dump(config_data))

    with pytest.raises(ParserError) as exc:
        load_config(path)

    assert expected_error in str(exc.value)


def test_load_config_fails_with_unsupported_heuristic(tmp_path: Path):
    config_data = valid_config_data.copy()
    config_data["heuristic"] = "unsupported_heuristic"

    path = tmp_path / "config.yaml"
    path.write_text(yaml.safe_dump(config_data))

    with pytest.raises(ParserError) as exc:
        load_config(path)

    assert "unsupported heuristic" in str(exc.value)


def test_load_config_replaces_source_and_destination_with_spaces(tmp_path: Path):
    path = tmp_path / "config.yaml"
    path.write_text(yaml.safe_dump(valid_config_data))

    cfg = load_config(path)

    assert cfg.source == (1, 1)
    assert cfg.dest == (2, 3)
    assert cfg.map.at(1, 1) == " "
    assert cfg.map.at(2, 3) == " "


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
def test_load_config_raises_parser_error(
    tmp_path: Path, map_str: str, expected_error: str
):
    config_data = valid_config_data.copy()
    config_data["map"] = map_str

    path = tmp_path / "config.yaml"
    path.write_text(yaml.safe_dump(config_data))

    with pytest.raises(ParserError, match=expected_error):
        load_config(path)

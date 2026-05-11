import textwrap
from collections.abc import Callable
from pathlib import Path

import pytest
import yaml

from animated_a_star_cli.core.config import Config
from animated_a_star_cli.core.heuristic import euclidean, manhattan
from animated_a_star_cli.core.map import Map
from animated_a_star_cli.ui.parser import ParserError, load_config


@pytest.fixture
def valid_config_data() -> dict:
    map = textwrap.dedent("""\
        #####
        #o  #
        # #x#
        #####
    """)
    return {
        "map": map,
        "heuristic": "euclidean",
        "delay": 32,
    }


def write_config(config_data: dict, tmp_path: Path) -> Path:
    path = tmp_path / "config.yaml"
    path.write_text(yaml.safe_dump(config_data))
    return path


class TestParsing:
    @staticmethod
    def test_load_config_succeeds_with_valid_data(
        tmp_path: Path, valid_config_data: dict
    ):
        path = write_config(valid_config_data, tmp_path)
        cfg = load_config(path)

        assert isinstance(cfg, Config)
        assert isinstance(cfg.map, Map)
        assert isinstance(cfg.delay, int)
        assert isinstance(cfg.source, tuple)
        assert isinstance(cfg.dest, tuple)

        assert cfg.heuristic is euclidean
        assert cfg.delay == 32
        assert cfg.source == (1, 1)
        assert cfg.dest == (2, 3)

    @staticmethod
    def test_load_config_replaces_source_and_destination_with_spaces(
        tmp_path: Path, valid_config_data: dict
    ):
        path = write_config(valid_config_data, tmp_path)
        cfg = load_config(path)

        assert cfg.source == (1, 1)
        assert cfg.dest == (2, 3)
        assert cfg.map.at(1, 1) == " "
        assert cfg.map.at(2, 3) == " "

    @pytest.mark.parametrize(
        "heuristic, expected_func",
        [
            ("euclidean", euclidean),
            ("manhattan", manhattan),
        ],
    )
    @staticmethod
    def test_load_config_succeeds_with_supported_heuristics(
        heuristic: str, expected_func: Callable, tmp_path: Path, valid_config_data: dict
    ):
        config_data = valid_config_data.copy()
        config_data["heuristic"] = heuristic
        path = write_config(config_data, tmp_path)

        cfg = load_config(path)

        assert cfg.heuristic is expected_func

    @pytest.mark.parametrize("delay", [0, 1, 32, 100, int(1e9)])
    @staticmethod
    def test_load_config_succeeds_with_valid_delay(
        delay: int, tmp_path: Path, valid_config_data: dict
    ):
        config_data = valid_config_data.copy()
        config_data["delay"] = delay
        path = write_config(config_data, tmp_path)

        cfg = load_config(path)

        assert cfg.delay == delay


class TestValidation:
    NON_RETANGULAR_MAP = textwrap.dedent("""\
        ###
        #o##
    """)
    NON_3x3_MAPS = [
        textwrap.dedent("""\
            ##
            #o
            ##
        """),
        textwrap.dedent("""\
            #o#
            #x#
        """),
    ]
    INVALID_CHAR_MAP = textwrap.dedent("""\
        ###
        #o#
        #a#
    """)
    TWO_SOURCES_MAP = textwrap.dedent("""\
        ###
        #oo
        #x#
    """)
    TWO_DESTS_MAP = TWO_SOURCES_MAP.replace("o", "x", 1)
    NO_SOURCE_MAP = textwrap.dedent("""\
        ###
        # #
        #x#
    """)

    @pytest.mark.parametrize(
        "config_content, expected_error",
        [
            ("", "config file is empty"),
            ("   \n  ", "config file is empty"),
            (
                "- just a list\n- not a dict",
                "invalid config format. expected a dictionary",
            ),
            ("not: a valid: yaml: content", "invalid YAML format"),
            ("map: [unclosed", "invalid YAML format"),
        ],
    )
    @staticmethod
    def test_load_config_fails_with_invalid_content(
        tmp_path: Path, config_content: str, expected_error: str
    ):
        path = tmp_path / "config.yaml"
        path.write_text(config_content)

        with pytest.raises(ParserError, match=expected_error):
            load_config(path)

    @staticmethod
    def test_load_config_fails_with_missing_file(tmp_path: Path):
        path = tmp_path / "nonexistent_config.yaml"

        with pytest.raises(FileNotFoundError):
            load_config(path)

    @pytest.mark.parametrize(
        "missing_field",
        [
            "map",
            "heuristic",
            "delay",
        ],
    )
    @staticmethod
    def test_load_config_fails_with_missing_fields(
        tmp_path: Path, missing_field: str, valid_config_data: dict
    ):
        config_data = valid_config_data.copy()
        config_data.pop(missing_field)
        path = write_config(config_data, tmp_path)

        with pytest.raises(ParserError, match=missing_field):
            load_config(path)

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
    @staticmethod
    def test_load_config_fails_with_invalid_delay(
        tmp_path: Path,
        delay: int | float | str,
        expected_error: str,
        valid_config_data: dict,
    ):
        config_data = valid_config_data.copy()
        config_data["delay"] = delay
        path = write_config(config_data, tmp_path)

        with pytest.raises(ParserError, match=expected_error):
            load_config(path)

    @staticmethod
    def test_load_config_fails_with_unsupported_heuristic(
        tmp_path: Path, valid_config_data: dict
    ):
        config_data = valid_config_data.copy()
        config_data["heuristic"] = "unsupported_heuristic"
        path = write_config(config_data, tmp_path)

        with pytest.raises(ParserError, match="unsupported heuristic"):
            load_config(path)

    @pytest.mark.parametrize(
        "map_str, expected_error",
        [
            ("", "map string is empty"),
            ("   \n  ", "map string is empty"),
            (NON_RETANGULAR_MAP, "map must be rectangular"),
            (NON_3x3_MAPS[0], "map must be at least 3x3"),
            (NON_3x3_MAPS[1], "map must be at least 3x3"),
            (INVALID_CHAR_MAP, "map contains invalid characters"),
            (TWO_SOURCES_MAP, "map must contain exactly one source 'o'"),
            (TWO_DESTS_MAP, "map must contain exactly one destination 'x'"),
            (NO_SOURCE_MAP, "map must contain exactly one source 'o'"),
        ],
    )
    @staticmethod
    def test_load_config_fails_with_invalid_map(
        tmp_path: Path, map_str: str, expected_error: str, valid_config_data: dict
    ):
        config_data = valid_config_data.copy()
        config_data["map"] = map_str
        path = write_config(config_data, tmp_path)

        with pytest.raises(ParserError, match=expected_error):
            load_config(path)

import textwrap
from collections.abc import Callable
from pathlib import Path
from typing import Any

import pytest
import yaml

from animated_a_star_cli.core.heuristic import euclidean, manhattan
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
    def assert_field(
        self,
        *,
        field: str,
        value: Any,
        expected_value: Any,
        valid_config_data: dict,
        tmp_path: Path,
    ):
        config_data = valid_config_data.copy()
        config_data[field] = value
        path = write_config(config_data, tmp_path)
        cfg = load_config(path)
        assert getattr(cfg, field) == expected_value

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
        "heuristic, expected_func", [("euclidean", euclidean), ("manhattan", manhattan)]
    )
    def test_load_config_succeeds_with_supported_heuristics(
        self,
        heuristic: str,
        expected_func: Callable,
        tmp_path: Path,
        valid_config_data: dict,
    ):
        self.assert_field(
            field="heuristic",
            value=heuristic,
            expected_value=expected_func,
            valid_config_data=valid_config_data,
            tmp_path=tmp_path,
        )

    @pytest.mark.parametrize("delay", [0, 1, 32, 100, int(1e9)])
    def test_load_config_succeeds_with_valid_delay(
        self, delay: int, tmp_path: Path, valid_config_data: dict
    ):
        self.assert_field(
            field="delay",
            value=delay,
            expected_value=delay,
            valid_config_data=valid_config_data,
            tmp_path=tmp_path,
        )


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

    def assert_invalid_field_error(
        self,
        *,
        field: str,
        invalid_value: Any,
        expected_error: str,
        valid_config_data: dict,
        tmp_path: Path,
    ):
        config_data = valid_config_data.copy()
        config_data[field] = invalid_value
        path = write_config(config_data, tmp_path)
        with pytest.raises(ParserError, match=expected_error):
            load_config(path)

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
    def test_load_config_fails_with_invalid_content(
        self, tmp_path: Path, config_content: str, expected_error: str
    ):
        path = tmp_path / "config.yaml"
        path.write_text(config_content)

        with pytest.raises(ParserError, match=expected_error):
            load_config(path)

    def test_load_config_fails_with_missing_file(self, tmp_path: Path):
        path = tmp_path / "nonexistent_config.yaml"

        with pytest.raises(FileNotFoundError):
            load_config(path)

    @pytest.mark.parametrize("missing_field", ["map", "heuristic", "delay"])
    def test_load_config_fails_with_missing_fields(
        self, tmp_path: Path, missing_field: str, valid_config_data: dict
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
    def test_load_config_fails_with_invalid_delay(
        self,
        tmp_path: Path,
        delay: int | float | str,
        expected_error: str,
        valid_config_data: dict,
    ):
        self.assert_invalid_field_error(
            field="delay",
            invalid_value=delay,
            expected_error=expected_error,
            valid_config_data=valid_config_data,
            tmp_path=tmp_path,
        )

    def test_load_config_fails_with_unsupported_heuristic(
        self, tmp_path: Path, valid_config_data: dict
    ):
        self.assert_invalid_field_error(
            field="heuristic",
            invalid_value="unsupported_heuristic",
            expected_error="unsupported heuristic",
            valid_config_data=valid_config_data,
            tmp_path=tmp_path,
        )

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
    def test_load_config_fails_with_invalid_map(
        self, tmp_path: Path, map_str: str, expected_error: str, valid_config_data: dict
    ):
        self.assert_invalid_field_error(
            field="map",
            invalid_value=map_str,
            expected_error=expected_error,
            valid_config_data=valid_config_data,
            tmp_path=tmp_path,
        )

from pathlib import Path

import pytest

from animated_a_star_cli.config import ConfigError, load_config


def test_loads_expected_map():
    config = load_config()
    expected_map = (
        "###########\n"
        "#o        #\n"
        "#         #\n"
        "#         #\n"
        "#         #\n"
        "#         #\n"
        "#        x#\n"
        "###########\n"
    )
    assert config.map == expected_map


def test_load_fails_with_missing_fields(tmp_path: Path):
    path = tmp_path / "invalid_config.yaml"
    path.write_text("wrong_field: 123")

    with pytest.raises(ConfigError, match="missing required config fields"):
        load_config(path)


def test_load_fails_with_invalid_format(tmp_path: Path):
    path = tmp_path / "invalid_config.yaml"
    path.write_text("- just a list\n- not a dict")

    with pytest.raises(ConfigError, match="invalid config format"):
        load_config(path)


def test_load_fails_with_empty_file(tmp_path: Path):
    path = tmp_path / "empty_config.yaml"
    path.write_text("")

    with pytest.raises(ConfigError, match="config file is empty"):
        load_config(path)


def test_load_fails_with_missing_file(tmp_path: Path):
    path = tmp_path / "nonexistent_config.yaml"

    with pytest.raises(FileNotFoundError):
        load_config(path)

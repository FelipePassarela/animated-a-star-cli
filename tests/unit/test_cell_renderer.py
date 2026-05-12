import pytest

from animated_a_star_cli.ui.cell_renderer import glyph_from_neighs


class TestPath:
    PATH_BODY_CASES = [
        (" ", " ", "*", "*", "═"),
        ("*", "*", " ", " ", "║"),
        (" ", "*", " ", "*", "╔"),
        (" ", "*", "*", " ", "╗"),
        ("*", " ", " ", "*", "╚"),
        ("*", " ", "*", " ", "╝"),
    ]
    PATH_HEAD_CASES = [
        ("*", " ", " ", " ", "↓"),
        (" ", "*", " ", " ", "↑"),
        (" ", " ", "*", " ", "→"),
        (" ", " ", " ", "*", "←"),
    ]
    NULL_PATH_CASES = [
        (None, None, "*", "*", "═"),
        ("*", "*", None, None, "║"),
        (None, "*", None, "*", "╔"),
        (None, "*", "*", None, "╗"),
        ("*", None, None, "*", "╚"),
        ("*", None, "*", None, "╝"),
    ]

    @pytest.mark.parametrize("up, down, left, right, expected", PATH_BODY_CASES)
    def test_from_neighs_returns_correct_path_body(
        self, up: str, down: str, left: str, right: str, expected: str
    ):
        glyph = glyph_from_neighs("*", up, down, left, right)
        assert glyph == expected

    @pytest.mark.parametrize("up, down, left, right, expected", PATH_HEAD_CASES)
    def test_from_neighs_returns_correct_path_head(
        self, up: str, down: str, left: str, right: str, expected: str
    ):
        glyph = glyph_from_neighs("*", up, down, left, right)
        assert glyph == expected

    @pytest.mark.parametrize("up, down, left, right, expected", NULL_PATH_CASES)
    def test_from_neighs_succeeds_with_null_path(
        self,
        up: str | None,
        down: str | None,
        left: str | None,
        right: str | None,
        expected: str,
    ):
        glyph = glyph_from_neighs("*", up, down, left, right)
        assert glyph == expected


class TestWall:
    WALL_CASES = [
        (" ", " ", " ", " ", "─"),
        (" ", " ", " ", "#", "─"),
        (" ", " ", "#", " ", "─"),
        (" ", " ", "#", "#", "─"),
        ("#", " ", " ", " ", "│"),
        (" ", "#", " ", " ", "│"),
        ("#", "#", " ", " ", "│"),
        (" ", "#", " ", "#", "┌"),
        (" ", "#", "#", " ", "┐"),
        ("#", " ", " ", "#", "└"),
        ("#", " ", "#", " ", "┘"),
        ("#", "#", "#", " ", "┤"),
        ("#", "#", " ", "#", "├"),
        ("#", " ", "#", "#", "┴"),
        (" ", "#", "#", "#", "┬"),
        ("#", "#", "#", "#", "┼"),
    ]
    NULL_WALL_CASES = [
        (None, None, None, None, "─"),
        (None, "#", "#", None, "┐"),
        ("#", "#", "#", None, "┤"),
        ("#", "#", None, "#", "├"),
        ("#", None, "#", "#", "┴"),
        (None, "#", "#", "#", "┬"),
    ]

    @pytest.mark.parametrize("up, down, left, right, expected", WALL_CASES)
    def test_from_neighs_succeeds_with_walls(
        self, up: str, down: str, left: str, right: str, expected: str
    ):
        glyph = glyph_from_neighs("#", up, down, left, right)
        assert glyph == expected

    @pytest.mark.parametrize("up, down, left, right, expected", NULL_WALL_CASES)
    def test_from_neighs_succeeds_with_null_wall(
        self,
        up: str | None,
        down: str | None,
        left: str | None,
        right: str | None,
        expected: str,
    ):
        glyph = glyph_from_neighs("#", up, down, left, right)
        assert glyph == expected


class TestUnknownNeighs:
    UNKNOWN_PATH_CASES = [
        (" ", " ", " ", " "),
        ("*", "*", "*", "*"),
        (" ", "*", "*", "*"),
        ("*", " ", "*", "*"),
        ("*", "*", " ", "*"),
        ("*", "*", "*", " "),
    ]
    UNKNOWN_CENTERS = [" ", "o", "x", "?", "A", "B", "C"]

    @pytest.mark.parametrize("center", UNKNOWN_CENTERS)
    def test_from_neighs_send_back_unknown_center(self, center: str):
        glyph = glyph_from_neighs(center, " ", " ", " ", " ")
        assert glyph == center

    @pytest.mark.parametrize("up, down, left, right", UNKNOWN_PATH_CASES)
    def test_from_neighs_returns_question_mark_for_unknown_path(
        self, up: str, down: str, left: str, right: str
    ):
        glyph = glyph_from_neighs("*", up, down, left, right)
        assert glyph == "?"

from itertools import product

import pytest

from pformat.indentation_utility import (
    DEFAULT_INDENT_CHARACTER,
    DEFAULT_INDENT_WIDTH,
    IndentMarker,
    IndentType,
)

from .conftest import assert_does_not_throw

BOOLEAN_VALS = [True, False]


class TestIndentMarker:
    INVALID_CHARS = ["", "abc"]
    VALID_CHARS = [" ", "_"]

    @pytest.fixture(autouse=True, params=BOOLEAN_VALS, ids=[f"fill={f}" for f in BOOLEAN_VALS])
    def setup(self, request: pytest.FixtureRequest):
        self.fill = request.param

    @pytest.mark.parametrize(
        "character", INVALID_CHARS, ids=[f"character={repr(c)}" for c in INVALID_CHARS]
    )
    def test_init_with_invalid_character_str(self, character: str):
        with pytest.raises(ValueError) as err:
            _ = IndentMarker(character, self.fill)

        assert (
            str(err.value)
            == f"The character of an IndentMarker must be a string of length 1 - got `{character}`"
        )

    @pytest.mark.parametrize(
        "character", VALID_CHARS, ids=[f"character={repr(c)}" for c in VALID_CHARS]
    )
    def test_init_with_valid_character_str(self, character: str):
        assert_does_not_throw(IndentMarker, character, self.fill)


INDENT_WIDTH_VALS = [2, 3, 4]
DEPTH_VASL = [0, 1, 2]


class TestIndentType:
    MARKERS = [
        IndentMarker(" ", fill=True),
        IndentMarker(".", fill=True),
        IndentMarker("|", fill=False),
    ]
    WM_PARAMS = list(product(INDENT_WIDTH_VALS, MARKERS))
    WM_IDS = [f"width={w},marker={m}" for w, m in WM_PARAMS]

    WD_PARAMS = list(product(INDENT_WIDTH_VALS, DEPTH_VASL))
    WD_IDS = [f"width={w},depth={d}" for w, d in WD_PARAMS]

    @pytest.fixture(params=WM_PARAMS, ids=WM_IDS)
    def sut(self, request: pytest.FixtureRequest) -> IndentType:
        self.dummy_str = "string"
        self.width, self.marker = request.param
        return IndentType(self.width, self.marker)

    def test_defalt_init(self):
        sut = IndentType()
        assert sut.width == DEFAULT_INDENT_WIDTH
        assert sut.marker == IndentMarker()

    def test_default_new(self):
        assert IndentType.new() == IndentType()

    @pytest.mark.parametrize("width,marker", WM_PARAMS, ids=WM_IDS)
    def test_new(self, width: int, marker: IndentMarker):
        assert IndentType.new(
            width=width, character=marker.character, fill=marker.fill
        ) == IndentType(width, marker)

    @pytest.mark.parametrize(
        "width", INDENT_WIDTH_VALS, ids=[f"width={w}" for w in INDENT_WIDTH_VALS]
    )
    def test_predefined_types(self, width: int):
        assert IndentType.NONE(width) == IndentType(width=width)
        assert IndentType.DOTS(width) == IndentType.new(width=width, character="·")
        assert IndentType.THICK_DOTS(width) == IndentType.new(width=width, character="•")
        assert IndentType.LINE(width) == IndentType.new(width=width, character="|", fill=False)
        assert IndentType.BROKEN_BAR(width) == IndentType.new(
            width=width, character="¦", fill=False
        )

    @pytest.mark.parametrize("width,depth", WD_PARAMS, ids=WD_IDS)
    def test_length(self, width: int, depth: int):
        sut = IndentType(width=width)
        assert sut.length(depth) == width * depth

    @pytest.mark.parametrize("width,depth", WD_PARAMS, ids=WD_IDS)
    def test_string_fill(self, width: int, depth: int):
        character = "_"
        sut = IndentType.new(width, character=character, fill=True)

        assert sut.string(depth) == character * sut.length(depth)

    @pytest.mark.parametrize("width,depth", WD_PARAMS, ids=WD_IDS)
    def test_string_no_fill(self, width: int, depth: int):
        character = "|"
        sut = IndentType.new(width, character=character, fill=False)

        assert sut.string(depth) == f"{character}{DEFAULT_INDENT_CHARACTER * (width - 1)}" * depth

    def test_add_to_default_depth(self, sut: IndentType):
        assert sut.add_to(self.dummy_str) == f"{sut.string(depth=1)}{self.dummy_str}"

    @pytest.mark.parametrize("depth", DEPTH_VASL, ids=[f"depth={d}" for d in DEPTH_VASL])
    def test_add_indent(self, sut: IndentType, depth: int):
        assert sut.add_to(self.dummy_str, depth) == f"{sut.string(depth)}{self.dummy_str}"

    @pytest.mark.parametrize("depth", DEPTH_VASL, ids=[f"depth={d}" for d in DEPTH_VASL])
    def test_add_to_each_for_empty_list(self, sut: IndentType, depth: int):
        assert len(sut.add_to_each(list(), depth)) == 0

    def test_add_to_each_default_depth(self, sut: IndentType):
        assert all(
            s_out == f"{sut.string(depth=1)}{self.dummy_str}"
            for s_out in sut.add_to_each([self.dummy_str for _ in range(5)])
        )

    @pytest.mark.parametrize("depth", DEPTH_VASL, ids=[f"depth={d}" for d in DEPTH_VASL])
    def test_add_to_each(self, sut: IndentType, depth: int):
        assert all(
            s_out == f"{sut.string(depth)}{self.dummy_str}"
            for s_out in sut.add_to_each([self.dummy_str for _ in range(5)], depth)
        )

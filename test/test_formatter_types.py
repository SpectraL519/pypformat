import pytest

from pformat.formatter_types import (
    CustomMultilineFormatter,
    CustomNormalFormatter,
    MultilineFormatter,
    NormalFormatter,
    TypeFormatter,
)

from .conftest import assert_does_not_throw

TYPES_DICT = {
    int: 123,
    float: 3.14,
    str: "string",
    bytes: b"bytes",
    list: [1, 2, 3],
    dict: {"k1": 1, "k2": 2},
}
TYPES_KEYS = list(TYPES_DICT.keys())


class InvalidType:
    pass


class TestTypeFormatterRepr:
    FORMATTER_TYPES = (TypeFormatter, NormalFormatter, MultilineFormatter)

    @pytest.fixture(autouse=True, params=TYPES_KEYS, ids=[f"t={t.__name__}" for t in TYPES_KEYS])
    def set_type_param(self, request: pytest.FixtureRequest) -> TypeFormatter:
        self.type = request.param

    @pytest.mark.parametrize(
        "fmt_type",
        FORMATTER_TYPES,
        ids=[f"fmt_type={fmt_type.__name__}" for fmt_type in FORMATTER_TYPES],
    )
    def test_repr(self, fmt_type: type):
        sut = fmt_type(self.type)
        assert repr(sut) == f"{fmt_type.__name__}({self.type.__name__})"


class TestTypeFormatter:
    @pytest.fixture(params=TYPES_KEYS, ids=[f"t={t.__name__}" for t in TYPES_KEYS])
    def sut(self, request: pytest.FixtureRequest) -> TypeFormatter:
        self.type = request.param
        return TypeFormatter(self.type)

    def test_call(self, sut: TypeFormatter):
        with pytest.raises(NotImplementedError) as err:
            sut(self.type())

        assert str(err.value) == f"{repr(sut)}.__call__ is not implemented"

    def test_check_type_invalid(self, sut: TypeFormatter):
        with pytest.raises(TypeError) as err:
            sut._check_type(InvalidType())

        assert str(err.value) == f"[{repr(sut)}] Cannot format an object of type `InvalidType`"

    def test_check_type_valid(self, sut: TypeFormatter):
        assert_does_not_throw(sut._check_type, self.type())


class TestCustomNormalFormatter:
    @pytest.fixture(params=TYPES_KEYS, ids=[f"t={t.__name__}" for t in TYPES_KEYS])
    def sut(self, request: pytest.FixtureRequest) -> CustomNormalFormatter:
        self.type = request.param
        self.fmt_func = lambda obj, depth: str(obj)
        return CustomNormalFormatter(self.type, self.fmt_func)

    def test_call_with_invalid_type(self, sut: CustomNormalFormatter):
        with pytest.raises(TypeError) as err:
            sut(InvalidType())

        assert str(err.value) == f"[{repr(sut)}] Cannot format an object of type `InvalidType`"

    def test_call_with_correct_type(self, sut: CustomNormalFormatter):
        value = TYPES_DICT[self.type]
        assert sut(value) == self.fmt_func(value, depth=0)


class TestCustomMultilineFormatter:
    @pytest.fixture(params=TYPES_KEYS, ids=[f"t={t.__name__}" for t in TYPES_KEYS])
    def sut(self, request: pytest.FixtureRequest) -> CustomMultilineFormatter:
        self.type = request.param
        self.fmt_func = lambda obj, depth: [str(obj)]
        return CustomMultilineFormatter(self.type, self.fmt_func)

    def test_call_with_invalid_type(self, sut: CustomMultilineFormatter):
        with pytest.raises(TypeError) as err:
            sut(InvalidType())

        assert str(err.value) == f"[{repr(sut)}] Cannot format an object of type `InvalidType`"

    def test_call_with_correct_type(self, sut: CustomMultilineFormatter):
        value = TYPES_DICT[self.type]
        assert sut(value) == self.fmt_func(value, depth=0)

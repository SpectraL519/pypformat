from itertools import product
from typing import Any

import pytest

from pformat.formatter_types import (
    CustomMultilineFormatter,
    CustomNormalFormatter,
    MultilineFormatter,
    NormalFormatter,
    TypeFormatter,
    multiline_formatter,
    normal_formatter,
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
TYPES = list(TYPES_DICT.keys())


class InvalidType:
    pass


class TestTypeFormatterCommon:
    FORMATTER_TYPES = (TypeFormatter, NormalFormatter, MultilineFormatter)

    @pytest.fixture(
        autouse=True,
        params=product(FORMATTER_TYPES, TYPES),
        ids=[
            f"fmt_type={fmt_t.__name__},t={t.__name__}"
            for fmt_t, t in product(FORMATTER_TYPES, TYPES)
        ],
    )
    def set_type_param(self, request: pytest.FixtureRequest) -> TypeFormatter:
        self.fmt_type, self.type = request.param

    def test_eq_with_non_formatter_type(self):
        sut = self.fmt_type(self.type)

        with pytest.raises(TypeError) as err:
            sut == InvalidType()

        assert (
            str(err.value)
            == f"Cannot compare a `{self.fmt_type.__name__}` instance to an instance of `InvalidType`"
        )

    def test_eq_with_valid_formatter_type(self):
        sut = self.fmt_type(self.type)

        assert all(sut == ft(self.type) for ft in TestTypeFormatterCommon.FORMATTER_TYPES)
        assert all(sut != ft(InvalidType) for ft in TestTypeFormatterCommon.FORMATTER_TYPES)

    def test_repr(self):
        sut = self.fmt_type(self.type)
        assert repr(sut) == f"{self.fmt_type.__name__}({self.type.__name__})"

    def test_is_valid_with_concrete_type(self):
        sut = self.fmt_type(self.type)
        assert sut.is_valid(self.type())
        assert not sut.is_valid(InvalidType())

    def test_is_valid_with_any_type(self):
        sut = self.fmt_type(Any)
        assert sut.is_valid(self.type())
        assert sut.is_valid(InvalidType())


class TestTypeFormatter:
    @pytest.fixture(params=TYPES, ids=[f"t={t.__name__}" for t in TYPES])
    def sut(self, request: pytest.FixtureRequest) -> TypeFormatter:
        self.type = request.param
        return TypeFormatter(self.type)

    def test_call(self, sut: TypeFormatter):
        with pytest.raises(NotImplementedError) as err:
            sut(self.type())

        assert str(err.value) == f"{repr(sut)}.__call__ is not implemented"

    def test_check_type_invalid(self, sut: TypeFormatter):
        invalid_value = InvalidType()
        with pytest.raises(TypeError) as err:
            sut._check_type(invalid_value)

        assert (
            str(err.value)
            == f"[{repr(sut)}] Cannot format an object of type `InvalidType` - `{str(invalid_value)}`"
        )

    def test_check_type_valid(self, sut: TypeFormatter):
        assert_does_not_throw(sut._check_type, self.type())


class TestCustomNormalFormatter:
    @pytest.fixture(params=TYPES, ids=[f"t={t.__name__}" for t in TYPES])
    def sut(self, request: pytest.FixtureRequest) -> CustomNormalFormatter:
        self.type = request.param
        self.fmt_func = lambda obj, depth: str(obj)
        return CustomNormalFormatter(self.type, self.fmt_func)

    def test_call_with_invalid_type(self, sut: CustomNormalFormatter):
        invalid_value = InvalidType()
        with pytest.raises(TypeError) as err:
            sut(invalid_value)

        assert (
            str(err.value)
            == f"[{repr(sut)}] Cannot format an object of type `InvalidType` - `{str(invalid_value)}`"
        )

    def test_call_with_correct_type(self, sut: CustomNormalFormatter):
        value = TYPES_DICT[self.type]
        assert sut(value) == self.fmt_func(value, depth=0)

    @pytest.mark.parametrize("t", TYPES)
    def test_normal_formatter_builder(self, t: type):
        fmt_func = lambda x, depth: str(x)
        sut = normal_formatter(t, fmt_func)

        assert isinstance(sut, CustomNormalFormatter)

        value = t()
        assert sut(value) == fmt_func(value, depth=0)


class TestCustomMultilineFormatter:
    @pytest.fixture(params=TYPES, ids=[f"t={t.__name__}" for t in TYPES])
    def sut(self, request: pytest.FixtureRequest) -> CustomMultilineFormatter:
        self.type = request.param
        self.fmt_func = lambda obj, depth: [str(obj)]
        return CustomMultilineFormatter(self.type, self.fmt_func)

    def test_call_with_invalid_type(self, sut: CustomMultilineFormatter):
        invalid_value = InvalidType()
        with pytest.raises(TypeError) as err:
            sut(invalid_value)

        assert (
            str(err.value)
            == f"[{repr(sut)}] Cannot format an object of type `InvalidType` - `{str(invalid_value)}`"
        )

    def test_call_with_correct_type(self, sut: CustomMultilineFormatter):
        value = TYPES_DICT[self.type]
        assert sut(value) == self.fmt_func(value, depth=0)

    @pytest.mark.parametrize("t", TYPES)
    def test_normal_formatter_builder(self, t: type):
        fmt_func = lambda x, depth: [str(x)]
        sut = multiline_formatter(t, fmt_func)

        assert isinstance(sut, CustomMultilineFormatter)

        value = t()
        assert sut(value) == fmt_func(value, depth=0)

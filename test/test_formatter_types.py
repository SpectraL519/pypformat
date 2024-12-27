import sys
from itertools import product
from typing import Any, Union

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


def gen_concrete_fmt_type(fmt_type: type) -> type:
    class ConcreteFormatter(fmt_type):
        def __call__(self, obj: Any, depth: int = 0) -> str:
            fmt_type.__call__(self, obj, depth)

    return ConcreteFormatter


FORMATTER_TYPES = [
    gen_concrete_fmt_type(ft) for ft in (TypeFormatter, NormalFormatter, MultilineFormatter)
]


class TestTypeFormatterCommon:
    def __gen_derived_type(self, t: type) -> type:
        class derived(t):
            pass

        return derived

    @pytest.fixture(
        params=product(FORMATTER_TYPES, TYPES),
        ids=[
            f"fmt_type={fmt_t.__name__},t={t.__name__}"
            for fmt_t, t in product(FORMATTER_TYPES, TYPES)
        ],
    )
    def set_fmt_and_type_params(self, request: pytest.FixtureRequest) -> TypeFormatter:
        self.fmt_type, self.type = request.param
        self.derived_type = self.__gen_derived_type(self.type)

    def test_eq_with_non_formatter_type(self, set_fmt_and_type_params):
        sut = self.fmt_type(self.type)

        with pytest.raises(TypeError) as err:
            sut == InvalidType()

        assert (
            str(err.value)
            == f"Cannot compare a `{self.fmt_type.__name__}` instance to an instance of `InvalidType`"
        )

    def test_eq_with_valid_formatter_type(self, set_fmt_and_type_params):
        sut = self.fmt_type(self.type)

        assert all(sut == ft(self.type) for ft in FORMATTER_TYPES)
        assert all(sut != ft(InvalidType) for ft in FORMATTER_TYPES)

    def test_repr(self, set_fmt_and_type_params):
        sut = self.fmt_type(self.type)
        assert repr(sut) == f"{self.fmt_type.__name__}({self.type.__name__})"

    STRICT_VALS = [True, False]

    @pytest.mark.parametrize(
        "exact_match", STRICT_VALS, ids=[f"{exact_match=}" for exact_match in STRICT_VALS]
    )
    def test_has_valid_type_with_any_type(self, set_fmt_and_type_params, exact_match: bool):
        sut = self.fmt_type(Any)
        assert sut.has_valid_type(self.type(), exact_match=exact_match)
        assert sut.has_valid_type(InvalidType(), exact_match=exact_match)

    def test_has_valid_type_with_concrete_type(self, set_fmt_and_type_params):
        sut = self.fmt_type(self.type)

        assert sut.has_valid_type(self.type())
        assert sut.has_valid_type(self.derived_type())
        assert not sut.has_valid_type(InvalidType())

    def test_has_valid_type_with_concrete_type_exact_match(self, set_fmt_and_type_params):
        sut = self.fmt_type(self.type)

        assert sut.has_valid_type(self.type(), exact_match=True)
        assert not sut.has_valid_type(self.derived_type(), exact_match=True)
        assert not sut.has_valid_type(InvalidType(), exact_match=True)

    if sys.version_info >= (3, 10):
        union_type = int | float | str | bytes | list | dict
    else:
        union_type = Union[int, float, str, bytes, list, dict]

    @pytest.mark.parametrize(
        "fmt_type", FORMATTER_TYPES, ids=[f"{fmt_type=}" for fmt_type in FORMATTER_TYPES]
    )
    def test_has_valid_type_with_union_type(self, fmt_type: type):
        sut = gen_concrete_fmt_type(fmt_type)(self.union_type)

        assert all(sut.has_valid_type(t()) for t in TYPES)
        assert all(sut.has_valid_type(self.__gen_derived_type(t)()) for t in TYPES)
        assert not sut.has_valid_type(InvalidType())

    @pytest.mark.parametrize(
        "fmt_type", FORMATTER_TYPES, ids=[f"{fmt_type=}" for fmt_type in FORMATTER_TYPES]
    )
    def test_has_valid_type_with_union_type_exact_match(self, fmt_type: type):
        sut = fmt_type(self.union_type)

        assert all(sut.has_valid_type(t(), exact_match=True) for t in TYPES)
        assert all(
            not sut.has_valid_type(self.__gen_derived_type(t)(), exact_match=True) for t in TYPES
        )
        assert not sut.has_valid_type(InvalidType(), exact_match=True)


class TestTypeFormatter:
    @pytest.fixture(
        params=list(product(FORMATTER_TYPES, TYPES)),
        ids=[f"fmt_type={ft},t={t.__name__}" for ft, t in product(FORMATTER_TYPES, TYPES)],
    )
    def sut(self, request: pytest.FixtureRequest) -> TypeFormatter:
        self.fmt_type, self.type = request.param
        return self.fmt_type(self.type)

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

import sys
from typing import Any, Union

import pytest

from pformat.typing_utility import _has_valid_type, _is_union


def test_is_union():
    assert _is_union(Union[int, float])

    if sys.version_info >= (3, 10):
        assert _is_union(int | float)

    assert not _is_union(object)
    assert not _is_union(Any)
    assert not _is_union(int)


class TestHasValidType:
    TYPES = (int, float, str, bytes, list, dict)
    EXACT_MATCH_VALS = [True, False]

    def __gen_derived_type(self, t: type) -> type:
        class Derived(t):
            pass

        return Derived

    class InvalidType:
        pass

    @pytest.fixture(params=TYPES, ids=[f"t={t.__name__}" for t in TYPES])
    def set_type_params(self, request: pytest.FixtureRequest):
        self.type = request.param
        self.derived_type = self.__gen_derived_type(self.type)

    @pytest.mark.parametrize(
        "exact_match", EXACT_MATCH_VALS, ids=[f"{exact_match=}" for exact_match in EXACT_MATCH_VALS]
    )
    def test_has_valid_type_with_any_type(self, set_type_params, exact_match: bool):
        assert _has_valid_type(self.type(), Any, exact_match=exact_match)
        assert _has_valid_type(self.derived_type(), Any, exact_match=exact_match)
        assert _has_valid_type(TestHasValidType.InvalidType(), Any, exact_match=exact_match)

    def test_has_valid_type_with_concrete_type(self, set_type_params):
        assert _has_valid_type(self.type(), self.type)
        assert _has_valid_type(self.derived_type(), self.type)
        assert not _has_valid_type(TestHasValidType.InvalidType(), self.type)

    def test_has_valid_type_with_concrete_type_exact_match(self, set_type_params):
        assert _has_valid_type(self.type(), self.type, exact_match=True)
        assert not _has_valid_type(self.derived_type(), self.type, exact_match=True)
        assert not _has_valid_type(TestHasValidType.InvalidType(), self.type, exact_match=True)

    if sys.version_info >= (3, 10):
        union_type = int | float | str | bytes | list | dict
    else:
        union_type = Union[int, float, str, bytes, list, dict]

    def test_has_valid_type_with_union_type(self):
        assert all(_has_valid_type(t(), self.union_type) for t in TestHasValidType.TYPES)
        assert all(
            _has_valid_type(self.__gen_derived_type(t)(), self.union_type)
            for t in TestHasValidType.TYPES
        )
        assert not _has_valid_type(TestHasValidType.InvalidType(), self.union_type)

    def test_has_valid_type_with_union_type_exact_match(self):
        assert all(
            _has_valid_type(t(), self.union_type, exact_match=True) for t in TestHasValidType.TYPES
        )
        assert all(
            not _has_valid_type(self.__gen_derived_type(t)(), self.union_type, exact_match=True)
            for t in TestHasValidType.TYPES
        )
        assert not _has_valid_type(
            TestHasValidType.InvalidType(), self.union_type, exact_match=True
        )

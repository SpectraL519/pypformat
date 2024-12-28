import sys
from functools import cmp_to_key
from typing import Any, Union

import pytest

from pformat.typing_utility import Ordering, has_valid_type, is_union, type_cmp


def test_is_union():
    assert is_union(Union[int, float])

    if sys.version_info >= (3, 10):
        assert is_union(int | float)

    assert not is_union(object)
    assert not is_union(Any)
    assert not is_union(int)


TYPES = (int, float, str, bytes, list, dict)
TYPE_IDS = [f"t={t.__name__}" for t in TYPES]

if sys.version_info >= (3, 10):
    UNION_TYPE = int | float | str | bytes | list | dict
else:
    UNION_TYPE = Union[int, float, str, bytes, list, dict]


class DummyType1:
    pass


class DummyType2:
    pass


def gen_derived_type(t: type) -> type:
    class Derived(t):
        pass

    return Derived


class TestHasValidType:
    @pytest.fixture(params=TYPES, ids=TYPE_IDS)
    def set_type_params(self, request: pytest.FixtureRequest):
        self.type = request.param
        self.derived_type = gen_derived_type(self.type)

    EXACT_MATCH_VALS = [True, False]

    @pytest.mark.parametrize(
        "exact_match", EXACT_MATCH_VALS, ids=[f"{exact_match=}" for exact_match in EXACT_MATCH_VALS]
    )
    def test_has_valid_type_with_any_type(self, set_type_params, exact_match: bool):
        assert has_valid_type(self.type(), Any, exact_match=exact_match)
        assert has_valid_type(self.derived_type(), Any, exact_match=exact_match)
        assert has_valid_type(DummyType1(), Any, exact_match=exact_match)

    def test_has_valid_type_with_concrete_type(self, set_type_params):
        assert has_valid_type(self.type(), self.type)
        assert has_valid_type(self.derived_type(), self.type)
        assert not has_valid_type(DummyType1(), self.type)

    def test_has_valid_type_with_concrete_type_exact_match(self, set_type_params):
        assert has_valid_type(self.type(), self.type, exact_match=True)
        assert not has_valid_type(self.derived_type(), self.type, exact_match=True)
        assert not has_valid_type(DummyType1(), self.type, exact_match=True)

    def test_has_valid_type_with_union_type(self):
        assert all(has_valid_type(t(), UNION_TYPE) for t in TYPES)
        assert all(has_valid_type(gen_derived_type(t)(), UNION_TYPE) for t in TYPES)
        assert not has_valid_type(DummyType1(), UNION_TYPE)

    def test_has_valid_type_with_union_type_exact_match(self):
        assert all(has_valid_type(t(), UNION_TYPE, exact_match=True) for t in TYPES)
        assert all(
            not has_valid_type(gen_derived_type(t)(), UNION_TYPE, exact_match=True) for t in TYPES
        )
        assert not has_valid_type(DummyType1(), UNION_TYPE, exact_match=True)


class TestTypeCmp:
    @pytest.fixture(params=TYPES, ids=TYPE_IDS)
    def set_type(self, request: pytest.FixtureRequest):
        self.type = request.param

    def test_cmp_with_same_types(self, set_type):
        assert type_cmp(self.type, self.type) == Ordering.EQ

    def test_cmp_with_object_and_any_combinations(self):
        assert type_cmp(object, object) == Ordering.EQ
        assert type_cmp(Any, Any) == Ordering.EQ

        assert type_cmp(object, Any) == Ordering.EQ
        assert type_cmp(Any, object) == Ordering.EQ

    def test_cmp_with_any_or_object(self, set_type):
        assert type_cmp(self.type, object) == Ordering.LT
        assert type_cmp(object, self.type) == Ordering.GT

        assert type_cmp(self.type, Any) == Ordering.LT
        assert type_cmp(Any, self.type) == Ordering.GT

    def test_cmp_with_both_union(self):
        u1 = UNION_TYPE
        u2 = (
            DummyType1 | DummyType2
            if sys.version_info >= (3, 10)
            else Union[DummyType1, DummyType2]
        )

        assert u1 is not u2
        assert type_cmp(u1, u2) == Ordering.EQ
        assert type_cmp(u2, u1) == Ordering.EQ

    def test_cmp_with_union_and_valid_type(self, set_type):
        derived_type = gen_derived_type(self.type)

        assert type_cmp(self.type, UNION_TYPE) == Ordering.LT
        assert type_cmp(UNION_TYPE, self.type) == Ordering.GT

        assert type_cmp(derived_type, UNION_TYPE) == Ordering.LT
        assert type_cmp(UNION_TYPE, derived_type) == Ordering.GT

    def test_cmp_with_union_and_invalid_type(self):
        assert type_cmp(DummyType1, UNION_TYPE) == Ordering.EQ
        assert type_cmp(UNION_TYPE, DummyType1) == Ordering.EQ

    def test_cmp_with_derived_types(self, set_type):
        derived_type_1 = gen_derived_type(self.type)
        derived_type_2 = gen_derived_type(derived_type_1)

        assert type_cmp(derived_type_1, self.type) == Ordering.LT
        assert type_cmp(derived_type_2, self.type) == Ordering.LT
        assert type_cmp(derived_type_2, derived_type_1) == Ordering.LT

        assert type_cmp(self.type, derived_type_1) == Ordering.GT
        assert type_cmp(self.type, derived_type_2) == Ordering.GT
        assert type_cmp(derived_type_1, derived_type_2) == Ordering.GT

    def test_cmp_with_different_types(self, set_type):
        assert type_cmp(DummyType1, DummyType2) == Ordering.EQ

    def test_sort_types(self):
        DummyType1Derived = gen_derived_type(DummyType1)
        DummyType2Derived = gen_derived_type(DummyType2)
        DummyTypeUnion = (
            DummyType1 | DummyType2
            if sys.version_info >= (3, 10)
            else Union[DummyType1, DummyType2]
        )

        types = [DummyTypeUnion, DummyType1Derived, DummyType2Derived, DummyType1, DummyType2]
        sorted_types = list(sorted(types, key=cmp_to_key(type_cmp)))

        assert sorted_types.index(DummyType1Derived) < sorted_types.index(DummyType1)
        assert sorted_types.index(DummyType2Derived) < sorted_types.index(DummyType2)

        assert sorted_types[-1] is DummyTypeUnion

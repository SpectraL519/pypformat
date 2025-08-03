import sys
from collections import (
    ChainMap,
    Counter,
    OrderedDict,
    UserDict,
    UserList,
    defaultdict,
    deque,
)
from collections.abc import Iterable, Mapping
from functools import cmp_to_key
from itertools import product
from types import GenericAlias, MappingProxyType
from typing import Any, Union

import pytest

from pformat.named_types import NamedIterable, NamedMapping
from pformat.typing_utility import Ordering, has_valid_type, is_type, is_union, type_cmp

from .conftest import gen_derived_type


def test_is_union():
    assert is_union(Union[int, float])

    if sys.version_info >= (3, 10):
        assert is_union(int | float)

    assert not is_union(object)
    assert not is_union(Any)
    assert not is_union(int)


SIMPLE_TYPES = (int, float, str, bytes, list, dict)
SIMPLE_TYPE_IDS = [f"t={t.__name__}" for t in SIMPLE_TYPES]

if sys.version_info >= (3, 10):
    UNION_TYPE = int | float | str | bytes | list | dict
else:
    UNION_TYPE = Union[int, float, str, bytes, list, dict]


class DummyType1:
    pass


class DummyType2:
    pass


class TestIsType:
    def test_simple_types(self):
        assert all(is_type(t) for t in SIMPLE_TYPES)

    def test_simple_type_instances(self):
        assert not any(is_type(t()) for t in SIMPLE_TYPES)

    def test_generic_aliases(self):
        assert all(
            is_type(t[v])
            for t in [list, UserList, set, frozenset, tuple, deque, NamedIterable]
            for v in SIMPLE_TYPES
        )
        assert all(
            is_type(t[v])
            for t in [
                dict,
                defaultdict,
                UserDict,
                OrderedDict,
                ChainMap,
                MappingProxyType,
                Counter,
                NamedMapping,
            ]
            for v in SIMPLE_TYPES
        )

    def test_generic_alias_instances(self):
        assert not any(
            is_type(t[v]())
            for t in [list, UserList, set, frozenset, tuple, deque]
            for v in SIMPLE_TYPES
        )
        assert not any(
            is_type(t[v, v]())
            for t in [dict, defaultdict, UserDict, OrderedDict, ChainMap, Counter]
            for v in SIMPLE_TYPES
        )


class TestHasValidType:
    @pytest.fixture(params=SIMPLE_TYPES, ids=SIMPLE_TYPE_IDS)
    def set_type_params(self, request: pytest.FixtureRequest):
        self.type = request.param
        self.derived_type = gen_derived_type(self.type)

    EXACT_MATCH_VALS = [True, False]

    @pytest.mark.parametrize(
        "exact_match", EXACT_MATCH_VALS, ids=[f"{exact_match=}" for exact_match in EXACT_MATCH_VALS]
    )
    def test_any_type(self, set_type_params, exact_match: bool):
        assert has_valid_type(self.type(), Any, exact_match=exact_match)
        assert has_valid_type(self.derived_type(), Any, exact_match=exact_match)
        assert has_valid_type(DummyType1(), Any, exact_match=exact_match)

    def test_concrete_type(self, set_type_params):
        assert has_valid_type(self.type(), self.type)
        assert has_valid_type(self.derived_type(), self.type)
        assert not has_valid_type(DummyType1(), self.type)

    def test_with_concrete_type_exact_match(self, set_type_params):
        assert has_valid_type(self.type(), self.type, exact_match=True)
        assert not has_valid_type(self.derived_type(), self.type, exact_match=True)
        assert not has_valid_type(DummyType1(), self.type, exact_match=True)

    def test_with_union_type(self):
        assert all(has_valid_type(t(), UNION_TYPE) for t in SIMPLE_TYPES)
        assert all(has_valid_type(gen_derived_type(t)(), UNION_TYPE) for t in SIMPLE_TYPES)
        assert not has_valid_type(DummyType1(), UNION_TYPE)

    def test_with_union_type_exact_match(self):
        assert all(has_valid_type(t(), UNION_TYPE, exact_match=True) for t in SIMPLE_TYPES)
        assert all(
            not has_valid_type(gen_derived_type(t)(), UNION_TYPE, exact_match=True)
            for t in SIMPLE_TYPES
        )
        assert not has_valid_type(DummyType1(), UNION_TYPE, exact_match=True)

    def test_type_or_generic_alias_type(self):
        types = [
            int,
            float,
            str,
            list,
            tuple,
            set,
            dict,
        ]
        concrete_generic_aliases = [
            list[int],
            UserList[int],
            set[int],
            frozenset[int],
            tuple[int],
            deque[int],
            dict[int, int],
            defaultdict[int, int],
            UserDict[int, int],
            OrderedDict[int, int],
            ChainMap[int, int],
            Counter[int, int],
        ]
        generic_aliases = [
            *concrete_generic_aliases,
            Iterable[int],
            Mapping[int, int],
        ]

        assert all(has_valid_type(t(), t) for t in types)
        assert all(has_valid_type(t(), t) for t in concrete_generic_aliases)

        type_collections = [types, generic_aliases]
        for T1, T2 in product(type_collections, type_collections):
            # for t1 in T1:
            #     for t2 in T2:
            #         assert not has_valid_type(t1, t2)
            assert not any(has_valid_type(t1, t2) for t1 in T1 for t2 in T2)

        assert all(has_valid_type(t, type) for t in types)
        # assert all(has_valid_type(t, GenericAlias) for t in generic_aliases)
        for t in generic_aliases:
            import pdb

            pdb.set_trace()
            assert has_valid_type(t, GenericAlias)


class TestTypeCmp:
    @pytest.fixture(params=SIMPLE_TYPES, ids=SIMPLE_TYPE_IDS)
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

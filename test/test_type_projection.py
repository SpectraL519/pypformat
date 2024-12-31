from unittest.mock import patch

import pytest

from pformat.type_projection import TypeProjection, projection

from .conftest import assert_does_not_throw, gen_derived_type

TYPE_VALS = {
    int: 123,
    float: 3.14,
    str: "string",
    bytes: b"bytes",
    list: [1, 2, 3],
    dict: {"k1": 1, "k2": 2},
}
TYPE_PROJECTIONS = {
    int: lambda x: str(x),
    float: lambda x: int(x),
    str: lambda x: list(x),
    bytes: lambda x: x.decode("utf-8", errors="ignore"),
    list: lambda x: tuple(x),
    dict: lambda x: list(x.items()),
}
TYPES = list(TYPE_VALS.keys())


class InvalidType:
    pass


class TestTypeProjection:
    @pytest.fixture(params=TYPES, ids=[f"t={t.__name__}" for t in TYPES])
    def sut(self, request: pytest.FixtureRequest) -> TypeProjection:
        self.type = request.param
        self.value = TYPE_VALS[self.type]
        return TypeProjection(self.type)

    def test_eq_with_non_projection_type(self, sut: TypeProjection):
        with pytest.raises(TypeError) as err:
            sut == InvalidType()

        assert (
            str(err.value)
            == "Cannot compare a `TypeProjection` instance to an instance of `InvalidType`"
        )

    def test_eq_with_valid_projection_types(self, sut: TypeProjection):
        assert sut == TypeProjection(self.type)
        assert sut != TypeProjection(InvalidType)

    def test_repr(self, sut: TypeProjection):
        assert repr(sut) == f"TypeProjection({self.type.__name__})"

    def test_call_with_invalid_type(self, sut: TypeProjection):
        invalid_value = InvalidType()
        with pytest.raises(TypeError) as err:
            sut(invalid_value)

        assert (
            str(err.value)
            == f"[{repr(sut)}] Cannot process an object of type `InvalidType` - `{str(invalid_value)}`"
        )

    def test_call_with_default_projection(self, sut: TypeProjection):
        assert sut(self.value) == self.value

    @pytest.mark.parametrize("t", TYPES, ids=[f"t={t.__name__}" for t in TYPES])
    def test_call_with_non_default_projection(self, t: type):
        value = TYPE_VALS[t]
        proj = TYPE_PROJECTIONS[t]

        sut = TypeProjection(t, proj)
        assert sut(value) == proj(value)

    @patch("pformat.type_specific_callable.has_valid_type")
    def test_has_valid_type(self, mock_has_valid_type, sut: TypeProjection):
        invalid_value = InvalidType()

        sut.has_valid_type(invalid_value)
        mock_has_valid_type.assert_called_once_with(invalid_value, self.type, False)

        mock_has_valid_type.reset_mock()

        sut.has_valid_type(invalid_value, exact_match=True)
        mock_has_valid_type.assert_called_once_with(invalid_value, self.type, True)

    def test_validate_type_invalid(self, sut: TypeProjection):
        invalid_value = InvalidType()
        expected_err_msg = (
            f"[{repr(sut)}] Cannot process an object of type `InvalidType` - `{str(invalid_value)}`"
        )

        with pytest.raises(TypeError) as err_1:
            sut._validate_type(invalid_value)
        assert str(err_1.value) == expected_err_msg

        with pytest.raises(TypeError) as err_2:
            sut._validate_type(invalid_value, exact_match=True)
        assert str(err_2.value) == expected_err_msg

    def test_validate_type_valid(self, sut: TypeProjection):
        assert_does_not_throw(sut._validate_type, self.type())
        assert_does_not_throw(sut._validate_type, self.type(), True)

    def test_validate_type_derived_with_exact_match(self, sut: TypeProjection):
        derived_type = gen_derived_type(self.type)
        derived_value = derived_type()
        with pytest.raises(TypeError) as err:
            sut._validate_type(derived_value, exact_match=True)

        assert (
            str(err.value)
            == f"[{repr(sut)}] Cannot process an object of type `{derived_type.__name__}` - `{str(derived_value)}`"
        )


@pytest.mark.parametrize("t", TYPES, ids=[f"t={t.__name__}" for t in TYPES])
def test_projection_builder(t: type):
    value = TYPE_VALS[t]
    proj = TYPE_PROJECTIONS[t]

    sut = projection(t, proj)
    assert sut == TypeProjection(t, proj)
    assert sut(value) == proj(value)

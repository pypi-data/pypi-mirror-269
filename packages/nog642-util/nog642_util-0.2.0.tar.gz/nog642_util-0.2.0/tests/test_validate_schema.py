#!/usr/bin/env python3
from typing import Optional, Union

import pytest

from nog642_util import (StrEnum, validate_schema, Nullable, SchemaValueError, SchemaTypeError,
                         SchemaDefinitionError)


def test_empty_str():
    assert validate_schema(
        data='',
        schema=str
    ) is None  # success


def test_nonempty_str():
    assert validate_schema(
        data='test',
        schema=str
    ) is None  # success


def test_nonempty_nullable_str():
    assert validate_schema(
        data='test',
        schema=Nullable(str)
    ) is None  # success


def test_nullable_str():
    assert validate_schema(
        data=None,
        schema=Nullable(str)
    ) is None  # success


def test_none_str_against_nullable_int():
    with pytest.raises(SchemaTypeError):
        validate_schema(
            data='None',
            schema=Nullable(int)
        )


def test_str_against_int():
    with pytest.raises(SchemaTypeError):
        validate_schema(
            data='test',
            schema=int
        )


def test_invalid_dict_schema():
    with pytest.raises(SchemaDefinitionError):
        validate_schema(
            data={},
            # this is not a valid schema
            schema={}
        )


def test_empty_dict():
    assert validate_schema(
        data={},
        # this is not a valid schema
        schema=dict
    ) is None  # success


def test_explicit_empty_dict():
    assert validate_schema(
        data={},
        schema=(dict, 'explicit', {})
    ) is None  # success


def test_explicit_dict_schema_missing_required():
    with pytest.raises(SchemaDefinitionError):
        validate_schema(
            data={},
            # this is not a valid schema, because keys of the explicit dict need to be
            #     ('required', ...) or ('optional', ...)
            schema=(dict, 'explicit', {'a': int})
        )


def test_nullable_explicit_dict():
    assert validate_schema(
        data=None,
        schema=Nullable((dict, 'explicit', {'a': ('required', int)}))
    ) is None  # success


def test_explicit_dict():
    assert validate_schema(
        data={'a': 5},
        schema=Nullable((dict, 'explicit', {'a': ('required', int)}))
    ) is None  # success


def test_nullable_explicit_dict_against_empty_str():
    with pytest.raises(SchemaTypeError):
        validate_schema(
            data='',
            schema=Nullable((dict, 'explicit', {'a': ('required', int)}))
        )


def test_nonempty_explicit_dict_against_empty_dict():
    with pytest.raises(SchemaValueError):
        validate_schema(
            data={},
            schema=(dict, 'explicit', {'a': ('required', int)})
        )


def test_explicit_dict_optional_key():
    assert validate_schema(
        data={},
        schema=(dict, 'explicit', {'a': ('optional', int)})
    ) is None  # success


def test_explicit_dict_key_type_failure():
    with pytest.raises(SchemaTypeError):
        validate_schema(
            data={'a': None},
            schema=(dict, 'explicit', {'a': ('required', int)})
        )


def test_explicit_dict_key_type_success():
    assert validate_schema(
        data={'a': 5},
        schema=(dict, 'explicit', {'a': ('required', int)})
    ) is None  # success


def test_explicit_dict_required_nullable_key():
    assert validate_schema(
        data={'a': None},
        schema=(dict, 'explicit', {'a': ('required', Nullable(int))})
    ) is None  # success


def test_explicit_dict_required_nullable_int_key_against_empty_dict():
    with pytest.raises(SchemaValueError):
        validate_schema(
            data={},
            schema=(dict, 'explicit', {'a': ('required', Nullable(int))})
        )


class TestEnum(StrEnum):
    __test__ = False  # not a test case
    enum_value_a = 'enum_value_a'
    enum_value_b = 'enum_value_b_str'


def test_explicit_dict_required_enum_key_invalid_str():
    with pytest.raises(SchemaValueError):
        validate_schema(
            data={'a': 'invalid'},
            schema=(dict, 'explicit', {'a': ('required', TestEnum)})
        )


def test_explicit_dict_required_enum_key_against_int():
    with pytest.raises(SchemaTypeError):
        validate_schema(
            data={'a': 5},
            schema=(dict, 'explicit', {'a': ('required', TestEnum)})
        )


def test_explicit_dict_required_enum_key():
    assert validate_schema(
        data={'a': TestEnum.enum_value_a},
        schema=(dict, 'explicit', {'a': ('required', TestEnum)})
    ) is None  # success


def test_explicit_dict_required_enum_key_valid_str():
    assert validate_schema(
        data={'a': TestEnum.enum_value_b.value},
        schema=(dict, 'explicit', {'a': ('required', TestEnum)})
    ) is None  # success


def test_explicit_dict_required_nullable_enum():
    assert validate_schema(
        data={'a': None},
        schema=(dict, 'explicit', {'a': ('required', Nullable(TestEnum))})
    ) is None  # success


def test_explicit_dict_required_union_str_int_against_str():
    assert validate_schema(
        data={'a': 'test'},
        schema=(dict, 'explicit', {'a': ('required', Union[str, int])})
    ) is None  # success


def test_explicit_dict_required_union_str_int_against_int():
    assert validate_schema(
        data={'a': 5},
        schema=(dict, 'explicit', {'a': ('required', Union[str, int])})
    ) is None  # success


def test_explicit_dict_required_union_str_int_failure():
    with pytest.raises(SchemaTypeError):
        validate_schema(
            data={'a': []},
            schema=(dict, 'explicit', {'a': ('required', Union[str, int])})
        )


def test_explicit_dict_required_typing_optional_str_against_list():
    with pytest.raises(SchemaTypeError):
        validate_schema(
            data={'a': []},
            schema=(dict, 'explicit', {'a': ('required', Optional[str])})
        )


def test_explicit_dict_required_typing_optional_str_against_null():
    assert validate_schema(
        data={'a': None},
        schema=(dict, 'explicit', {'a': ('required', Optional[str])})
    ) is None  # success


def test_explicit_dict_required_typing_optional_str_against_str():
    assert validate_schema(
        data={'a': 'test'},
        schema=(dict, 'explicit', {'a': ('required', Optional[str])})
    ) is None  # success


def test_explicit_dict_required_union_str_enum_against_invalid_str():
    assert validate_schema(
        data={'a': 'invalid'},
        schema=(dict, 'explicit', {'a': ('required', Union[TestEnum, str])})
    ) is None  # success


def test_explicit_dict_required_union_int_enum_against_invalid_str():
    with pytest.raises(SchemaTypeError):
        validate_schema(
            data={'a': 'invalid'},
            schema=(dict, 'explicit', {'a': ('required', Union[TestEnum, int])})
        )


# def test_explicit_dict_typeerror():
#     with pytest.raises(SchemaDefinitionError):
#         advanced_validate_schema(
#             data={},
#             schema=(dict, 'explicit', {'a', int})
#         )

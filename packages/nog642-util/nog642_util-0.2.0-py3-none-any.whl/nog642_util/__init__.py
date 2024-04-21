#!/usr/bin/env python3
from __future__ import annotations

from collections.abc import Collection, Sequence
from enum import Enum, EnumMeta
import inspect
import json
import sys
import traceback
import typing
from typing import FrozenSet
from typing import get_origin as typing_get_origin
from typing import get_args as typing_get_args


class _StrEnumMeta(EnumMeta):
    _StrEnum__member_set: FrozenSet[StrEnum]

    def __new__(metacls, name, bases, attrs):
        cls = EnumMeta.__new__(metacls, name, bases, attrs)
        if len(cls) > 0:  # if the class has any members
            member_set_attr_name = '_StrEnum__member_set'
            if hasattr(cls, member_set_attr_name):
                raise ValueError(f'StrEnum cannot define value __value_set; '
                                 f'already defined as {getattr(cls, member_set_attr_name)}')
            setattr(cls, member_set_attr_name, frozenset(cls.__members__.values()))
        return cls

    def __contains__(cls, item):
        if isinstance(item, cls):
            return True
        return item in cls._StrEnum__member_set


class StrEnum(str, Enum, metaclass=_StrEnumMeta):
    """
    To be used for basic string enums.

    Major change is that enum instances now compare equal to the string value,
    as opposed to plain enums (because of the str mixin).

    Whether a string is a valid enum can be checked using the `in` operator on
    the class directly.

    Example usage:
    >>> class Example(StrEnum):
    ...     abc = 'abc'
    ...     XYZ = 'xyz'
    ...
    >>> Example.XYZ == 'xyz'
    True
    >>> 'xyz' in Example
    True
    >>> Example('xyz')
    <Example.XYZ: 'xyz'>
    >>> isinstance(Example.XYZ, str)
    True
    """


def get_full_traceback() -> str:
    """
    traceback.format_exc() does not give the functions above the function where it is called (whereas an exception
    bubbled all the way up would). This function does the same thing but gives the full traceback.
    """
    etype, exc, tb = sys.exc_info()
    if exc is None:
        raise ValueError('There is no exception')

    try:
        tb_exc = traceback.TracebackException(etype, exc, tb)

        # get the default traceback
        traceback_list = list(tb_exc.format())

        # try to find where the last exception begins
        traceback_str = 'Traceback (most recent call last):\n'
        for i, entry in enumerate(reversed(traceback_list)):
            if entry == traceback_str:
                break
        else:
            # traceback format is not as expected. return default
            print('WARNING: unexpected traceback format found by get_full_traceback', file=sys.stderr)
            return ''.join(traceback_list)

        # cut out the last exception. we will regenerate this one with a full traceback
        traceback_str = ''.join(traceback_list[:-(i + 1)]) + traceback_str

        try:
            outer_frames = inspect.getouterframes(tb.tb_frame)
        except Exception:
            # probably at outermost level
            outer_frames = list()

        for _, filename, lineno, function, code_context, _ in outer_frames[:0:-1]:
            traceback_str += f'  File "{filename}", line {lineno}, in {function}\n'
            for line in code_context:
                traceback_str += '    ' + line.lstrip()

        for _, filename, lineno, function, code_context, _ in inspect.getinnerframes(tb):
            traceback_str += f'  File "{filename}", line {lineno}, in {function}\n'
            for line in code_context:
                traceback_str += '    ' + line.lstrip()

        # get the actual exception message. remove the trailing newline.
        traceback_str += ''.join(tb_exc.format_exception_only())[:-1]

    except Exception as e:
        # this should not happen, but maybe there is some edge case; better not to have it crash just in case
        print('WARNING: error in get_full_traceback, returning possibly incomplete stack trace.'
              f'Error was: {e}', file=sys.stderr)
        return ''.join(traceback.format_exception(etype, exc, tb))

    return traceback_str


class SchemaError(Exception):
    """
    raised by validate_schema
    """


class SchemaTypeError(TypeError, SchemaError):
    pass


class SchemaValueError(ValueError, SchemaError):
    pass


class SchemaDefinitionError(Exception):
    pass


class Nullable:
    """
    To be used with validate_schema.
    Nullable(schema) will be the same as schema except it can also be None.
    """
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f'Nullable({self.value!r})'


def _plain_type_check(data, data_type, qualname) -> bool:
    """
    Utility method of validate_schema.
    Handles typing.Union (and typing.Optional, which is an alias for typing.Union).
    Does not handle typing.Union inside typing.Union, because that can be flattened.
    :param data:
    :param data_type:
    :return:
    :raises SchemaValueError: in special cases, see below
    """
    # support Union and Optional typing
    if typing_get_origin(data_type) is typing.Union:
        for t in typing_get_args(data_type):
            try:
                if _plain_type_check(data, t, qualname=qualname):
                    return True
            except SchemaValueError:
                pass
        return False

    # support strings counting as StrEnum values
    # and add additional input checks for the definition being processed (data_type must be a type)
    try:
        subclass_check_result = issubclass(data_type, StrEnum)
    except TypeError as e:
        raise SchemaDefinitionError(f"Expected {data_type!r} to be a python type, found {type(data_type)}, it's "
                                    f'likely you are passing some of the parameters in your schema definition '
                                    f'in the wrong order where this is defined!') from e
    if subclass_check_result:
        if (not isinstance(data, data_type)) and isinstance(data, str):
            # try converting to an enum first
            try:
                data = data_type(data)
            except Exception as e:
                raise SchemaValueError(f'{qualname} must be a member of {data_type.__qualname__}: '
                                       f'one of {set(data_type)}, not {data!r}') from e

    return isinstance(data, data_type)


def validate_schema(data, schema, qualname='data'):
    """
    qualname is the name of the data passed in. It is used to generate error messages.

    TODO: support explicit tuples

    A valid schema can take the following forms, where sub_schema is itself a valid schema:
    - python_type (including typing.Union)
    - Nullable(sub_schema)
    - (python_type, 'custom', custom_handler)
    - (dict, 'explicit', {
        'example_key1': ('required', sub_schema),
        'example_key2': ('optional', sub_schema)
      })
    - (dict, 'keyvalue', (
        sub_schema, sub_schema
      ))
    - (list, 'items', sub_schema)
    - (set, 'items', sub_schema)

    python_type represents a python type to be checked with isinstance.
    custom_handler is a function taking the data as the first argument and the qualname of that
        data as the second argument, and returns (not raises) either an exception or None. The
        purpose of returning instead of raising is to allow the use of lambdas.

    (dict, 'explicit', {}) is for when the dictionary has a fixed set of keys that are explicitly
        defined. Each key needs to specify if it is required or optional (meaning it can be missing,
        but if it is present it needs to match the schema). Note that optional here is not the same
        as nullable. A required key can be nullable and an optional key can be non-nullable.
    (dict, 'keyvalue', (sub_schema, sub_schema)) is for when the dictionary has an arbitrary/dynamic
        set of keys. Here, you define the schemas for the keys and the values in the form
        (key_schema, value_schema). Often key_schema will just be str.
    (list, 'items', sub_schema) and (set, 'items', sub_schema) are for when you want to define a
        schema for each item in a collection. Any collection (i.e. a subclass of collections.abc.Collection)
        will work here, not just list or set.

    StrEnum is supported. If the schema is a subclass of StrEnum, it will accept both enum instances
        and the corresponding strings as valid values. Regular python enums are not supported yet (they
        are just checked with isinstance).

    :param data:
    :param schema:
    :param qualname: name of the data passed in. It is used to generate error messages.
    :return:
    """
    if isinstance(schema, Nullable):
        if data is None:
            return  # schema validation success
        # data is not None, so get the actual schema and continue
        schema = schema.value
    if isinstance(schema, tuple):
        data_type = schema[0]

        if not _plain_type_check(data, data_type, qualname=qualname):
            raise SchemaTypeError(f'{qualname} must be of type {data_type} not {type(data)}')
        validation_type = schema[1]

        if validation_type == 'custom':
            result = schema[2](data, qualname)
            if result is not None:
                raise result

        elif issubclass(data_type, dict):
            if validation_type == 'explicit':
                undefined = object()  # sentinel value
                for key, value_schema_tuple in schema[2].items():
                    if isinstance(key, str):
                        key_str = json.dumps(key)
                    else:
                        key_str = repr(key)
                    try:
                        required, value_schema = value_schema_tuple
                    except Exception as e:
                        raise SchemaDefinitionError(f'Bad schema: value schemas for explicit dict '
                                                    f'{qualname}[{key_str}] must be tuples of form '
                                                    f"('required', schema) or ('optional', schema), "
                                                    f'not {value_schema_tuple!r}') from e
                    if required == 'required':
                        try:
                            value = data[key]
                        except KeyError as e:
                            raise SchemaValueError(f'{qualname} missing required key: {key_str}') from e
                    elif required == 'optional':
                        if key in data:
                            value = data[key]
                        else:
                            value = undefined
                    else:
                        raise ValueError('Bad schema: first item in explicit schema tuples for '
                                         f"{qualname} values must be 'required' or 'optional', not "
                                         f'{required}')
                    if value is not undefined:
                        validate_schema(value, value_schema, qualname=f'{qualname}[{key_str}]')

            elif validation_type == 'keyvalue':
                key_schema, value_schema = schema[2]
                for key, value in data.items():
                    validate_schema(key, key_schema, qualname=f'{qualname} keys')
                    if isinstance(key, str):
                        key_str = json.dumps(key)
                    else:
                        key_str = repr(key)
                    validate_schema(value, value_schema, qualname=f'{qualname}[{key_str}]')

            else:
                raise ValueError(f'Bad schema: {qualname} dict validation type must '
                                 f"be 'explicit', 'keyvalue', or 'custom', not {validation_type!r}")

        elif issubclass(data_type, Collection):
            if validation_type == 'items':
                item_schema = schema[2]
                if issubclass(data_type, Sequence):
                    for i, item in enumerate(data):
                        validate_schema(item, item_schema, qualname=f'{qualname}[{i}]')
                else:
                    for item in data:
                        validate_schema(item, item_schema, qualname=f'{qualname} item')

            else:
                raise ValueError(f'Bad schema: {qualname} non-dict collection validation type must '
                                 f"be 'items' or 'custom', not {validation_type!r}")

        else:
            raise ValueError(f'Bad schema: {qualname}: non-custom tuple validation is not '
                             f'available for type {data_type}')
    else:
        if not _plain_type_check(data, schema, qualname=qualname):
            raise SchemaTypeError(f"{qualname} must be of type {schema} not {type(data)}")

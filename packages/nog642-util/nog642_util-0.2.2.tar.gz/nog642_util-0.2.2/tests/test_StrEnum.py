#!/usr/bin/env python3
from nog642_util import StrEnum


class TestEnum(StrEnum):
    __test__ = False  # not a test case
    a = 'a'
    b = 'b_str'


def test_string_equality_matching_name():
    assert TestEnum.a == 'a'


def test_string_equality_nonmatching_name():
    assert TestEnum.b == 'b_str'


def test_string_inequality_nonmatching_name():
    assert TestEnum.b != 'b'


def test_membership_check_enum_instance():
    assert TestEnum.a in TestEnum
    assert TestEnum.b in TestEnum


def test_membership_check_matching_name():
    assert 'a' in TestEnum


def test_membership_check_nonmatching_name_value():
    assert 'b_str' in TestEnum


def test_membership_check_nonmatching_name_name():
    assert 'b' not in TestEnum


def test_membership_check_invalid_value():
    assert 'invalid' not in TestEnum

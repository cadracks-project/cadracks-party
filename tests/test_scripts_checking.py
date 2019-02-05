#!/usr/bin/env python
# coding: utf-8

r"""Tests for the scripts_checking module"""

import pytest
from os.path import join, dirname, isdir
from cadracks_party.scripts_checking import check_script,\
    check_all_scripts_from_library_jsons


def test_check_all_scripts_lib_ok():
    ok, _ = check_all_scripts_from_library_jsons(
        join(dirname(__file__), "scripts/sample_lib_ok"))
    assert ok is True


def test_check_all_scripts_lib_missing():
    r"""A script that should have been generated is missing"""
    missing_part_folder = join(dirname(__file__), "scripts/sample_lib_missing")
    assert isdir(missing_part_folder)
    ok, all_errors = check_all_scripts_from_library_jsons(missing_part_folder)
    assert ok is False
    assert len(all_errors.keys()) == 1


def test_invalid_file():
    with pytest.raises(IOError):
        _, _ = check_script(join(dirname(__file__), "scripts/unknown.py"))


def test_valid_script():
    ok, errors = check_script(join(dirname(__file__), "scripts/valid.py"))
    assert ok is True
    assert len(errors) == 0


def test_invalid_script_part_not_defined():
    ok, errors = check_script(join(dirname(__file__),
                                   "scripts/invalid_part_not_defined.py"))
    assert ok is False
    assert len(errors) == 1


def test_invalid_script_part_is_none():
    ok, errors = check_script(join(dirname(__file__),
                                   "scripts/invalid_part_is_none.py"))
    assert ok is False
    assert len(errors) == 1


def test_invalid_script_anchors_not_defined():
    ok, errors = check_script(join(dirname(__file__),
                                   "scripts/invalid_anchors_not_defined.py"))
    assert ok is False
    assert len(errors) == 1


def test_invalid_script_anchors_is_none():
    ok, errors = check_script(join(dirname(__file__),
                                   "scripts/invalid_anchors_is_none.py"))
    assert ok is False
    assert len(errors) == 1


def test_invalid_script_anchors_not_a_dict():
    ok, errors = check_script(join(dirname(__file__),
                                   "scripts/invalid_anchors_not_a_dict.py"))
    assert ok is False
    assert len(errors) == 1


def test_invalid_script_part_and_anchors_not_defined():
    ok, errors = check_script(
        join(dirname(__file__),
             "scripts/invalid_part_and_anchors_not_defined.py"))
    assert ok is False
    assert len(errors) == 2

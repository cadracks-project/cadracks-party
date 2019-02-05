#!/usr/bin/env python
# coding: utf-8

r"""Parts library checks"""

import sys
import json
import logging

if sys.version_info[0] < 3:
    PY2 = True
else:
    PY2 = False

logger = logging.getLogger(__name__)


def check_library_json_rules(json_filename):
    r"""Check that the entries in the 'data' field of a library respect the
    rules defined in the 'rules' field of the library

    Parameters
    ----------
    json_filename : str
        Path to the JSON file that describes the parts library

    Returns
    -------
    tuple(bool, errors)
        bool : True if the library is OK, False otherwise
        errors : dict (keys: part_identifier, values: list of broken rules)

    Raises
    ------
    NameError if the rules definition contain wrong identifiers
    SyntaxError if there is a syntax error in the rules definition

    """
    with open(json_filename) as data_file:
        json_file_content = json.load(data_file)

    library_ok = True
    errors = dict()

    string_types = (unicode, str) if PY2 else str

    for part_id, part_values in json_file_content["data"].items():
        # assign the values to a Python variable with the same name
        for dict_entry_key, dict_entry_value in part_values.items():
            # if type(dict_entry_value) not in [unicode, str]:
            # if not isinstance(dict_entry_value, (unicode, str)):

            if not isinstance(dict_entry_value, string_types):
                instruction = "%s = %s" % (dict_entry_key, dict_entry_value)
            else:
                instruction = "%s = '%s'" % (dict_entry_key, dict_entry_value)
            exec(instruction)

        for rule in json_file_content["rules"]:
            # instruction = "bool_ = %s" % rule
            # logger.info("Checking '%s' for part %s" % (rule, part_id))
            try:
                if PY2:
                    instruction = "bool_ = %s" % rule
                    exec(instruction)
                else:
                    bool_ = eval(rule)

                if bool_ is True:
                    # logger.info("OK")
                    pass
                else:
                    library_ok = False
                    if part_id not in errors.keys():
                        errors[part_id] = list()
                    errors[part_id].append(rule)
                    logger.error("Library data definition error")
            except NameError:
                library_ok = False
                if part_id not in errors.keys():
                    errors[part_id] = list()
                errors[part_id].append(rule)
                logger.error("Rules definition error (NameError)")

    return library_ok, errors


def check_library_units_definition(json_filename):
    r"""Test that each field of a data entry is referenced in the 'units'
    section of the library.json file

    Parameters
    ----------
    json_filename : str
        Path to the JSON file that describes the parts library

    Returns
    -------
    tuple(bool, errors)
        bool : True if the library is OK, False otherwise
        errors : dict (keys: part_identifier, values: list of broken rules)

    """

    library_ok = True
    errors = dict()

    fields = list()

    with open(json_filename) as data_file:
        json_file_content = json.load(data_file)

    for unit, definition in json_file_content["metadata"]["units"].items():
        try:
            for field in definition[1]:
                if field not in fields:
                    fields.append(field)
                else:
                    library_ok = False
                    if "units definition" not in errors.keys():
                        errors["units definition"] = list()
                    errors["units definition"].append("field '%s' is duplicated" % str(field))
        except IndexError:
            library_ok = False
            if "units definition" not in errors.keys():
                        errors["units definition"] = list()
            errors["units definition"].append("Improperly defined units : %s " % str(unit))

    for part_id, part_values in json_file_content["data"].items():
        for dict_entry_key in part_values.keys():
            if dict_entry_key in fields or \
                            dict_entry_key in ["description", "generator"]:
                pass
            else:
                library_ok = False
                if part_id not in errors.keys():
                    errors[part_id] = list()
                errors[part_id].append("field '%s' not defined in units" % dict_entry_key)
                logger.error("Library data definition error")

    return library_ok, errors


def check_library_fields(json_filename):
    r"""Check that every entry in the 'data' section if the library JSON
    file has the same fields (order does not matter)

    Parameters
    ----------
    json_filename : str
        Path to the JSON file that describes the parts library

    Returns
    -------
    tuple(bool, errors, set_)
        bool : True if the library is OK, False otherwise
        errors : dict (keys: part_identifier, values: list of broken rules)
        set_ : reference set of fields

    """
    library_ok = True
    errors = dict()

    reference_set_of_fields = set()

    with open(json_filename) as data_file:
        json_file_content = json.load(data_file)

    # Populate the reference set of fields
    feed = True  # Hackish way to only consider the first dictionary entry

    # Issue #7
    # test_missing_field : check_library_fields
    # finds 8 reference fields (10 expected)
    # The determination of the set of reference fields must be deterministic
    # This is why the data items are sorted
    for part_id, part_values in sorted(json_file_content["data"].items()):
        if feed is True:
            for dict_entry_key in part_values.keys():
                reference_set_of_fields.add(dict_entry_key)
        feed = False

    logger.info("Reference set of fields : %s" % str(reference_set_of_fields))

    # Check the set of fields in the data section
    # against the reference set of fields
    for part_id, part_values in json_file_content["data"].items():
        current_set_of_fields = set()
        for dict_entry_key in part_values.keys():
            current_set_of_fields.add(dict_entry_key)

        if current_set_of_fields == reference_set_of_fields:
            pass
        else:
            library_ok = False
            current_minus_ref = current_set_of_fields.difference(reference_set_of_fields)
            ref_minus_current = reference_set_of_fields.difference(current_set_of_fields)
            errors[part_id] = current_minus_ref.union(ref_minus_current)

    return library_ok, errors, reference_set_of_fields


def check_all(json_filename):
    r"""Perform every possible test on the library

    Parameters
    ----------
    json_filename : str
        Path to the JSON file that describes the parts library

    Returns
    -------
    tuple(bool, errors)
        bool : True if the library is OK, False otherwise
        errors : dict (keys: part_identifier, values: list of broken rules)

    """
    logger.info("Checking the library %s  ..." % json_filename)
    ok_rules, errors_rules = check_library_json_rules(json_filename)
    ok_units, errors_units = check_library_units_definition(json_filename)
    ok_fields, errors_fields, _ = check_library_fields(json_filename)

    ok = all(list_element is True for list_element in [ok_rules, ok_units, ok_fields])

    if ok is True:
        logger.info("...done - All OK")
    else:
        logger.error("ERROR(S) in the library %s" % json_filename)
        logger.info("rules ok : %s" % str(ok_rules))
        logger.info("units ok : %s" % str(ok_units))
        logger.info("fields ok : %s" % str(ok_fields))

    return ([ok_rules, ok_units, ok_fields],
            [errors_rules, errors_units, errors_fields])

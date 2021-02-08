#!/usr/bin/env python
# coding: utf-8

# Copyright 2018-2019 Guillaume Florent, Thomas Paviot, Bernard Uguen

# This file is part of cadracks-party.
#
# cadracks-party is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# any later version.
#
# cadracks-party is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with cadracks-party.  If not, see <https://www.gnu.org/licenses/>.

r"""Checks for scripts generated from a library.json"""

# import imp
import importlib.util
import os
import json

from ccad.model import Solid


def check_script(script_path):
    r"""Check that a script generated from a library.json file respect some
    criteria like:
    - having a 'part' variable that is a NotNull Solid
    - having an anchors variable that is a dict

    Parameters
    ----------
    script_path : str
        Path to the Python geometry script

    Returns
    -------
    tuple(bool, errors)
        bool : True if the library is OK, False otherwise
        errors : dict (keys: part_identifier, values: list of broken rules)

    Raises
    ------
    IOError : if script_path points to a nonexistent file

    """

    script_ok = True
    errors = list()
    spec = importlib.util.spec_from_file_location(script_path, script_path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    # mod = imp.load_source(script_path, script_path)

    # part variable checks
    if hasattr(mod, "part"):
        if mod.part is None:
            script_ok = False
            errors.append("part variable is None")
        else:
            if mod.part.shape.IsNull():
                script_ok = False
                errors.append("part variable is Null")
            else:
                if not isinstance(mod.part, Solid):
                    script_ok = False
                    errors.append("part variable is not a Solid")
    else:
        script_ok = False
        errors.append("geometry script has no 'part' attribute")

    # anchors variable checks
    if hasattr(mod, "anchors"):
        if mod.anchors is None:
            script_ok = False
            errors.append("anchors variable is None")
        else:
            if not isinstance(mod.anchors, dict):
                script_ok = False
                errors.append("anchors variable is not a dict")
    else:
        script_ok = False
        errors.append("geometry script has no 'anchors' attribute")

    return script_ok, errors


def check_all_scripts_from_library_jsons(folder_path):
    r"""Check every geometry script found in a folder

    Parameters
    ----------
    folder_path : str

    Returns
    -------
    bool, dict

    """
    scripts_ok = True
    all_errors = dict()

    # TODO : raise an error if no library in subfolders structure
    for item in os.walk(folder_path):
        if "library.json" in item[2]:
            with open("%s/%s" % (item[0], "library.json")) as data_file:
                json_file_content = json.load(data_file)

            for part_id, _ in json_file_content["data"].items():
                try:
                    script_path = os.path.join(item[0], "scripts/%s.py" % part_id)
                    script_ok, errors = check_script(script_path)
                    if script_ok is False:
                        scripts_ok = False
                        all_errors["%s/%s" % (item[0], "library.json")] = {part_id: errors}
                except IOError:
                    scripts_ok = False
                    all_errors["%s/%s" % (item[0], "library.json")] = \
                        {part_id: "No script for %s" % part_id}

    return scripts_ok, all_errors

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

r"""Unique geometry script generation logic from a JSON parts library file"""

# import imp
import importlib.util
import logging
import json
import codecs
from os import remove, walk
from os.path import join, splitext, dirname, basename

from aocxchange.step import StepExporter
from aocxchange.stl import StlExporter

from cadracks_party.templating import reconstruct_script_code_template, render
from cadracks_party.library_checking import check_library_json_rules
from cadracks_party.commons import create_folder


logger = logging.getLogger(__name__)


def _scripts_folder(folder_path):
    return join(folder_path, "scripts")


def _steps_folder(folder_path):
    return join(folder_path, "steps")


def _stls_folder(folder_path):
    return join(folder_path, "stls")


def _htmls_folder(folder_path):
    return join(folder_path, "htmls")


def _svgs_folder(folder_path):
    return join(folder_path, "svgs")


def _generate_script(json_generators, scripts_folder, part_id, context_):
    r"""Generate the Python geometry script for a given part_id

    Parameters
    ----------
    json_generators : dict
        Geometry generation code (key: generator id; value: lines of code)
    scripts_folder : str
        The folder where the script should be written
    part_id : str
        part id
    context_ : dict
        Values linked to the part_id

    Returns
    -------
    str : the path to the created Python geometry file

    """
    with open("tmp.py", "w") as tmp_file:
        tmp_file.write(reconstruct_script_code_template(
            json_generators[context_["generator"]]))

    # Use tmp.py as a template for context_ and write the results to the
    # part script
    py_geometry_file = join(scripts_folder, "%s.py" % part_id)
    with open(py_geometry_file, 'w') as f:
        f.write(render("tmp.py", context_))
    remove("tmp.py")

    return py_geometry_file


def _generate_cad(output_folder, py_geometry_file, output_format):
    if output_format not in ["step", "stl", "html"]:
        raise ValueError
    spec = importlib.util.spec_from_file_location(py_geometry_file, py_geometry_file)
    py_geometry_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(py_geometry_module)
    # py_geometry_module = imp.load_source(py_geometry_file, py_geometry_file)
    shape = py_geometry_module.__shape__
    part_id = splitext(basename(py_geometry_file))[0]
    part_id = str(part_id)  # Keeps the OCC STEP Writer happy !

    if output_format == "step":
        # part.to_step(join(output_folder, "%s.stp" % part_id))
        exporter = StepExporter(filename=join(output_folder, "%s.stp" % part_id))
        exporter.add_shape(shape)
        exporter.write_file()
    elif output_format == "stl":
        # part.to_stl(join(output_folder, "%s.stl" % part_id))
        exporter = StlExporter(filename=join(output_folder, "%s.stl" % part_id))
        exporter.set_shape(shape)
        exporter.write_file()
    # elif output_format == "html":
    #     part.to_html(join(output_folder, "%s.html" % part_id))
    else:
        msg = "Unknown export format"
        logger.error(msg)
        raise ValueError(msg)


def generate(json_library_filepath,
             generate_steps=False,
             generate_stls=False,
             # generate_htmls=False,
             generate_svgs=False):
    r"""Create a geometry generation script for each part defined
    in the PJSON file passed as a parameter

    Parameters
    ----------
    json_library_filepath : str
        The path to the PJSON file describing the parts library
    generate_steps : bool
    generate_stls : bool

    generate_svgs : bool
        Should the SVG drawings embedded in the PJSON file be extracted

    Raises
    ------
    KeyError

    """
    # Get the path of the JSON file passed as a parameter
    base_folder = dirname(json_library_filepath)
    scripts_folder = _scripts_folder(folder_path=base_folder)

    create_folder(scripts_folder)

    # Deal with folder creation only one (i.e. not in the loop)
    if generate_steps:
        steps_folder = _steps_folder(base_folder)
        create_folder(steps_folder)
    if generate_stls:
        stls_folder = _stls_folder(base_folder)
        create_folder(stls_folder)
    # if generate_htmls:
    #     htmls_folder = _htmls_folder(base_folder)
    #     create_folder(htmls_folder)
    if generate_svgs:
        svgs_folder = _svgs_folder(base_folder)
        create_folder(svgs_folder)

    with open(json_library_filepath) as data_file:
        json_file_content = json.load(data_file)

    if generate_svgs:
        for drawing_id, drawing_content in \
                json_file_content["drawings"].items():
            with codecs.open(join(svgs_folder, "%s.svg" % drawing_id),
                             'w',
                             'utf-8') as svg_file:
                for line in drawing_content:
                    svg_file.write("%s\n" % line.replace("'", "\"").replace("@simple_quote@", "'"))

    json_generators = json_file_content["generators"]

    # Check data is not empty
    for part_id, context_ in json_file_content["data"].items():
        py_geometry_file = _generate_script(json_generators, scripts_folder,
                                            part_id, context_)
        if generate_steps:
            _generate_cad(steps_folder, py_geometry_file, output_format="step")
        if generate_stls:
            _generate_cad(stls_folder, py_geometry_file, output_format="stl")
        # if generate_htmls:
        #     _generate_cad(htmls_folder, py_geometry_file, output_format="html")


def generate_all(base_folder,
                 preview=False,
                 generate_steps=False,
                 generate_stls=False):
    r"""For each folder containing a JSON parts library definition:
    - check the JSON file is OK
    - if so, generate the geometry scripts

    Parameters
    ----------
    base_folder : str
        The root folder from which to generate
    preview : bool
        If True, do everything but creating the geometry scripts
        If False, also generate the geometry scripts
    generate_steps : bool
    generate_stls : bool

    """
    for item in walk(base_folder):
        if "library.json" in item[2]:
            json_filename_ = join(item[0], "library.json")
            logger.info("Library filename : %s" % json_filename_)
            logger.info("Checking the rules for the library JSON ...")
            ok, errors = check_library_json_rules(json_filename=json_filename_)
            if ok:
                logger.info("... done. Rules are OK")
                logger.info("Creating the Python scripts from the library "
                            "JSON ...")
                if preview is False:
                    generate(json_library_filepath=json_filename_,
                             generate_steps=generate_steps,
                             generate_stls=generate_stls)
                logger.info("... done")
            else:
                logger.error("The library contains errors, please "
                             "correct these before generating the scripts")
                print(errors)

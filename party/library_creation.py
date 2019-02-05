#!/usr/bin/env python
# coding: utf-8

r"""The library_creation.py module contains standard mechanisms to create a
library.json file from standard templates

Currently implemented:

- alias mechanism : replace aliases by the values they refer to
- generator code : replace the {{ generators }} tag in the template by the code
found in the generators subdirectory
- drawings : the {{ drawings }} tag is replaced by the content of svg files
in the drawings subdirectory

Every function has a file_in and a file_out parameter that can be used by
the specific library.json creation routines as required

"""

import sys
import json
import codecs
from os import remove, listdir
from os.path import join, dirname, basename, splitext
import logging
import copy
# from ast import literal_eval

from collections import OrderedDict

from party.templating import render, generators_to_json_string, \
    svg_to_json_string
from party.commons import create_folder

if sys.version_info[0] < 3:
    PY2 = True
else:
    PY2 = False

logger = logging.getLogger(__name__)


def create_skeleton(base_folder):
    r"""Create a skeleton for a parts library project

    Parameters
    ----------
    base_folder : str
        The path to the base folder of the library

    """

    folder_name = basename(base_folder)

    # Create the base folder if it does not exist
    create_folder(base_folder)

    # Build the paths for subdirectories
    generators_folder_path = join(base_folder, "generators")
    drawings_folder_path = join(base_folder, "drawings")

    # Create the subdirectories if they do not exist
    create_folder(generators_folder_path)

    create_folder(drawings_folder_path)

    # Create the path to a sample generator
    # that will be named after the base directory name
    sample_generator_path = join(generators_folder_path, "%s.py" % folder_name)

    # Path for the library template
    sample_library_template_path = join(base_folder, "library_template.json")

    # Path for sample scripts that:
    # - create the library from the template
    # - use the template once created
    # sample_create_path = join(base_folder, "create_library.py")
    # sample_use_path = join(base_folder, "use_library.py")

    # Write a script in the sample generator that creates a cylinder geometry
    with open(sample_generator_path, 'w') as gen:
        gen.write('r"""Generation script for %s"""\n' % folder_name)
        gen.write("\n")
        gen.write("from ccad.model import cylinder\n")
        gen.write("\n")
        gen.write("radius = {{ radius }}\n")
        gen.write("length = {{ length }}\n")
        gen.write("\n")
        gen.write("part = cylinder(radius, length)\n")
        gen.write('anchors = {1: {"position": (0., 0., 0.), '
                  '"direction": (0., 0., -1.)},\n')
        gen.write('           2: {"position": (0., 0., length), '
                  '"direction": (0., 0., 1.)}}\n')

    # Write the sample template with:
    # - 2 entries in the data section
    # - 2 rules (radius and length strictly positive)
    # - a nomenclature
    with open(sample_library_template_path, 'w') as template:
        template.write("{\n")
        template.write('  "metadata":{\n')
        template.write('    "name": "%s",\n' % folder_name)
        template.write('    "description": "<please complete>",\n')
        template.write('    "nomenclature": "\'cylinder_\' + str(2*radius) + '
                       '\'x\' + str(int(length))",\n')
        template.write('    "units": {\n')
        template.write('      "length": ["mm", ["radius", "length"]],\n')
        template.write('      "force": ["N", []],\n')
        template.write('      "weight": ["g", []]\n')
        template.write('    },\n')
        template.write('    "authors": ["<author 1>", "<author 2>"],\n')
        template.write('    "url": "https://github.com/<please complete>",\n')
        template.write('    "license": "GPL v3"\n')
        template.write('  },\n')
        template.write('  "generators":\n')
        template.write('    { {{ generators }} },\n')
        template.write('  "rules": ["radius > 0", "length > 0"],\n')
        template.write('  "aliases": {},\n')
        template.write('  "data":{\n')
        template.write('    "part_id_1": {\n')
        template.write('      "description": "Part number 1",\n')
        template.write('      "generator": "%s",\n' % folder_name)
        template.write('      "radius": 10.0,\n')
        template.write('      "length": 20.0\n')
        template.write('    },\n')
        template.write('    "part_id_2": {\n')
        template.write('      "description": "Part number 2",\n')
        template.write('      "generator": "%s",\n' % folder_name)
        template.write('      "radius": 10.0,\n')
        template.write('      "length": 40.0\n')
        template.write('    }\n')
        template.write('  },\n')
        template.write('  "drawings":\n')
        template.write('    { {{ drawings }} }\n')
        template.write('}\n')

    # Write the script that will create the PJSON library from the template
    # with open(sample_create_path, 'w') as create:
    #     create.write("#!/usr/bin/env python\n")
    #     create.write("# coding: utf-8\n")
    #     create.write("\n")
    #     create.write('r"""Script that creates the library.json file for '
    #                  'the %s"""\n' % folder_name)
    #     create.write("\n")
    #     create.write("import logging\n")
    #     create.write("\n")
    #     create.write("from party.library_creation import autocreate_library\n")
    #     create.write("from party.library_checking import check_all\n")
    #     create.write("\n")
    #     create.write("logging.basicConfig(level=logging.DEBUG,\n")
    #     create.write("                    format='%(asctime)s :: %"
    #                  "(levelname)6s :: '\n")
    #     create.write("                           '%(module)20s :: %(lineno)3d "
    #                  ":: %(message)s')\n")
    #     create.write("\n")
    #     create.write('autocreate_library("library_template.json")\n')
    #     create.write('library_ok_list, _ = check_all("library.json")\n')
    #     create.write("for entry in library_ok_list:\n")
    #     create.write("    assert entry is True\n")

    # Write the script that will use the PJSON library, once created, to create
    # CAD files and HTML files
    # with open(sample_use_path, 'w') as use:
    #     use.write("#!/usr/bin/env python\n")
    #     use.write("# coding: utf-8\n")
    #     use.write("\n")
    #     use.write('r"""Example use of the library.json file to create '
    #               'geometry_scripts \n')
    #     use.write('and cad files"""\n')
    #     use.write("\n")
    #     use.write("import logging\n")
    #     use.write("from os.path import join, dirname\n")
    #     use.write("\n")
    #     use.write("from party.library_use import generate\n")
    #     use.write("\n")
    #     use.write("\n")
    #     use.write("logging.basicConfig(level=logging.DEBUG,\n")
    #     use.write("                    format='%(asctime)s :: %"
    #               "(levelname)6s :: '\n")
    #     use.write("                           '%(module)20s :: %(lineno)3d :: %"
    #               "(message)s')\n")
    #     use.write("\n")
    #     use.write('generate(json_library_filepath=join(dirname(__file__), '
    #               '"library.json"),\n')
    #     use.write("         generate_steps=True, generate_stls=True, "
    #               "generate_htmls=True)\n")


def _analyze_template(template_file):
    r"""Analyze a parts library template file for certain features and report
    on their presence

    Parameters
    ----------
    template_file : str
        Path to the template file

    Returns
    -------
    dict : keys are features, values are bool (True if feature is present)

    """

    info = {"generators": False, "drawings": False, "aliases": False}

    with open(template_file) as f:
        content = f.readlines()

    for line in content:
        if "{{generators}}" in line or "{{ generators }}" in line:
            info["generators"] = True

        if "{{drawings}}" in line or "{{ drawings }}" in line:
            info["drawings"] = True

        if "__alias__" in line:
            info["aliases"] = True

    return info


def autocreate_library(template_file,
                       library_file_name="library.json",
                       delete_intermediate=True):
    r"""Automated parts library creation from a template file. The template
    processing is automated depending on the presence of certain features in
    the template

    Parameters
    ----------
    template_file : str
        Path to the template file
    library_file_name : str, optional (default is 'library.json')
        Name of the final library file
    delete_intermediate : bool, optional (default is True)
        Should the intermediate files for library creation be deleted

    """
    logger.info("Creating the library %s from its template ..." %
                library_file_name)

    # Analyze the template to determine which operations should be performed
    info = _analyze_template(template_file)

    # Report the operations to perform
    logger.info("template file has generators tag : %s" %
                str(info["generators"]))
    logger.info("template file has drawings tag : %s" %
                str(info["drawings"]))
    logger.info("template file has aliases : %s" % str(info["aliases"]))

    template_folder = dirname(template_file)

    # funcs pipeline contains the functions that should be called to create
    # the PJSON file from its template
    funcs_pipeline = list()
    if info["generators"] is True or info["drawings"] is True:
        funcs_pipeline.append(template_handle_tags)
    if info["aliases"]:
        funcs_pipeline.append(template_handle_aliases)

    for i, func in enumerate(funcs_pipeline):
        # last operation
        # can also be the first of there is only one
        if i == len(funcs_pipeline) - 1:
            if i == 0:
                input_ = template_file
            else:
                input_ = join(template_folder, "tmp_%i.json" % (i-1))
            func(input_, library_file_name)
            if delete_intermediate is True and i != 0:
                remove(join(template_folder, "tmp_%i.json" % (i-1)))
        # first operation
        # ignored if there is only one, it is handle in the first condition
        elif i == 0:
            func(template_file, join(template_folder, "tmp_0.json"))
        # any operation in between the first and the last
        else:
            func(join(template_folder, "tmp_%i.json" % (i - 1)),
                 join(template_folder, "tmp_%i.json" % i))
            if delete_intermediate is True:
                remove(join(template_folder, "tmp_%i.json" % (i - 1)))

    # Do in any case ...
    template_handle_nomenclature(library_file_name, library_file_name)

    logger.info("...done")


def template_handle_includes(file_in, file_out):
    r"""Replace includes found in a template file by the values they refer to

    Parameters
    ----------
    file_in : str
        Path to the input file (i.e. a template using includes)
    file_out : str
        The output file
        (i.e. a template with replaced includes or the final file)

    """
    # TODO : complete the include functionality
    with open(file_in) as fi:
        json_content = json.load(fi, object_pairs_hook=OrderedDict)

    json_includes = json_content["includes"]

    print(json_includes)  # just so that json_includes is used somewhere

    # Read the files declared in the includes

    # Create aliases from these files

    # Write the output file

    # with open(file_out, 'w') as fp:
    #     json.dump(json_content, fp, sort_keys=False, indent=2)


def template_handle_aliases(file_in, file_out):
    r"""Replace aliases found in a template file by the values they refer to

    Parameters
    ----------
    file_in : str
        Path to the input file (i.e. a template using aliases)
    file_out : str
        The output file
        (i.e. a template with replaced aliases or the final file)

    """
    with open(file_in) as fi:
        json_content = json.load(fi, object_pairs_hook=OrderedDict)

    json_aliases = json_content["aliases"]

    # Deal with the aliases
    # name is a string (the part identifier)
    # context_ is a dict
    for _, context_ in json_content["data"].items():
        # modify context with the alias mechanism
        while has_aliases(context_):
            for k, v in context_.items():
                if "__alias__" in str(v):
                    key_in_aliases = str(v).replace("__alias__", "")
                    for alias_key, alias_value in \
                            json_aliases[key_in_aliases].items():
                        context_[alias_key] = alias_value
                    # del context_[k]  # do not keep the alias link
                    context_[k] = context_[k].replace("__alias__", "")

    del json_content["aliases"]

    with open(file_out, 'w') as fp:
        json.dump(json_content, fp, sort_keys=False, indent=2)


def template_handle_tags(file_in, file_out):
    r"""Replace the {{ <tag> }} tag:
    - by geometry generation code using Python generator files in the
      generators subdirectory for the {{ generators }} tag
    - by svg content in the drawings subfolder for the {{ drawings }} tag

    Parameters
    ----------
    file_in : str
        Path to the input file
        (i.e. a template containing a {{ <tag> )} tag(s))
    file_out : str
        The output file
        (i.e. a template with replaced {{ <tag> }} tags or the final file)

    """
    context = dict()

    # -------- Deal with generator code --------
    generators = dict()

    generators_folder = join(dirname(file_in), "generators")

    # iterate over the files in the generators folder
    for generator_file in listdir(generators_folder):
        # use the file name without extension as the generator id
        generator_id = splitext(generator_file)[0]

        with open(join(generators_folder, generator_file)) as gf:
            generators[generator_id] = gf.readlines()

    context["generators"] = generators_to_json_string(generators)

    # -------- Deal with the drawings --------
    drawings = dict()

    drawings_folder = join(dirname(file_in), "drawings")

    # iterate over the files in the drawings folder
    for drawing_file in listdir(drawings_folder):
        # use the file name without extension as the drawing id
        drawing_id, _ = splitext(drawing_file)

        # SVG drawings files may (and certainly will) contain non-ascii
        # characters, hence the use of codecs
        with codecs.open(join(drawings_folder, drawing_file), 'r', 'utf-8') \
                as df:
            drawings[drawing_id] = df.readlines()

    context["drawings"] = svg_to_json_string(drawings)

    with codecs.open(file_out, 'w', 'utf-8') as fo:
        fo.write(render(file_in, context))


def has_aliases(d):
    r"""Checks if a dictionary has values with the __alias__ string

    Parameters
    ----------
    d : dict

    Returns
    -------
    bool

    """
    has_alias = False
    for _, v in d.items():
        if "__alias__" in str(v):
            has_alias = True
    return has_alias


def template_handle_nomenclature(file_in, file_out):
    r"""Replaces the part_ids by the nomenclature computed id

    Parameters
    ----------
    file_in : str
        Path to the input file
        (i.e. a template containing a {{ generators )} tag)
    file_out : str
        The output file
        (i.e. a template with replaced {{ generators }} tag or the final file)

    """
    with open(file_in) as fi:
        json_content = json.load(fi, object_pairs_hook=OrderedDict)

    string_types = (unicode, str) if PY2 else str

    # Avoid RuntimeError in Python3 by modifying a copy
    # of the iterated OrderedDict
    json_content_copy = copy.deepcopy(json_content)

    try:
        nomenclature_string = json_content["metadata"]["nomenclature"]

        for part_id, part_values in json_content["data"].items():
            for var, value in part_values.items():
                if not isinstance(value, string_types):
                    exec("%s = %s" % (var, value))
                else:
                    exec("%s = '%s'" % (var, value))

            if part_id != eval(nomenclature_string):
                # json_content["data"][eval(nomenclature_string)] = part_values
                # del json_content["data"][part_id]
                json_content_copy["data"][eval(nomenclature_string)] = part_values
                del json_content_copy["data"][part_id]
            else:
                pass  # do nothing, everything is fine

        with open(file_out, 'w') as fp:
            # json.dump(json_content, fp, sort_keys=False, indent=2)
            json.dump(json_content_copy, fp, sort_keys=False, indent=2)
    except KeyError:
        logger.warning("No nomenclature specified, using user input")

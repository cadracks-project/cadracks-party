#!/usr/bin/env python
# coding: utf-8

r"""Functions for templates handling"""

import os.path
from jinja2 import Environment, FileSystemLoader


def render(template_path, context):
    r"""Render a template using a context

    Parameters
    ----------
    template_path : str
        Full path to a template
    context : dict
        Dict used for template rendering

    Returns
    -------
    The template rendered with the context

    """
    path, filename = os.path.split(template_path)
    return Environment(loader=FileSystemLoader(path or './')).\
        get_template(filename).render(context)


def generators_to_json_string(generators_dict):
    r"""Transform a dictionary of generators (key = file name no extension;
    value = file content) to a json string

    Parameters
    ----------
    generators_dict : dict
        Dictionary of generators. The key is the file name without the
        extension; the value is the generator file content

    Returns
    -------
    str : the json string that will replace the {{ generators }} tag in
          library_template.json

    """
    # -> replace the generators_dict parameter name by something more generic
    json_ = list()
    length = len(generators_dict.keys())
    for i, (gen_id, content) in enumerate(generators_dict.items()):
        json_.append('"%s"' % gen_id)
        json_.append(' : ')
        json_.append('[')
        for k, line in enumerate(content):
            json_.append('"%s"' % line.replace("\n", "")
                         .replace("\"\"\"", "'''")
                         .replace("\\", "\\\\")
                         .replace("\"", "'"))

            if k != len(content) - 1:  # no comma separation if last line
                json_.append(",")
        # s += str(content)
        json_.append(']')

        if i != length - 1:  # no comma separation of last generator
            json_.append(",")

        json_.append('\n')
    return "".join(json_)


def svg_to_json_string(drawings_dict):
    r"""Transform a dictionary of SVG drawings (key = file name no extension;
    value = file content) to a json string

    Parameters
    ----------
    drawings_dict : dict
        Dictionary of SVG drawings. The key is the file name without the
        extension; the value is the drawing file content

    Returns
    -------
    str : the json string that will replace the {{ drawings }} tag in
          library_template.json

    """
    json_ = list()
    length = len(drawings_dict.keys())
    for i, (gen_id, content) in enumerate(drawings_dict.items()):
        json_.append('"%s"' % gen_id)
        json_.append(' : ')
        json_.append('[')
        for k, line in enumerate(content):
            json_.append('"%s"' % line.replace("\n", "")
                         # .replace("\"\"\"", "'''")
                         # .replace("\\", "\\\\")
                         .replace("'", "@simple_quote@")
                         .replace("\"", "'")
                         )

            if k != len(content) - 1:  # no comma separation if last line
                json_.append(",")
        # s += str(content)
        json_.append(']')

        if i != length - 1:  # no comma separation of last drawing
            json_.append(",")

        json_.append('\n')
    return "".join(json_)


def reconstruct_script_code_template(generator_code):
    r"""Reconstruct a valid Python code from the generator code stored in the
    JSON library definition file.

    Parameters
    ----------
    generator_code : list
        List of ccad python instructions (containing Jinja placeholders)

    Returns
    -------
    str : the reconstructed code, including import
    and an if __name__ == '__main__' idiom

    """
    code = list()
    code.append("#!/usr/bin/env python\n")
    code.append("# coding: utf-8\n\n")
    # code.append("from ccad.model import cylinder\n\n")
    code.append("\n".join(generator_code).replace("'''", "\"\"\"").replace("'", "\""))
    # code.append("\n\nif __name__ == '__main__':\n")
    # code.append("    import ccad.display as cd\n")
    # code.append("    v = cd.view()\n")
    # code.append("    v.display(part, color=(0.1, 0.1, 1.0), transparency=0.3)\n")
    # code.append("    for k, anchor in anchors.items():\n")
    # code.append("        v.display_vector(origin=anchor['position'], direction=anchor['direction'])\n")
    # code.append("    cd.start()\n\n")
    return "".join(code)

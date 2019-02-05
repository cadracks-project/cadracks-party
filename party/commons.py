#!/usr/bin/env python
# coding: utf-8

r"""commons.py module

Gathers functions used in more than 1 module

"""

from os import mkdir, makedirs
from os.path import isdir
import logging
import errno

logger = logging.getLogger(__name__)


def mkdir_p(path):
    r"""mkdir -p in Python

    Parameters
    ----------
    path

    """
    try:
        makedirs(path)
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise


def create_folder(folder_path):
    r"""Create the folder if it does not exist

    Parameters
    ----------
    folder_path : str
        Path to the folder to create

    """
    if not isdir(folder_path):
        mkdir(folder_path)
        logger.info("Creating %s folder" % folder_path)
    else:
        logger.info("Folder %s already exists" % folder_path)

    #     mkdir_p(folder_path)
    #     logger.info("Creating %s folder" % folder_path)
    # else:
    #     logger.info("Folder %s already exists" % folder_path)


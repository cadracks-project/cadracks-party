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


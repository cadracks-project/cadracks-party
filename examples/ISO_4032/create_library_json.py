#!/usr/bin/python
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

r"""Script that creates the library.json file for the ISO 4032 standard"""


import logging
from party.library_creation import autocreate_library
from party.library_checking import check_all

logger = logging.getLogger(__name__)


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s :: %(levelname)6s :: '
                               '%(module)20s :: %(lineno)3d :: %(message)s')

    logger.info("Creating the library JSON from its template ...")
    autocreate_library("library_template.json")
    logger.info("...done")

    logger.info("Checking the library JSON  ...")
    library_ok_list, _ = check_all("library.json")
    ok = all(list_element is True for list_element in library_ok_list)
    if ok is True:
        logger.info("...done - All OK")
    else:
        logger.error("ERROR(S) in the library JSON")
        logger.info("rules ok : %s" % str(library_ok_list[0]))
        logger.info("units ok : %s" % str(library_ok_list[1]))
        logger.info("fields ok : %s" % str(library_ok_list[2]))

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

r"""Example of initing a parts library project by generating a skeleton"""

import os
import logging

from cadracks_party.library_creation import create_skeleton

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s :: %(levelname)6s :: '
                           '%(module)20s :: %(lineno)3d :: %(message)s')

create_skeleton(os.path.join(os.path.dirname(__file__), "new_library"))

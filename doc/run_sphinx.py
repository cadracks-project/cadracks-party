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

r"""Generate the sphinx documentation"""

from os.path import join, dirname
from os import getcwd, chdir
from subprocess import call


folders = {"source": join(dirname(__file__), "source"),
           "build": join(dirname(__file__), "build")}

# Run sphinx
cwd = getcwd()
chdir(folders["source"])
call(["ls", "-l"])
call("sphinx-apidoc -f -o ./ %s" % join(dirname(__file__), "../cadracks_party/cadracks_party"))
call("sphinx-build -b html %s %s" % (folders["source"], folders["build"]))
chdir(cwd)

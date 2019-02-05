#!/usr/bin/env python
# coding: utf-8**

"""setuptools based setup module"""

from setuptools import setup
# from setuptools import find_packages
# To use a consistent encoding
import codecs
from os import path

import party

here = path.abspath(path.dirname(__file__))

# Get the long description from the README_SHORT file
with codecs.open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()


setup(
    name=party.__name__,
    version=party.__version__,
    description=party.__description__,
    long_description=long_description,
    url=party.__url__,
    download_url=party.__download_url__,
    author=party.__author__,
    author_email=party.__author_email__,
    license=party.__license__,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6'],
    keywords=['OpenCascade', 'PythonOCC', 'ccad', 'CAD', 'parts', 'json'],
    packages=['party', ],
    install_requires=[],  # OCC, scipy and wx cannot be installed via pip
    extras_require={
        'dev': [],
        'test': ['pytest', 'coverage'],
    },
    package_data={},
    data_files=[],
    entry_points={},
    scripts=['bin/party-skeleton', 'bin/party-create', 'bin/party-use']

    )

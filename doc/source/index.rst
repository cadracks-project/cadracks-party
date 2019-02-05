.. party documentation master file, created by
   sphinx-quickstart on Fri May  5 16:07:47 2017.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

party
=====

Plain text (JSON) parts libraries for open hardware projects.

WARNING : **party** is currently in *work in progress* status

**party** aims at creating and handling parts libraries defined in a single text (JSON) file where the metadata, the data, the
geometry creation logic and the *anchors* creation logic are defined.

The *anchors* concept is a set of vectors attached to a part geometry that can be used to place the part in an assembly.

.. figure:: _static/iso4032_nut_m2.5_screenshot.PNG
   :scale: 100 %
   :alt: ISO 4032 M2.5 Nut from a parts library file (the small yellow arrow represents the anchor)

   ISO 4032 M2.5 Nut from a parts library file (the small yellow arrow represents the anchor)


Contents:

.. toctree::
   :maxdepth: 2

   part_libraries
   party_presentation
   pljson_file_format
   assembling_pljson
   using_pljson

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`


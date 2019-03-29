Project Usage
================

 - Create a virtual environment
 - Activate it
 - Make data
 - Run notebooks

Make
~~~~~~~~~
The Makefile contains the central entry points for common tasks related to this project.

+---------------------+-----------------------------------------------------------------------------------------------+
| Command             | Description                                                                                   |
+=====================+===============================================================================================+
| clean               | Delete all compiled Python files (does not remove created data files)                         |
+---------------------+-----------------------------------------------------------------------------------------------+
| notebooks           | Run notebooks and output rst to docs (RUN BEFORE DOCS)                                        |
+---------------------+-----------------------------------------------------------------------------------------------+
| create_environment  | Set up python interpreter environment. Creates a virtual environment for project development. |
+---------------------+-----------------------------------------------------------------------------------------------+
| data                | Make Dataset. Downloads the food atlas data and parses it into pickles of pandas data frames. |
+---------------------+-----------------------------------------------------------------------------------------------+
| docs                | Make Docs. Output in HTML format in docs/html. Index link will be printed                     |
+---------------------+-----------------------------------------------------------------------------------------------+
| lint                | Lint using flake8                                                                             |
+---------------------+-----------------------------------------------------------------------------------------------+
| requirements        | Install Python Dependencies                                                                   |
+---------------------+-----------------------------------------------------------------------------------------------+
| test_environment    | Test python environment is setup correctly                                                    |
+---------------------+-----------------------------------------------------------------------------------------------+

Notebooks
~~~~~~~~~~

.. toctree::
    :glob:

    notebooks/*

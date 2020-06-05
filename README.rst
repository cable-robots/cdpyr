========
Overview
========

A Python 3 package for designing, analyzing, and simulating cable-driven parallel robots.

* Free software: European Union Public Licence V. 1.2

Installation
============

::

    pip install cdpyr

You can also install the in-development version with::

    pip install https://gitlab.com/cable-robots/cdpyr/-/archive/master/cdpyr-master.zip


Documentation
=============


https://cdpyr.readthedocs.io/


Development
===========

To run the all tests run::

    tox

Note, to combine the coverage data from all the tox environments run:

.. list-table::
    :widths: 10 90
    :stub-columns: 1

    - - Windows
      - ::

            set PYTEST_ADDOPTS=--cov-append
            tox

    - - Other
      - ::

            PYTEST_ADDOPTS=--cov-append tox

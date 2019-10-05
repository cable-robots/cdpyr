========
Overview
========

.. start-badges

.. list-table::
    :stub-columns: 1

    * - docs
      - |docs|
    * - tests
      - | |travis|
        |
    * - package
      - | |commits-since|
.. |docs| image:: https://readthedocs.org/projects/cdpyr/badge/?style=flat
    :target: https://readthedocs.org/projects/cdpyr
    :alt: Documentation Status

.. |travis| image:: https://api.travis-ci.org/cable-robots/cdpyr.svg?branch=master
    :alt: Travis-CI Build Status
    :target: https://travis-ci.org/cable-robots/cdpyr

.. |commits-since| image:: https://img.shields.io/github/commits-since/cable-robots/cdpyr/v1.0.dev0.svg
    :alt: Commits since latest release
    :target: https://github.com/cable-robots/cdpyr/compare/v1.0.dev0...master



.. end-badges

A Python 3 package for designing, analyzing, and simulating cable-driven parallel robots.

* Free software: BSD 3-Clause License

Installation
============

::

    pip install cdpyr

You can also install the in-development version with::

    pip install https://github.com/cable-robots/cdpyr/archive/master.zip


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

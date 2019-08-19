# -*- coding: utf-8 -*-

"""Top-level package for CDPyR."""

__author__ = 'Philipp Tempel'
__email__ = 'philipp.tempel@isw.uni-stuttgart.de'
__version__ = '1.0.0-dev'

from cdpyr import algorithms, attr, geometry, io, mechanics, motion, robot

__all__ = [
    'attr',
    'robot',
    'algorithms',
    'motion',
    'mechanics',
    'geometry',
    'io'
]

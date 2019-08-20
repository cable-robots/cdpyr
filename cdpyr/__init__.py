# -*- coding: utf-8 -*-

"""Top-level package for CDPyR."""

__author__ = 'Philipp Tempel'
__email__ = 'philipp.tempel@isw.uni-stuttgart.de'
__version__ = '1.0.0-dev'

from cdpyr import algorithms, geometry, io, mechanics, motion, robot, validators

__all__ = [
    'validators',
    'robot',
    'algorithms',
    'motion',
    'mechanics',
    'geometry',
    'io',
]

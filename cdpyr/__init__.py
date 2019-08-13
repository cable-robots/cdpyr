# -*- coding: utf-8 -*-

"""Top-level package for CDPyR."""

__author__ = 'Philipp Tempel'
__email__ = 'philipp.tempel@isw.uni-stuttgart.de'
__version__ = '1.0.0-dev'

from cdpyr import algorithms
from cdpyr import geometry
from cdpyr import mechanics
from cdpyr import motion
from cdpyr import robot

__all__ = [
    'robot',
    'algorithms',
    'motion',
    'mechanics',
    'geometry',
    'io'
]

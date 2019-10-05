# -*- coding: utf-8 -*-

"""Top-level package for CDPyR."""
from __future__ import annotations

__author__ = 'Philipp Tempel'
__email__ = 'p.tempel@tudelft.nl'
__version__ = '1.0.0-dev'

from cdpyr import validator
from cdpyr import mechanics
from cdpyr import geometry
from cdpyr import kinematics
from cdpyr import robot
from cdpyr import analysis
from cdpyr import motion
from cdpyr import stream
from cdpyr import schema

__all__ = [
    'analysis',
    'geometry',
    'kinematics',
    'mechanics',
    'motion',
    'robot',
    'schema',
    'stream',
    'validator',
]

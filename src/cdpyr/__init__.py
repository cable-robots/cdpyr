# -*- coding: utf-8 -*-

"""
Top-level package for CDPyR.
"""

# @formatter:off
from __future__ import annotations
from cdpyr import (
    # vital imports
    helpers,
    typing,
    mixin,
    exceptions,
    # actual CDPyR imports
    validator,
    mechanics,
    geometry,
    kinematics,
    robot,
    motion,
    analysis,
    # I/O imports
    stream,
    schema
)
# @formatter:on

__author__ = 'Philipp Tempel'
__email__ = 'p.tempel@tudelft.nl'
__version__ = '1.0.0-dev'

__all__ = [
        'analysis',
        'exceptions',
        'geometry',
        'helpers',
        'kinematics',
        'mechanics',
        'mixin',
        'motion',
        'robot',
        'schema',
        'stream',
        'typing',
        'validator',
]

# -*- coding: utf-8 -*-

"""
Top-level package for CDPyR.
"""

__author__ = 'Philipp Tempel'
__email__ = 'p.tempel@tudelft.nl'
__version__ = '1.0.0-dev'
__all__ = [
        'analysis',
        'exceptions',
        'geometry',
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

# @formatter:off
from cdpyr import (
    # vital imports
    helper,
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

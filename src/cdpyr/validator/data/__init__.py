from __future__ import annotations

from typing import AnyStr, Optional, Sized

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"


def length(value: Sized,
           expected: int,
           name: Optional[AnyStr] = None):
    if len(value) != expected:
        raise ValueError(
                'Expected `{}` to have {} element{}, got {} instead.'.format(
                        name if name is not None else 'value',
                        expected,
                        's' if expected > 1 else '',
                        len(value)
                ))

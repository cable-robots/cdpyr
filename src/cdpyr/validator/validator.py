from typing import Sequence, Union

import numpy as np_

from cdpyr.typing import Num, Vector, Matrix


def nonzero(value: Union[Num, Vector, Sequence[Num]], name: str = None):
    value = np_.asarray(value)
    if np_.any(value == 0):
        raise ValueError(
            'Expected `{}` to be {}nonzero.'.format(
                name if name is not None else 'value',
                'all ' if value.size > 1 else ''
            )
        )


def negative(value: Union[Num, Vector, Sequence[Num]], name: str = None):
    value = np_.asarray(value)
    if np_.any(value >= 0):
        raise ValueError(
            'Expected `{}` to be {}negative.'.format(
                name if name is not None else 'value',
                'all ' if value.size > 1 else ''
            )
        )


def nonnegative(value: Union[Num, Vector, Sequence[Num]], name: str = None):
    value = np_.asarray(value)
    if np_.any(value < 0):
        raise ValueError(
            'Expected `{}` to be {}nonnegative.'.format(
                name if name is not None else 'value',
                'all ' if value.size > 1 else ''
            )
        )


def positive(value: Union[Num, Vector, Sequence[Num]], name: str = None):
    value = np_.asarray(value)
    if np_.any(value <= 0):
        raise ValueError(
            'Expected `{}` to be {}positive.'.format(
                name if name is not None else 'value',
                'all ' if value.size > 1 else ''
            )
        )


def nonpositive(value: Union[Num, Vector, Sequence[Num]], name: str = None):
    value = np_.asarray(value)
    if np_.any(value > 0):
        raise ValueError(
            'Expected `{}` to be {}positive.'.format(
                name if name is not None else 'value',
                'all ' if value.size > 1 else ''
            )
        )


def dimensions(value: Union[Num, Vector, Matrix, Sequence[Num]], expected: int, name: str = None):
    value = np_.asarray(value)
    if value.ndim != expected:
        raise ValueError(
            'Expected `{}` to have {} dimension{}, got {} instead.'.format(
                name if name is not None else 'value',
                expected,
                's' if expected > 1 else '',
                value.ndim
            )
        )


def shape(value: Union[Num, Vector, Matrix, Sequence[Num]], expected: Union[int, tuple], name: str = None):
    value = np_.asarray(value)
    if value.shape != expected:
        raise ValueError(
            'Expected `{}` to have shape {}, got {} instead.'.format(
                name if name is not None else 'value',
                expected,
                value.shape
            )
        )

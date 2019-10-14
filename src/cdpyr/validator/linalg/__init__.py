from typing import Union, Sequence

import numpy as np_

from cdpyr.typing import Num, Vector, Matrix
from cdpyr.validator.numeric import (
    greater_than_or_equal_to,
    less_than_or_equal_to,
    equal_to,
)


def dimensions(value: Union[Num, Vector, Matrix, Sequence[Num]], expected: int,
               name: str = None):
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


def shape(value: Union[Num, Vector, Matrix, Sequence[Num]],
          expected: Union[int, tuple],
          name: str = None):
    value = np_.asarray(value)
    if value.shape != expected:
        raise ValueError(
            'Expected `{}` to have shape {}, got {} instead.'.format(
                name if name is not None else 'value',
                expected,
                value.shape
            )
        )


def square(value: Union[Num, Vector, Matrix, Sequence[Num]], name: str = None):
    value = np_.asarray(value)

    try:
        dimensions(value, 2, name)
        n = value.shape[0]
        shape(value, (n, n), name)
    except ValueError as verr:
        raise ValueError(
            'Expected `{}` to be square.'.format(
                name if name is not None else 'value'
            )
        ) from verr


def symmetric(value: Union[Num, Vector, Matrix, Sequence[Num]],
              name: str = None):
    value = np_.asarray(value)

    try:
        square(value, name)
        if not np_.allclose(value - value.transpose(), 0):
            raise ValueError(
                'Expected `{}.T` to be equal to `{}`.'.format(
                    name if name is not None else 'value',
                    name if name is not None else 'value',
                )
            )
    except ValueError as verr:
        raise ValueError(
            'Expected `{}` to be symmetric.'.format(
                name if name is not None else 'value'
            )
        ) from verr


def inertia_tensor(value: Union[Sequence[Sequence[Num]], Matrix],
                   name: str = None):
    value = np_.asarray(value)

    try:
        dimensions(value, 2, name)
        shape(value, (3, 3), name)
        greater_than_or_equal_to(value.diagonal(), 0, 'diag({})'.format(
            name if name is not None else 'value'))
    except ValueError as verr:
        raise ValueError(
            'Expected `{}` to be a valid inertia tensor, but was not'.format(
                name if name is not None else 'value',
            )
        ) from verr


def rotation_matrix(value: Union[Sequence[Sequence[Num]], Matrix],
                    name: str = None):
    value = np_.asarray(value)

    try:
        dimensions(value, 2, name)
        shape(value, (3, 3), name)
        greater_than_or_equal_to(value, -1, name)
        less_than_or_equal_to(value, 1, name)
        equal_to(np_.abs(np_.linalg.det(value)), 1,
                 'det({})'.format(name if name is not None else 'value'))
    except ValueError as verr:
        raise ValueError(
            'Expected `{}` to be a valid rotation matrix, but was not.'.format(
                name if name is not None else 'value',
            )
        ) from verr


def unit_vector(value: Union[Sequence[Num], Vector], name: str = None):
    value = np_.asarray(value)

    try:
        dimensions(value, 1, name)
        equal_to(np_.linalg.norm(value), 1,
                 'norm({})'.format(name if name is not None else 'value'))
    except ValueError as verr:
        raise ValueError(
            'Expected `{}` to be a valid unit vector, but was not.'.format(
                name if name is not None else 'value',
            )
        ) from verr

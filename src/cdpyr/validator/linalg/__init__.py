from typing import AnyStr, Optional, Sequence, Union

import numpy as np_

from cdpyr.typing import Matrix, Num, Vector
from cdpyr.validator.numeric import equal_to, greater_than_or_equal_to

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"


def dimensions(value: Union[Num, Vector, Matrix, Sequence[Num]],
               expected: int,
               name: Optional[AnyStr] = None):
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
          name: Optional[AnyStr] = None):
    value = np_.asarray(value)
    if value.shape != expected:
        raise ValueError(
                'Expected `{}` to have shape {}, got {} instead.'.format(
                        name if name is not None else 'value',
                        expected,
                        value.shape
                )
        )


def square(value: Union[Num, Vector, Matrix, Sequence[Num]],
           name: Optional[AnyStr] = None):
    value = np_.asarray(value)

    try:
        dimensions(value, 2, name)
        n = value.shape[0]
        shape(value, (n, n), name)
    except ValueError as ValueE:
        raise ValueError(
                'Expected `{}` to be square.'.format(
                        name if name is not None else 'value'
                )
        ) from ValueE


def symmetric(value: Union[Num, Vector, Matrix, Sequence[Num]],
              name: Optional[AnyStr] = None):
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
    except ValueError as ValueE:
        raise ValueError(
                'Expected `{}` to be symmetric.'.format(
                        name if name is not None else 'value'
                )
        ) from ValueE


def inertia_tensor(value: Union[Sequence[Sequence[Num]], Matrix],
                   name: Optional[AnyStr] = None):
    value = np_.asarray(value)

    try:
        dimensions(value, 2, name)
        shape(value, (3, 3), name)
        greater_than_or_equal_to(value.diagonal(), 0, 'diag({})'.format(
                name if name is not None else 'value'))
    except ValueError as ValueE:
        raise ValueError(
                'Expected `{}` to be a valid inertia tensor, but was '
                'not'.format(
                        name if name is not None else 'value',
                )
        ) from ValueE


def rotation_matrix(value: Union[Sequence[Sequence[Num]], Matrix],
                    name: Optional[AnyStr] = None):
    value = np_.asarray(value)

    try:
        dimensions(value, 2, name)
        shape(value, (3, 3), name)
        # greater_than_or_equal_to(value, -1, name)
        # less_than_or_equal_to(value, 1, name)
        equal_to(np_.abs(np_.linalg.det(value)), 1,
                 'det({})'.format(name if name is not None else 'value'))
    except ValueError as ValueE:
        raise ValueError(
                'Expected `{}` to be a valid rotation matrix, but was '
                'not.'.format(
                        name if name is not None else 'value',
                )
        ) from ValueE


def space_coordinate(value: Union[Sequence[Sequence[Num]], Matrix],
                     name: Optional[AnyStr] = None):
    value = np_.asarray(value)

    try:
        dimensions(value, 1, name)
        shape(value, (3,), name)
    except ValueError as ValueE:
        raise ValueError(
                'Expected `{}` to be a valid space coordinate, but was '
                'not.'.format(
                        name if name is not None else 'value',
                )
        ) from ValueE


def unit_vector(value: Union[Sequence[Num], Vector],
                name: Optional[AnyStr] = None):
    value = np_.asarray(value)

    try:
        dimensions(value, 1, name)
        equal_to(np_.linalg.norm(value), 1,
                 'norm({})'.format(name if name is not None else 'value'))
    except ValueError as ValueE:
        raise ValueError(
                'Expected `{}` to be a valid unit vector, but was not.'.format(
                        name if name is not None else 'value',
                )
        ) from ValueE


def landspace(value: Union[Sequence[Num], Vector, Matrix],
              name: Optional[AnyStr] = None):
    value = np_.asarray(value)

    dimensions(value, 2, name)

    if value.shape[1] < value.shape[0]:
        raise ValueError(
                'Expected `{}` for be rectangular of landscape shape, '
                'but received a {} matrix.'.format(
                        name if name is not None else 'value',
                        value.shape
                )
        )


def portrait(value: Union[Sequence[Num], Vector, Matrix],
             name: Optional[AnyStr] = None):
    value = np_.asarray(value)

    dimensions(value, 2, name)

    if value.shape[0] < value.shape[1]:
        raise ValueError(
                'Expected `{}` for be rectangular of portrait shape, but received '
                'a {} matrix.'.format(
                        name if name is not None else 'value',
                        value.shape
                )
        )

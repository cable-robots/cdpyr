from typing import Sequence, Union

import numpy as np_

from cdpyr.typing import Matrix, Num, Vector


def nonzero(value: Union[Num, Vector, Sequence[Num]], name: str = None):
    value = np_.asarray(value)
    if (value == 0).any():
        raise ValueError(
            'Expected `{}` to be {}nonzero.'.format(
                name if name is not None else 'value',
                'all ' if value.size > 1 else ''
            )
        )


def negative(value: Union[Num, Vector, Sequence[Num]], name: str = None):
    value = np_.asarray(value)
    if (value >= 0).any():
        raise ValueError(
            'Expected `{}` to be {}negative.'.format(
                name if name is not None else 'value',
                'all ' if value.size > 1 else ''
            )
        )


def nonnegative(value: Union[Num, Vector, Sequence[Num]], name: str = None):
    value = np_.asarray(value)
    if (value < 0).any():
        raise ValueError(
            'Expected `{}` to be {}nonnegative.'.format(
                name if name is not None else 'value',
                'all ' if value.size > 1 else ''
            )
        )


def positive(value: Union[Num, Vector, Sequence[Num]], name: str = None):
    value = np_.asarray(value)
    if (value <= 0).any():
        raise ValueError(
            'Expected `{}` to be {}positive.'.format(
                name if name is not None else 'value',
                'all ' if value.size > 1 else ''
            )
        )


def nonpositive(value: Union[Num, Vector, Sequence[Num]], name: str = None):
    value = np_.asarray(value)
    if (value > 0).any():
        raise ValueError(
            'Expected `{}` to be {}positive.'.format(
                name if name is not None else 'value',
                'all ' if value.size > 1 else ''
            )
        )


def equal_to(value: Union[Num, Vector, Sequence[Num]],
             expected: Num,
             name: str = None,
             *args,
             **kwargs):
    value = np_.asarray(value)
    if not np_.allclose(value, expected, *args, **kwargs):
        raise ValueError(
            'Expected {}value{} of `{}` to be close to {}.'.format(
                'all ' if value.size > 1 else '',
                's' if value.size > 1 else '',
                name if name is not None else 'value',
                expected
            )
        )


def greater_than(value: Union[Num, Vector, Sequence[Num]],
                 expected: Num,
                 name: str = None):
    value = np_.asarray(value)
    if (value <= expected).any():
        raise ValueError(
            'Expected {}value{} of `{}` to be greater than {}.'.format(
                'all ' if value.size > 1 else '',
                's' if value.size > 1 else '',
                name if name is not None else 'value',
                expected
            )
        )


def greater_than_or_equal_to(value: Union[Num, Vector, Sequence[Num]],
                             expected: Num,
                             name: str = None):
    value = np_.asarray(value)
    if (value < expected).any():
        raise ValueError(
            'Expected {}value{} of `{}` to be greater than or equal to {'
            '}.'.format(
                'all ' if value.size > 1 else '',
                's' if value.size > 1 else '',
                name if name is not None else 'value',
                expected
            )
        )


def less_than(value: Union[Num, Vector, Sequence[Num]],
              expected: Num,
              name: str = None):
    value = np_.asarray(value)
    if (value >= expected).any():
        raise ValueError(
            'Expected {}value{} of `{}` to be less than {}.'.format(
                'all ' if value.size > 1 else '',
                's' if value.size > 1 else '',
                name if name is not None else 'value',
                expected
            )
        )


def less_than_or_equal_to(value: Union[Num, Vector, Sequence[Num]],
                          expected: Num,
                          name: str = None):
    value = np_.asarray(value)
    if (value > expected).any():
        raise ValueError(
            'Expected {}value{} of `{}` to be less than or equal {}.'.format(
                'all ' if value.size > 1 else '',
                's' if value.size > 1 else '',
                name if name is not None else 'value',
                expected
            )
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


def finite(value: Union[Num, Vector, Matrix, Sequence[Num]], name: str = None):
    value = np_.asarray(value)
    if np_.invert(np_.isfinite(value)).any():
        raise ValueError(
            'Expected `{}` to be finite, but was not.'.format(
                name if name is not None else 'value',
            )
        )


def nonnan(value: Union[Num, Vector, Matrix, Sequence[Num]], name: str = None):
    value = np_.asarray(value)
    if np_.isnan(value).any():
        raise ValueError(
            'Expected `{}` to be finite, but was not.'.format(
                name if name is not None else 'value',
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

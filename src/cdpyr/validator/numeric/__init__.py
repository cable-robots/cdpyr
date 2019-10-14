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

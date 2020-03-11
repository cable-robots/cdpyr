import pathlib as pl
from typing import AnyStr, Iterable, Mapping, Optional

from hurry.filesize import size as filesize

from cdpyr.helpers import conversion

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"

units = {"nsec": 1e-9, "usec": 1e-6, "msec": 1e-3, "sec": 1.0}


def format_time(dt,
                time_unit: Optional[AnyStr] = None,
                precision: Optional[int] = None):
    if isinstance(dt, Iterable):
        return [format_time(dt_, time_unit, precision) for dt_ in dt]

    unit = time_unit

    if unit is not None:
        scale = units[unit]
    else:
        scales = [(scale, unit) for unit, scale in units.items()]
        scales.sort(reverse=True)
        for scale, unit in scales:
            if dt >= scale:
                break

    return "%.*g %s" % (precision if precision is not None else 3,
                        dt / scale,
                        unit)


def full_classname(o: object):
    """

    References
    ----------
    .. [1] https://stackoverflow.com/questions/2020014/get-fully-qualified
    -class-name-of-an-object-in-python

    Parameters
    ----------
    o

    Returns
    -------

    """
    if isinstance(o, type):
        return ".".join([o.__module__, o.__name__])
    else:
        return ".".join([o.__class__.__module__, o.__class__.__name__])


def update_recursive(defaults: Mapping, update: Mapping):
    """
    Recursively update a dictionary.

    Parameters
    ----------
    defaults : Mapping
        Original data of which the base values are created.
    update : Mapping
        New data to push in to `defaults`. Any value in `update` will
        overwrite the corresponding value in `defaults. If `value` is a
        `Mapping`, this method recurses into the mapping.

    Returns
    -------
    merged : Mapping
        Resulting, recursively updated mapping.
    """
    for k, v in update.items():
        if isinstance(v, Mapping):
            defaults[k] = update_recursive(defaults.get(k, {}), v)
        else:
            defaults[k] = v
    return defaults


# data directory
DATADIR: pl.Path = (pl.Path(__file__).parent / '..' / 'data').resolve()

__all__ = [
        'DATADIR',
        'conversion',
        'format_time',
        'filesize',
        'full_classname',
        'update_recursive',
]

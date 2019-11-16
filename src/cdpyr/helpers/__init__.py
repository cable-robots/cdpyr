from typing import AnyStr, Optional

from hurry.filesize import size as filesize

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"
units = {"nsec": 1e-9, "usec": 1e-6, "msec": 1e-3, "sec": 1.0}


def format_time(dt,
                time_unit: Optional[AnyStr] = None,
                precision: Optional[int] = None):
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

    See Also
    --------
    https://stackoverflow.com/questions/2020014/get-fully-qualified-class-name-of-an-object-in-python

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


__all__ = [
    'format_time',
    'filesize',
    'full_classname',
]

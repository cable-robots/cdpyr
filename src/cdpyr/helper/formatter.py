from __future__ import annotations

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"
__all__ = [
        'filesize',
        'sane_string',
        'time',
        'units',
]

from typing import AnyStr, Iterable, Optional, Union

import hurry.filesize as filesize

units = {
        "nsec": 1e-9,
        "usec": 1e-6,
        "msec": 1e-3,
        "sec":  1.0
}


def time(dt: Union[float, Iterable[float]],
         time_unit: Optional[AnyStr] = None,
         precision: Optional[int] = None):
    if isinstance(dt, Iterable):
        return [time(dt_, time_unit, precision) for dt_ in dt]

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


def sane_string(s: str, keep: Iterable = None):
    """
    Create a sane string i.e., remove all non-alphanumeric characters

    Parameters
    ----------
    s : str
        Unsafe string to parse
    keep : Optional[Iterable]
        A sequence of additional characters to keep besides alphanumeric and the
        default (' ', '.', '_')

    Returns
    -------
    s : str
        A sane(r?) string
    """
    if keep is None:
        keep = (' ', '.', '_')

    return "".join(c for c in s if c.isalnum() or c in keep).rstrip()

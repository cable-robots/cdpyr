from __future__ import annotations

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"
__all__ = [
        'filesize',
        'time',
        'units',
]

from typing import AnyStr, Iterable, Optional

import hurry.filesize

filesize = hurry.filesize

units = {
        "nsec": 1e-9,
        "usec": 1e-6,
        "msec": 1e-3,
        "sec":  1.0
}


def time(dt,
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

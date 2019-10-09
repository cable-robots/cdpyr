from typing import AnyStr, Optional

from hurry.filesize import size as filesize

units = {"nsec": 1e-9, "usec": 1e-6, "msec": 1e-3, "sec": 1.0}


def format_time(dt, time_unit: Optional[AnyStr] = None, precision: int = None):
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


__all__ = [
    'format_time',
    'filesize',
]

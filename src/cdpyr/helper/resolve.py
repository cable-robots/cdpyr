from __future__ import annotations

__author__ = 'Philipp Tempel'
__email__ = 'p.tempel@tudelft.nl'
__all__ = [
        'full_classname',
]


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

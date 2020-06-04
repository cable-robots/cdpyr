from __future__ import annotations

__author__ = 'Philipp Tempel'
__email__ = 'p.tempel@tudelft.nl'
__all__ = [
        'update_recursive',
]

from typing import Mapping


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

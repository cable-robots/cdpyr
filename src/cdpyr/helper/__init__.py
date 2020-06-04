from __future__ import annotations

import pathlib as pl

from cdpyr.helper import data, formatter, magic_convert

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"
__all__ = [
        'formatter',
        'data',
        'magic_convert',
]

# data directory
DATADIR: pl.Path = (pl.Path(__file__).parent / '..' / 'data').resolve()

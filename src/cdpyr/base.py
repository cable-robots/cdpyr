from __future__ import annotations

__author__ = 'Philipp Tempel'
__email__ = 'p.tempel@tudelft.nl'
__all__ = [
        'Algorithm',
        'CdpyrObject',
        'Result',
]

from abc import ABC


class CdpyrObject(ABC):

    def __init__(self, *args, **kwargs):
        pass


class Algorithm(CdpyrObject):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Result(CdpyrObject):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

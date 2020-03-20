from __future__ import annotations

from abc import ABC

__author__ = 'Philipp Tempel'
__email__ = 'p.tempel@tudelft.nl'


class CdpyrObject(ABC):

    def __init__(self, *args, **kwargs):
        pass


class Algorithm(CdpyrObject):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Result(CdpyrObject):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


__all__ = [
        'Algorithm',
        'CdpyrObject',
        'Result',
]

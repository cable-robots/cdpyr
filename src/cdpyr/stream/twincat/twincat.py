from typing import Any, AnyStr, Dict, Tuple

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"


class Signal(object):
    bag: Dict[AnyStr, Any]

    def __init__(self, **kwargs):
        pass


class Scope(object):
    signals: Tuple['Signal']

    def __init__(self, signals: Tuple['Signal']):
        self.signals = signals


__all__ = [
        'Scope',
        'Signal',
]

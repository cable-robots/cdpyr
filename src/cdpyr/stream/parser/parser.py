from __future__ import annotations

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"
__all__ = [
        'Parser',
]

from abc import ABC, abstractmethod
from collections import OrderedDict
from typing import AnyStr, Mapping, Union

from cdpyr.base import Object
from cdpyr.robot.robot_component import RobotComponent


class Parser(Object, ABC):
    EXT = ''

    def kwargs(self, o: RobotComponent, **kwargs):
        return kwargs

    @abstractmethod
    def dumps(self, d: Union[OrderedDict, Mapping], *args, **kwargs) -> AnyStr:
        raise NotImplementedError()

    @abstractmethod
    def loads(self, s: AnyStr, *args, **kwargs) -> Union[OrderedDict, Mapping]:
        raise NotImplementedError()

from abc import ABC, abstractmethod
from collections import OrderedDict
from typing import AnyStr, Mapping, Union

from cdpyr.mixin.base_object import BaseObject
from cdpyr.robot.robot_component import RobotComponent

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"


class Parser(ABC, BaseObject):

    def kwargs(self, o: RobotComponent, **kwargs):
        return kwargs

    @abstractmethod
    def dumps(self, d: Union[OrderedDict, Mapping], *args, **kwargs) -> AnyStr:
        raise NotImplementedError()

    @abstractmethod
    def loads(self, s: AnyStr, *args, **kwargs) -> Union[OrderedDict, Mapping]:
        raise NotImplementedError()

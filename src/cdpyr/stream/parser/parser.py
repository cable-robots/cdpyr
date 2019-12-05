from abc import ABC, abstractmethod
from collections import OrderedDict
from typing import AnyStr, Union, Mapping

from cdpyr.robot.robot_component import RobotComponent


class Parser(ABC):

    def __init__(self, *args, **kwargs):
        pass

    def kwargs(self, o: RobotComponent, **kwargs):
        return kwargs

    @abstractmethod
    def dumps(self, d: Union[OrderedDict, Mapping], *args, **kwargs) -> AnyStr:
        raise NotImplementedError()

    @abstractmethod
    def loads(self, s: AnyStr, *args, **kwargs) -> Union[OrderedDict, Mapping]:
        raise NotImplementedError()

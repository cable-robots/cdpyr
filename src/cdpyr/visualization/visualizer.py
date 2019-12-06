from typing import Union

from cdpyr.analysis.result import PlottableResult
from cdpyr.mixin.base_object import BaseObject
from cdpyr.robot.robot_component import RobotComponent
from cdpyr.visualization.engine import engine as _engine

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"


class Visualizer(BaseObject):
    _engine: '_engine.Engine'

    def __init__(self, engine: '_engine.Engine', **kwargs):
        super().__init__(**kwargs)
        self._engine = engine

    @property
    def engine(self):
        return self._engine

    def close(self):
        self._engine.close()

    def draw(self, *args, **kwargs):
        self._engine.draw(*args, **kwargs)

    def reset(self):
        self._engine.reset()

    def show(self):
        self._engine.show()

    def render(self, obj: Union['RobotComponent', 'PlottableResult'], *args,
               **kwargs):
        return self._engine.render(obj, *args, **kwargs)


__all__ = [
        'Visualizer',
]

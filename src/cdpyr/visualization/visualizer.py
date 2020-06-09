from __future__ import annotations

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"
__all__ = [
        'Visualizer',
]

from typing import Union

from cdpyr.analysis.result import PlottableResult
from cdpyr.base import Object
from cdpyr.geometry.primitive import Primitive as GeometryPrimitive
from cdpyr.robot.robot_component import RobotComponent
from cdpyr.visualization.engine import engine as _engine_


class Visualizer(Object):
    _engine: _engine_.Engine

    def __init__(self, engine: _engine_.Engine, **kwargs):
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

    def render(self,
               obj: Union[RobotComponent, PlottableResult, GeometryPrimitive],
               *args,
               **kwargs):
        return self._engine.render(obj, *args, **kwargs)

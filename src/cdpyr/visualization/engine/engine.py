from __future__ import annotations

import itertools
from abc import ABC, abstractmethod
from typing import AnyStr, Callable, Dict, Union

import numpy as _np

from cdpyr import geometry as _geometry, robot as _robot
from cdpyr.analysis.kinematics import kinematics as _kinematics
from cdpyr.analysis.result import PlottableResult
from cdpyr.analysis.workspace import grid as _grid, hull as _hull
from cdpyr.base import Object
from cdpyr.geometry.primitive import Primitive as GeometryPrimitive
from cdpyr.helper.resolve import full_classname as fcn
from cdpyr.robot.robot_component import RobotComponent
from cdpyr.typing import Matrix, Vector

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"


class Engine(Object, ABC):
    AXES_NAMES = ('x', 'y', 'z')
    COORDINATE_DIRECTIONS = (
            (1.0, 0.0, 0.0),
            (0.0, 1.0, 0.0),
            (0.0, 0.0, 1.0),
    )
    COORDINATE_COLORS = (
            (1.0, 0.0, 0.0),
            (0.0, 1.0, 0.0),
            (0.0, 0.0, 1.0)
    )
    _NUMBER_OF_AXES: int
    _NUMBER_OF_COORDINATES: int

    _RESOLVER: Dict[
        AnyStr, Callable[
            [
                    Union[
                        RobotComponent,
                        PlottableResult,
                        GeometryPrimitive],
                    ...],
            None]
    ]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._RESOLVER = {
                fcn(_robot.Cable):                  self.render_cable,
                fcn(_robot.CableList):              self.render_cable_list,
                fcn(_robot.Drivetrain):             self.render_drivetrain,
                fcn(_robot.Drivetrain):             self.render_drum,
                fcn(_robot.Frame):                  self.render_frame,
                fcn(_robot.FrameAnchor): self.render_frame_anchor,
                fcn(_robot.FrameAnchorList):
                                                    self.render_frame_anchor_list,
                fcn(_robot.Gearbox):                self.render_gearbox,
                fcn(_geometry.Cuboid):              self.render_cuboid,
                fcn(_geometry.Cylinder):            self.render_cylinder,
                fcn(_geometry.Ellipsoid):           self.render_ellipsoid,
                fcn(_geometry.Polyhedron):          self.render_polyhedron,
                fcn(_geometry.Tube):                self.render_tube,
                fcn(_kinematics.Result):            self.render_kinematics,
                fcn(_robot.Robot):                  self.render_motor,
                fcn(_robot.Platform):      self.render_platform,
                fcn(_robot.PlatformList):  self.render_platform_list,
                fcn(_robot.PlatformAnchor):
                                           self.render_platform_anchor,
                fcn(_robot.PlatformAnchorList):
                                           self.render_platform_anchor_list,
                fcn(_robot.Pulley):        self.render_pulley,
                fcn(_robot.Robot):         self.render_robot,
                fcn(_grid.Result):         self.render_workspace_grid,
                fcn(_hull.Result):         self.render_workspace_hull,
        }

    @abstractmethod
    def close(self):
        raise NotImplementedError()

    @abstractmethod
    def draw(self, *args, **kwargs):
        raise NotImplementedError()

    @abstractmethod
    def reset(self):
        raise NotImplementedError()

    @abstractmethod
    def show(self):
        raise NotImplementedError()

    def render(self,
               o: Union[RobotComponent, PlottableResult, GeometryPrimitive],
               *args,
               **kwargs):
        KeyE1 = None
        # first, try to render the object with its designated renderer
        try:
            return self._RESOLVER[fcn(o)](o, *args, **kwargs)
        # failure, so let's see if the object can render with any of its
        # parent classes
        except KeyError as KeyE1:
            pass

        for parent in o.__class__.__mro__:
            try:
                return self._RESOLVER[fcn(parent)](o, *args, **kwargs)
            except KeyError as KeyE2:
                pass

        # if we got here, then the object could not be rendered in any way,
        # so we will explain that to the user
        raise KeyError(
                f'Unable to render object. Expected it to be any of '
                f'{", ".join(self._RESOLVER.keys())} but received {fcn(o)}.')

    @abstractmethod
    def render_cable(self, cable: _robot.Cable, *args, **kwargs):
        raise NotImplementedError()

    def render_cable_list(self, cable_list: _robot.CableList, *args,
                          **kwargs):
        for cable in cable_list:
            self.render(cable, *args, **kwargs)

    @abstractmethod
    def render_cuboid(self, cuboid: _geometry.Cuboid, *args, **kwargs):
        raise NotImplementedError()

    @abstractmethod
    def render_cylinder(self, cylinder: _geometry.Cylinder, *args, **kwargs):
        raise NotImplementedError()

    @abstractmethod
    def render_drivetrain(self, drivetrain: _robot.Drivetrain, *args,
                          **kwargs):
        raise NotImplementedError()

    @abstractmethod
    def render_drum(self, drum: _robot.Drum, *args, **kwargs):
        raise NotImplementedError()

    @abstractmethod
    def render_ellipsoid(self,
                         ellipsoid: _geometry.Ellipsoid,
                         *args, **kwargs):
        raise NotImplementedError()

    @abstractmethod
    def render_frame(self, frame: _robot.Frame, *args, **kwargs):
        raise NotImplementedError()

    @abstractmethod
    def render_frame_anchor(self,
                            anchor: _robot.FrameAnchor,
                            *args,
                            **kwargs):
        raise NotImplementedError()

    def render_frame_anchor_list(self,
                                 anchor_list: _robot.FrameAnchorList,
                                 *args,
                                 **kwargs):
        for anchor in anchor_list:
            self.render(anchor, *args, **kwargs)

    @abstractmethod
    def render_gearbox(self, gearbox: _robot.Gearbox, *args, **kwargs):
        raise NotImplementedError()

    @abstractmethod
    def render_kinematics(self, kinematics: _kinematics.Result, *args,
                          **kwargs):
        raise NotImplementedError()

    @abstractmethod
    def render_motor(self, motor: _robot.Motor, *args, **kwargs):
        raise NotImplementedError()

    @abstractmethod
    def render_platform(self, platform: _robot.Platform, *args, **kwargs):
        raise NotImplementedError()

    @abstractmethod
    def render_platform_anchor(self,
                               anchor: _robot.PlatformAnchor,
                               *args, **kwargs):
        raise NotImplementedError()

    def render_platform_anchor_list(self,
                                    anchor_list: _robot.PlatformAnchorList,
                                    *args, **kwargs):
        for anchor in anchor_list:
            self.render(anchor, *args, **kwargs)

    def render_platform_list(self, platform_list: _robot.PlatformList,
                             *args, **kwargs):
        for platform in platform_list:
            self.render(platform, *args, **kwargs)

    @abstractmethod
    def render_polyhedron(self, polyhedron: _geometry.Polyhedron, *args,
                          **kwargs):
        raise NotImplementedError()

    @abstractmethod
    def render_pulley(self, pulley: _robot.Pulley, *args, **kwargs):
        raise NotImplementedError()

    @abstractmethod
    def render_robot(self, robot: _robot.Robot, *args, **kwargs):
        raise NotImplementedError()

    @abstractmethod
    def render_tube(self, tube: _geometry.Tube, *args, **kwargs):
        raise NotImplementedError()

    @abstractmethod
    def render_workspace_grid(self, workspace: _grid.Result, *args,
                              **kwargs):
        raise NotImplementedError()

    @abstractmethod
    def render_workspace_hull(self, workspace: _hull.Result, *args,
                              **kwargs):
        raise NotImplementedError()

    def _render_component_list(self, obj: RobotComponent, name: str, *args,
                               **kwargs):
        # get user-defined plot styles for the component
        styles = kwargs.pop(name, {})
        # if the styles are not False, then plot the component
        if styles is not False:
            # turn dictionary of styles into list of styles to that it can be
            # repeated for each component
            if isinstance(styles, Dict):
                styles = [styles]

            # get the components to plot from the object
            components = getattr(obj, name)

            # cyclic repetition of styles for each component
            if len(styles) < len(components):
                styles = itertools.cycle(styles)

            # loop over each component with its style
            for idx, component, style in zip(range(len(components)), components,
                                             styles):
                self.render(component, *args, **style, **kwargs, loop_index=idx)

    def _extract_coordinates(self, coordinate: Union[Vector, Matrix]):
        """
        Convert any given (3,) coordinate into something that the plotting
        engine can understand for the current amount of axes

        Parameters
        ----------
        coordinate: Vector | None
            A `(3,X)` vector of entries or `None`. If `None`, defaults to `[
            0.0]` times the number of axes

        Returns
        -------
        coordinate: Vector
            A `(NA,X)` matrix of `_NUMBER_OF_AXES` coordinates which can be
            directly passed to the underlying matplotlib render call.

        """
        # anything into a numpy array
        coordinate = _np.asarray(coordinate)

        # scalars into vectors
        if coordinate.ndim == 0:
            coordinate = _np.asarray([coordinate])

        # turn vectors into matrices
        if coordinate.ndim == 1:
            coordinate = coordinate[:, _np.newaxis]

        # if the coordinate has less rows than the visualization needs, we will
        # add zeros at the bottom
        if coordinate.shape[0] < self._NUMBER_OF_AXES:
            coordinate = _np.pad(coordinate, (
                    (0, self._NUMBER_OF_AXES - coordinate.shape[0]),))

        # return result
        return coordinate[0:self._NUMBER_OF_AXES, :]

    def _extract_dcm(self, dcm: Union[Vector, Matrix]):
        """
        Convert any given (3,) coordinate into something that the plotting
        engine can understand for the current amount of axes

        Parameters
        ----------
        coordinate: Vector | None
            A `(3,X)` vector of entries or `None`. If `None`, defaults to `[
            0.0]` times the number of axes

        Returns
        -------
        coordinate: Vector
            A `(NA,X)` matrix of `_NUMBER_OF_AXES` coordinates which can be
            directly passed to the underlying matplotlib render call.

        """
        # anything into a numpy array
        dcm = _np.asarray(dcm)

        # check if it's a single dcm
        is_single = dcm.ndim == 2

        # turn vectors into matrices
        if is_single:
            dcm = dcm[:, :, _np.newaxis]

        # extract the data
        dcm = dcm[0:self._NUMBER_OF_AXES, 0:self._NUMBER_OF_AXES, :]

        # return single or all dcms
        return dcm[0] if is_single else dcm

    def _prepare_plot_coordinates(self, coordinates: Union[Vector, Matrix]):
        """
        Convert any given (3,) coordinate into something that the plotting
        engine can understand for the current amount of axes

        Parameters
        ----------
        coordinate: Vector | None
            A `(3,X)` vector of entries or `None`. If `None`, defaults to `[
            0.0]` times the number of axes

        Returns
        -------
        coordinate: Matrix
            `(NA,X)` matrix of `NA` coordinates of dimensions `X`

        """
        # anything into a numpy array
        coordinates = _np.asarray(coordinates)

        # scalars into vectors
        if coordinates.ndim == 0:
            coordinates = _np.asarray([coordinates])

        # turn vectors into matrices
        if coordinates.ndim == 1:
            coordinates = coordinates[:, _np.newaxis]

        return coordinates

    def _rgb2RGB(self, rgb: Union[Vector, Matrix]):
        """
        Convert RGB values in [0, 1] to values in [0, 255]

        Parameters
        ----------
        RGB : array_like | Vector | Matrix
            Array-like object of RGB values in the range of [0, 1]

        Returns
        -------
        rgb : array_like | Vector | Matrix
            Same type as input, yet values are scaled to lie in the range of
            [0, 255]
        """
        return type(rgb)(_np.asarray(rgb) * 255)

    def _RGB2rgb(self, rgb: Union[Vector, Matrix]):
        """
        Convert RGB values in [0, 255] to values in [0, 1]

        Parameters
        ----------
        rgb : array_like | Vector | Matrix
            Array-like object of RGB values in the range of [0, 255]

        Returns
        -------
        RGB : array_like | Vector | Matrix
            Same type as input, yet values are scaled to lie in the range of
            [0, 1]
        """
        return type(rgb)(_np.asarray(rgb) / 255)


__all__ = [
        'Engine',
]

import itertools
from abc import ABC, abstractmethod
from typing import AnyStr, Callable, Dict, Union

import numpy as _np

from cdpyr import geometry as _geometry
from cdpyr.analysis.kinematics import kinematics as _kinematics
from cdpyr.analysis.result import PlottableResult
from cdpyr.analysis.workspace import grid as _grid, hull as _hull
from cdpyr.helpers import full_classname as fcn
from cdpyr.robot import (
    cable as _cable,
    drivetrain as _drivetrain,
    drum as _drum,
    frame as _frame,
    gearbox as _gearbox,
    motor as _motor,
    platform as _platform,
    pulley as _pulley,
    robot as _robot
)
from cdpyr.robot.anchor import (
    frame_anchor as _frame_anchor,
    platform_anchor as _platform_anchor
)
from cdpyr.robot.robot_component import RobotComponent
from cdpyr.typing import Matrix, Vector

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"


class Engine(ABC):
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

    _RESOLVER: Dict[AnyStr, Callable]

    def __init__(self, *args, **kwargs):
        self._RESOLVER = {
                fcn(_cable.Cable):               self.render_cable,
                fcn(_cable.CableList):           self.render_cable_list,
                fcn(_drivetrain.DriveTrain):     self.render_drivetrain,
                fcn(_drum.Drum):                 self.render_drum,
                fcn(_frame.Frame):               self.render_frame,
                fcn(_frame_anchor.FrameAnchor):  self.render_frame_anchor,
                fcn(_frame_anchor.FrameAnchorList):
                                                 self.render_frame_anchor_list,
                fcn(_gearbox.Gearbox):           self.render_gearbox,
                fcn(_geometry.Cuboid):           self.render_cuboid,
                fcn(_geometry.Cylinder):         self.render_cylinder,
                fcn(_geometry.EllipticCylinder): self.render_elliptic_cylinder,
                fcn(_geometry.Sphere):           self.render_sphere,
                fcn(_geometry.Tube):             self.render_tube,
                fcn(_kinematics.Result):         self.render_kinematics,
                fcn(_motor.Motor):               self.render_motor,
                fcn(_platform.Platform):         self.render_platform,
                fcn(_platform.PlatformList):     self.render_platform_list,
                fcn(_platform_anchor.PlatformAnchor):
                                                 self.render_platform_anchor,
                fcn(_platform_anchor.PlatformAnchorList):
                                                 self.render_platform_anchor_list,
                fcn(_pulley.Pulley):             self.render_pulley,
                fcn(_robot.Robot):               self.render_robot,
                fcn(_grid.Result):               self.render_workspace_grid,
                fcn(_hull.Result):               self.render_workspace_hull,
        }

    @abstractmethod
    def close(self):
        raise NotImplementedError()

    @abstractmethod
    def draw(self):
        raise NotImplementedError()

    @abstractmethod
    def reset(self):
        raise NotImplementedError()

    @abstractmethod
    def show(self):
        raise NotImplementedError()

    def render(self, o: Union['RobotComponent', 'PlottableResult'], *args,
               **kwargs):
        self._RESOLVER[fcn(o)](o, *args, **kwargs)

    @abstractmethod
    def render_cable(self, cable: '_cable.Cable', *args, **kwargs):
        raise NotImplementedError()

    def render_cable_list(self, cable_list: '_cable.CableList', *args,
                          **kwargs):
        for cable in cable_list:
            self.render(cable, *args, **kwargs)

    @abstractmethod
    def render_cuboid(self, cuboid: '_geometry.Cuboid', *args, **kwargs):
        raise NotImplementedError()

    @abstractmethod
    def render_cylinder(self, cylinder: '_geometry.Cylinder', *args, **kwargs):
        raise NotImplementedError()

    @abstractmethod
    def render_drivetrain(self, drivetrain: '_drivetrain.DriveTrain', *args,
                          **kwargs):
        raise NotImplementedError()

    @abstractmethod
    def render_drum(self, drum: '_drum.Drum', *args, **kwargs):
        raise NotImplementedError()

    @abstractmethod
    def render_elliptic_cylinder(self,
                                 elliptic_cylinder:
                                 '_geometry.EllipticCylinder',
                                 *args, **kwargs):
        raise NotImplementedError()

    @abstractmethod
    def render_frame(self, frame: '_frame.Frame', *args, **kwargs):
        raise NotImplementedError()

    @abstractmethod
    def render_frame_anchor(self, anchor: '_frame_anchor.FrameAnchor', *args,
                            **kwargs):
        raise NotImplementedError()

    def render_frame_anchor_list(self,
                                 anchor_list: '_frame_anchor.FrameAnchorList',
                                 *args, **kwargs):
        for anchor in anchor_list:
            self.render(anchor, *args, **kwargs)

    @abstractmethod
    def render_gearbox(self, gearbox: '_gearbox.Gearbox', *args, **kwargs):
        raise NotImplementedError()

    @abstractmethod
    def render_kinematics(self, kinematics: '_kinematics.Result',
                          robot: '_robot.Robot', *args, **kwargs):
        raise NotImplementedError()

    @abstractmethod
    def render_motor(self, motor: '_motor.Motor', *args, **kwargs):
        raise NotImplementedError()

    @abstractmethod
    def render_platform(self, platform: '_platform.Platform', *args, **kwargs):
        raise NotImplementedError()

    @abstractmethod
    def render_platform_anchor(self, anchor: '_platform_anchor.PlatformAnchor',
                               *args, **kwargs):
        raise NotImplementedError()

    def render_platform_anchor_list(self,
                                    anchor_list:
                                    '_platform_anchor.PlatformAnchorList',
                                    *args, **kwargs):
        for anchor in anchor_list:
            self.render(anchor, *args, **kwargs)

    def render_platform_list(self, platform_list: '_platform.PlatformList',
                             *args, **kwargs):
        for platform in platform_list:
            self.render(platform, *args, **kwargs)

    @abstractmethod
    def render_pulley(self, pulley: '_pulley.Pulley', *args, **kwargs):
        raise NotImplementedError()

    @abstractmethod
    def render_robot(self, robot: '_robot.Robot', *args, **kwargs):
        raise NotImplementedError()

    @abstractmethod
    def render_sphere(self, sphere: '_geometry.Sphere', *args, **kwargs):
        raise NotImplementedError()

    @abstractmethod
    def render_tube(self, tube: '_geometry.Tube', *args, **kwargs):
        raise NotImplementedError()

    @abstractmethod
    def render_workspace_grid(self, workspace: '_grid.Result', *args,
                              **kwargs):
        raise NotImplementedError()

    @abstractmethod
    def render_workspace_hull(self, workspace: '_hull.Result', *args,
                              **kwargs):
        raise NotImplementedError()

    def _render_component_list(self, obj: 'RobotComponent', name: str, *args,
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
        coordinate: Vector
            A `(NA,X)` matrix of `_NUMBER_OF_AXES` coordinates which can be
            directly passed to the underlying matplotlib render call.

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
        return 255 * _np.asarray(rgb)


__all__ = [
        'Engine',
]

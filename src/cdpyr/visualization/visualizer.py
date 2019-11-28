import itertools
from abc import (
    ABC,
    abstractmethod
)
from typing import (
    AnyStr,
    Callable,
    Dict,
    Union,
    Sequence
)

import numpy as _np

from cdpyr.analysis.workspace import (
    result as _workspace
)
from cdpyr.analysis.workspace.grid import grid_result as _grid
from cdpyr.analysis.workspace.hull import hull_result as _hull
from cdpyr.geometry import (
    cuboid as _cuboid,
    cylinder as _cylinder,
    elliptic_cylinder as _elliptic_cylinder,
    geometry as _geometry,
    sphere as _sphere,
    tube as _tube,
)
from cdpyr.robot import (
    RobotComponent,
    drivetrain as _drivetrain,
    drum as _drum,
    frame as _frame,
    gearbox as _gearbox,
    kinematicchain as _kinematic_chain,
    motor as _motor,
    platform as _platform,
    pulley as _pulley,
    robot as _robot,
)
from cdpyr.robot.anchor import (
    frame_anchor as _frame_anchor,
    platform_anchor as _platform_anchor,
)
from cdpyr.typing import (
    Matrix,
    Vector
)

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"


class Visualizer(ABC):
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
    AXES_NAMES = ('x', 'y', 'z')
    _NUMBER_OF_AXES: int
    _NUMBER_OF_COORDINATES: int

    _MAPPING: Dict[AnyStr, Callable]

    def __init__(self):
        self._MAPPING = {
            # _cable.Cable.__name__:           self.render_cable,
            _cuboid.Cuboid.__name__:     self.render_cuboid,
            _cylinder.Cylinder.__name__: self.render_cylinder,
            _drivetrain.DriveTrain.__name__:
                                         self.render_drivetrain,
            _drum.Drum.__name__:         self.render_drum,
            _elliptic_cylinder.EllipticCylinder.__name__:
                                         self.render_elliptic_cylinder,
            _frame.Frame.__name__:       self.render_frame,
            _frame_anchor.FrameAnchor.__name__:
                                         self.render_frame_anchor,
            _gearbox.Gearbox.__name__:   self.render_gearbox,
            _geometry.Geometry.__name__: self.render_geometry,
            _kinematic_chain.KinematicChain.__name__:
                                         self.render_kinematic_chain,
            _motor.Motor.__name__:       self.render_motor,
            _platform.Platform.__name__: self.render_platform,
            _platform_anchor.PlatformAnchor.__name__:
                                         self.render_platform_anchor,
            _pulley.Pulley.__name__:     self.render_pulley,
            _robot.Robot.__name__:       self.render_robot,
            _sphere.Sphere.__name__:     self.render_sphere,
            _tube.Tube.__name__:         self.render_tube,
            _workspace.Result.__name__:  self.render_workspace,
            _grid.GridResult.__name__:       self.render_workspace_grid,
            _hull.HullResult.__name__:       self.render_workspace_hull,
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

    def render(self, obj: RobotComponent, *args, **kwargs):
        # just a convenience wrapper for the underlying implementation of
        # that particular object's rendering method

        # get type of the object being passed
        type = obj.__class__.__name__

        # draw the given object only if it is supposed to be drawn
        if not args or (args and isinstance(args[0], bool) and args[0]):
            try:
                # return the specific plot handling method
                return self._MAPPING[type](obj, *args, **kwargs)
            except KeyError as KeyE:
                raise RuntimeWarning(
                    f'No render method for object of type `{type}` found.') \
                    from KeyE

    # @abstractmethod
    # def render_cable(self,
    #                  cable: '_cable.Cable',
    #                  *args,
    #                  **kwargs):
    #     raise NotImplementedError()

    @abstractmethod
    def render_coordinate_system(self,
                                 position: Vector,
                                 dcm: Matrix,
                                 **kwargs):
        raise NotImplementedError()

    @abstractmethod
    def render_cuboid(self,
                      cuboid: '_cuboid.Cuboid',
                      *args,
                      **kwargs):
        raise NotImplementedError()

    @abstractmethod
    def render_cylinder(self,
                        cylinder: '_cylinder.Cylinder',
                        *args,
                        **kwargs):
        raise NotImplementedError()

    @abstractmethod
    def render_elliptic_cylinder(self,
                                 cylinder:
                                 '_elliptic_cylinder.EllipticCylinder',
                                 *args,
                                 **kwargs):
        raise NotImplementedError()

    @abstractmethod
    def render_drivetrain(self,
                          drivetrain: '_drivetrain.DriveTrain',
                          *args,
                          **kwargs):
        raise NotImplementedError()

    @abstractmethod
    def render_drum(self,
                    drum: '_drum.Drum',
                    *args,
                    **kwargs):
        raise NotImplementedError()

    @abstractmethod
    def render_frame(self,
                     frame: '_frame.Frame',
                     *args,
                     **kwargs):
        raise NotImplementedError()

    @abstractmethod
    def render_frame_anchor(self,
                            frame_anchor: '_frame_anchor.FrameAnchor',
                            *args,
                            **kwargs):
        raise NotImplementedError()

    @abstractmethod
    def render_gearbox(self,
                       gearbox: '_gearbox.Gearbox',
                       *args,
                       **kwargs):
        raise NotImplementedError()

    def render_geometry(self,
                        geometry: '_geometry.Geometry',
                        *args,
                        **kwargs):
        return self.render(geometry, *args, **kwargs)

    @abstractmethod
    def render_kinematic_chain(self,
                               kinematic_chain:
                               '_kinematic_chain.KinematicChain',
                               *args,
                               **kwargs):
        raise NotImplementedError()

    @abstractmethod
    def render_motor(self,
                     motor: '_motor.Motor',
                     *args,
                     **kwargs):
        raise NotImplementedError()

    @abstractmethod
    def render_platform(self,
                        platform: '_platform.Platform',
                        *args,
                        **kwargs):
        raise NotImplementedError()

    @abstractmethod
    def render_platform_anchor(self,
                               platform_anchor:
                               '_platform_anchor.PlatformAnchor',
                               *args,
                               **kwargs):
        raise NotImplementedError()

    @abstractmethod
    def render_pulley(self,
                      pulley: '_pulley.Pulley',
                      *args,
                      **kwargs):
        raise NotImplementedError()

    @abstractmethod
    def render_robot(self,
                     robot: '_robot.Robot',
                     *args,
                     **kwargs):
        raise NotImplementedError()

    @abstractmethod
    def render_sphere(self,
                      sphere: '_sphere.Sphere',
                      *args,
                      **kwargs):
        raise NotImplementedError()

    @abstractmethod
    def render_tube(self,
                    tube: '_tube.Tube',
                    *args,
                    **kwargs):
        raise NotImplementedError()

    def render_workspace(self,
                         workspace: '_workspace.Result',
                         *args,
                         **kwargs):
        return self.render_workspace(workspace, *args, **kwargs)

    @abstractmethod
    def render_workspace_grid(self,
                              workspace: '_grid.GridResult',
                              *args,
                              **kwargs):
        raise NotImplementedError()

    @abstractmethod
    def render_workspace_hull(self,
                              workspace: '_hull.HullResult',
                              *args,
                              **kwargs):
        raise NotImplementedError()

    def _render_component_list(self,
                               obj: object,
                               name: str,
                               *args,
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

        # if the coordinate has less rows than the visualizer needs, we will
        # add zeros at the bottom
        if coordinate.shape[0] < self._NUMBER_OF_AXES:
            coordinate = _np.pad(coordinate, (
                (0, self._NUMBER_OF_AXES - coordinate.shape[0]),))

        # return result
        return coordinate[0:self._NUMBER_OF_AXES,:]

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
        single = dcm.ndim == 2

        # turn vectors into matrices
        if single:
            dcm = dcm[:, :, _np.newaxis]

        # extract the data
        dcm = dcm[0:self._NUMBER_OF_AXES,0:self._NUMBER_OF_AXES,:]

        # return single or all dcms
        return dcm[0] if single else dcm

    def _prepare_plot_coordinates(self, coordinates: Union[Vector, Matrix], axes: Sequence[AnyStr] = None):
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

        # return result as a dictionary of ('e0': [], 'e1': [], ..., 'en': [])
        if axes is not None:
            return dict(zip(axes[0:self._NUMBER_OF_AXES], coordinates))
        # return result as simple array
        else:
            return coordinates

    def _rgb2RGB(self, rgb: Vector):
        rgb = _np.asarray(rgb)

        return rgb * 255

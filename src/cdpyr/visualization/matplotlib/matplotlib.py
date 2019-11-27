import itertools
from abc import ABC
from typing import (
    Dict,
    Union
)

import numpy as _np
from matplotlib import (
    collections as plt_collections,
    pyplot as plt
)
from mpl_toolkits.mplot3d import (
    Axes3D,
    art3d
)
from scipy.spatial import Delaunay as _Delaunay

from cdpyr.geometry import (
    cuboid as _cuboid,
    cylinder as _cylinder,
    elliptic_cylinder as _elliptic_cylinder,
    sphere as _sphere,
    tube as _tube
)
from cdpyr.kinematics.transformation import Homogenous as \
    _HomogenousTransformation
from cdpyr.robot import (
    robot as _robot,
)
from cdpyr.typing import (
    Matrix,
    Vector
)
from cdpyr.visualization.visualizer import Visualizer

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"


class Matplotlib(Visualizer, ABC):
    _figure: plt.Figure
    _NUMBER_OF_AXES: int
    _NUMBER_OF_COORDINATES: int

    def __init__(self, *args, figure: plt.Figure = None, **kwargs):
        super().__init__()
        self.figure = figure

    @property
    def figure(self):
        if self._figure is None:
            self._figure = plt.figure()

        return self._figure

    @figure.setter
    def figure(self, figure: plt.Figure):
        self._figure = figure

    @figure.deleter
    def figure(self):
        if self._figure is not None:
            plt.close(self._figure)

        del self._figure

    def _axes(self, *args, **kwargs) -> Union[Axes3D, plt.Axes]:
        if self._NUMBER_OF_AXES == 3:
            kwargs.update({'projection': '3d'})

        return self.figure.gca(*args,
                               **kwargs)

    @property
    def _poly_collection(self):
        if self._NUMBER_OF_AXES == 3:
            return art3d.Poly3DCollection
        else:
            return plt_collections.PolyCollection

    def close(self):
        del self.figure

    def draw(self):
        self._figure.canvas.draw_idle()

    def reset(self):
        # create a new figure
        self._figure = plt.figure()

    def show(self):
        self._figure.show()

    def render_robot(self,
                     robot: '_robot.Robot',
                     *args,
                     **kwargs):
        # first, render the frame
        frame_style = kwargs.pop('frame', {})
        if frame_style is not False:
            self.render(robot.frame,
                        **frame_style)

        # loop over the components to list
        for list_name in ('kinematic_chains', 'platforms'):
            self._render_component_list(robot, list_name, **kwargs)

    # def render_cable(self,
    #                  cable: '_cable.Cable',
    #                  *args,
    #                  **kwargs):
    #     pass

    def render_cuboid(self,
                      cuboid: '_cuboid.Cuboid',
                      *args,
                      **kwargs):
        # get all needed dimensions for the cuboid
        dimensions = _np.asarray([cuboid.width, cuboid.depth, cuboid.height])[
                     _np.newaxis,
                     0:self._NUMBER_OF_COORDINATES]

        # all combinations of positive and negative ones
        pos_neg_ones = _np.asarray(list(
                itertools.product((-1, 1), repeat=self._NUMBER_OF_COORDINATES)))

        # Determine the corners depending on the amount of axes
        if self._NUMBER_OF_COORDINATES == 1:
            vertices = _np.hstack((0.5 * pos_neg_ones * dimensions,
                                   _np.zeros((self._NUMBER_OF_AXES, 1))))
            edges = _np.asarray([[0, 1]])
        else:
            vertices = 0.5 * pos_neg_ones * dimensions

        try:
            # get edges of the convex hull and the list sorted
            # points/vertices as ued by Delaunay
            delau = _Delaunay(vertices)

            # get the cuboids faces and edges
            vertices = delau.points
            if self._NUMBER_OF_COORDINATES == 2:
                edges = delau.simplices
            else:
                edges = delau.convex_hull
        except Exception:
            pass

        # standard poly collection arguments
        pc_args = {
                'edgecolors': [0.0, 0.0, 0.0],
                'facecolors': [0.9, 0.9, 0.9],
        }
        # first, plot all patches, then loop over each edge and plot that
        # separately
        self._axes().add_collection(
                self._poly_collection(vertices[edges, :],
                                      **pc_args))

    def render_cylinder(self,
                        cylinder: '_cylinder.Cylinder',
                        *args,
                        **kwargs):
        pass

    def render_coordinate_system(self,
                                 position: Vector = None,
                                 dcm: Matrix = None,
                                 **kwargs):
        # default position
        position = self._parse_coordinate(position)

        # default rotation
        dcm = self._parse_dcm(dcm)

        # loop over each axis
        for idx in range(self._NUMBER_OF_COORDINATES):
            self._axes().quiver(
                    *position,
                    *dcm.dot(
                            self._parse_coordinate(
                                    self.COORDINATE_DIRECTIONS[idx])),
                    color=self.COORDINATE_COLORS[idx],
            )

    def render_drivetrain(self,
                          drivetrain: '_drivetrain.DriveTrain',
                          *args,
                          **kwargs):
        pass

    def render_drum(self,
                    drum: '_drum.Drum',
                    *args,
                    **kwargs):
        pass

    def render_elliptic_cylinder(self,
                                 cylinder:
                                 '_elliptic_cylinder.EllipticCylinder',
                                 *args,
                                 **kwargs):
        pass

    def render_frame(self,
                     frame: '_frame.Frame',
                     *args,
                     **kwargs):
        # render all anchors
        self._render_component_list(frame, 'anchors', **kwargs)

        # render world coordinate system
        self.render_coordinate_system()

    def render_frame_anchor(self,
                            anchor: '_frame_anchor.FrameAnchor',
                            *args,
                            **kwargs):

        # prepare position and orientation of the anchor
        position = self._parse_coordinate(anchor.linear.position)
        dcm = self._parse_dcm(anchor.angular.dcm)

        # plot coordinate system
        self.render_coordinate_system(position, dcm)

        # plot anchor
        self._axes().plot(*position,
                          marker='o', markersize=2,
                          color=[0.0, 0.0, 1.0],
                          linestyle='none',
                          )

    def render_gearbox(self,
                       gearbox: '_gearbox.Gearbox',
                       *args,
                       **kwargs):
        pass

    def render_kinematic_chain(self,
                               kinematic_chain:
                               '_kinematic_chain.KinematicChain',
                               *args,
                               **kwargs):
        # quicker access to platform, anchor, cable, etc.
        platform = kinematic_chain.platform
        frame_anchor = kinematic_chain.frame_anchor
        platform_anchor = kinematic_chain.platform_anchor
        cable = kinematic_chain.cable

        # get position of platform
        platform_position = self._parse_coordinate(
                platform.pose.linear.position)
        platform_dcm = self._parse_dcm(platform.pose.angular.dcm)

        # get position of anchor
        anchor_position = self._parse_coordinate(frame_anchor.linear.position)
        anchor_dcm = self._parse_dcm(frame_anchor.angular.dcm)

        # calculate distal position of cable
        distal_position = platform_position + platform_dcm.dot(
                self._parse_coordinate(platform_anchor.linear.position))
        proximal_point = anchor_position

        # finally, plot the cable from proximal to distal point
        self._axes().plot(*_np.hstack((proximal_point, distal_position)),
                          color=cable.color.get_rgb(),
                          linestyle='solid',
                          **kwargs)

    def render_motor(self,
                     motor: '_motor.Motor',
                     *args,
                     **kwargs):
        pass

    def render_platform(self,
                        platform: '_platform.Platform',
                        *args,
                        **kwargs):
        # get platform position and orientation
        position = self._parse_coordinate(platform.pose.linear.position)
        dcm = self._parse_dcm(platform.pose.angular.dcm)

        # plot platform shape
        if not platform.is_point:
            # get original anchors as (3,M) matrix
            anchors = self._parse_coordinate(platform.bi)

            # retrieve bounding box of anchors, note that Delaunay assumes
            # number of columns as number of dimensions
            delau = _Delaunay(anchors.T)

            # get edges of the convex hull and the list sorted
            # points/vertices as ued by Delaunay
            edges = delau.convex_hull
            vertices = delau.points

            # also rotate and translate the platform anchors
            vertices = (position + dcm.dot(vertices.T)).T

            pc_args = {
                    'edgecolors': [0.0, 0.0, 0.0],
                    'facecolors': [0.9, 0.9, 0.9],
            }
            self._axes().add_collection(
                    self._poly_collection(vertices[edges, :],
                                          **pc_args))

        # plot every platform anchor using the platform's current position
        # and orientation
        self._render_component_list(platform,
                                    'anchors',
                                    transformation=platform.pose.transformation,
                                    **kwargs)

        # # weird bug/behavior? of `plot3D` requires a numpy value for the
        # # `z`-coordinate, so this is a fix
        # position = _np.asarray([position]).T

        # platform center
        self._axes().plot(*position,
                          marker='o', markersize=2,
                          color=[0.0, 0.0, 1.0],
                          linestyle='none',
                          )

        # render reference coordinate system of platform
        self.render_coordinate_system(position)
        # render rotated coordinate system of platform
        if platform.motion_pattern.can_rotate:
            self.render_coordinate_system(position,
                                          dcm)

    #
    def render_platform_anchor(self,
                               anchor:
                               '_platform_anchor.PlatformAnchor',
                               *args,
                               transformation: _HomogenousTransformation = None,
                               **kwargs):
        # get the anchor's original position and orientation
        position = anchor.linear.position
        dcm = anchor.angular.dcm

        # default value for transformation, if the platform has no pose
        if transformation is None:
            transformation = _HomogenousTransformation()

        # transform the position
        position = self._parse_coordinate(transformation.apply(position))

        # plot the anchor at its final coordinate
        self._axes().plot(*position,
                          marker='o', markersize=2,
                          color=[0.0, 0.0, 1.0],
                          linestyle='none',
                          )

    def render_pulley(self,
                      pulley: '_pulley.Pulley',
                      *args,
                      **kwargs):
        pass

    def render_sphere(self,
                      sphere: '_sphere.Sphere',
                      *args,
                      **kwargs):
        pass

    def render_tube(self,
                    tube: '_tube.Tube',
                    *args,
                    **kwargs):
        pass

    def _render_component_list(self,
                               obj: object,
                               name: str,
                               *args,
                               **kwargs):
        styles = kwargs.pop(name, {})
        try:
            transformation = {'transformation': kwargs.pop('transformation')}
        except KeyError:
            transformation = {}
        if styles is not False:
            if isinstance(styles, Dict):
                styles = [styles]

            components = getattr(obj, name)

            if len(styles) < len(components):
                styles = itertools.cycle(styles)

            for component, style in zip(components, styles):
                self.render(component, *args, **transformation, **style)

    def _parse_coordinate(self, coordinate: Vector = None):
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
        if coordinate is None:
            coordinate = [0.0] * self._NUMBER_OF_AXES

        # anything into a numpy array
        coordinate = _np.asarray(coordinate)

        # scalars into vectors
        if coordinate.ndim == 0:
            coordinate = _np.asarray([coordinate])

        # turn vectors into matrices
        if coordinate.ndim == 1:
            coordinate = coordinate[:, _np.newaxis]

        # add rows of zeros below the coordinate to make it a valid matrix
        return _np.vstack((coordinate[0:self._NUMBER_OF_COORDINATES, :],
                           _np.zeros((
                                   self._NUMBER_OF_AXES -
                                   self._NUMBER_OF_COORDINATES,
                                   coordinate.shape[1]))))

    def _parse_dcm(self, dcm: Matrix = None):
        if dcm is None:
            dcm = _np.eye(self._NUMBER_OF_AXES)

        return _np.asarray(dcm)[0:self._NUMBER_OF_AXES, 0:self._NUMBER_OF_AXES]


__all__ = [
        'Matplotlib',
]

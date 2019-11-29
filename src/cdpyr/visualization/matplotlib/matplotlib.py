import itertools
from abc import (
    ABC,
)
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
from scipy.spatial import (
    ConvexHull as _ConvexHull,
    Delaunay as _Delaunay,
)

from cdpyr.analysis.workspace.grid import grid_result as _grid
from cdpyr.analysis.workspace.hull import hull_result as _hull
from cdpyr.geometry import (
    cuboid as _cuboid,
    cylinder as _cylinder,
    sphere as _sphere,
    tube as _tube,
)
from cdpyr.kinematics.transformation import Homogenous as \
    _HomogenousTransformation
from cdpyr.robot import (
    cable as _cable,
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
    Vector,
)
from cdpyr.visualization import visualizer as _visualizer

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"


class Matplotlib(_visualizer.Visualizer, ABC):
    _figure: plt.Figure

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
        self.figure.canvas.draw_idle()

    def reset(self):
        # create a new figure
        self.figure = plt.figure()

    def show(self):
        self.figure.show()

    def render_robot(self,
                     robot: '_robot.Robot',
                     *args,
                     **kwargs):
        # first, render the frame
        frame_style = kwargs.pop('frame', {})
        if frame_style is not False:
            self.render(robot.frame, **frame_style)

        # loop over the components to list
        for list_name in ('kinematic_chains', 'platforms'):
            self._render_component_list(robot, list_name, **kwargs)

    def render_cable(self,
                     cable: '_cable.Cable',
                     *args,
                     **kwargs):
        pass

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
                                 position: Vector,
                                 dcm: Matrix,
                                 **kwargs):
        # loop over each axis
        for idx in range(self._NUMBER_OF_COORDINATES):
            self._axes().quiver(
                *self._prepare_plot_coordinates(
                    self._extract_coordinates(position)),
                *self._prepare_plot_coordinates(self._extract_coordinates(
                    dcm.dot(self.COORDINATE_DIRECTIONS[idx]))),
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
        self.render_coordinate_system(_np.zeros((3, 1)), _np.eye(3))

    def render_frame_anchor(self,
                            anchor: '_frame_anchor.FrameAnchor',
                            *args,
                            **kwargs):
        # plot coordinate system
        self.render_coordinate_system(anchor.linear.position,
                                      anchor.angular.dcm)

        # plot anchor
        self._axes().plot(*self._prepare_plot_coordinates(
            self._extract_coordinates(anchor.linear.position)),
                          marker='o',
                          markersize=2,
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
        platform_position = platform.pose.linear.position
        platform_dcm = platform.pose.angular.dcm

        # get position of anchor
        anchor_position = frame_anchor.linear.position
        anchor_dcm = frame_anchor.angular.dcm

        # calculate distal position of cable
        distal_position = self._extract_coordinates(
            platform_position + platform_dcm.dot(
                platform_anchor.linear.position))
        proximal_point = self._extract_coordinates(anchor_position)

        # finally, plot the cable from proximal to distal point
        self._axes().plot(*self._prepare_plot_coordinates(
            _np.hstack((proximal_point, distal_position))),
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
        # # get platform position and orientation
        position = platform.pose.linear.position
        dcm = platform.pose.angular.dcm

        # plot platform shape
        if not platform.is_point:
            # get original anchors as (K,M) matrix
            anchors = self._extract_coordinates(platform.bi)

            # in 3D, we perform delaunay triangulation of the corners and
            # retrieve the convex hull from there
            if self._NUMBER_OF_AXES == 3:
                delau = _Delaunay(anchors.T)

                edges = delau.convex_hull
                vertices = delau.points
            # in any other case, we simply calculate the convex hull of
            # the anchors
            else:
                # calculate convex hull of the platform shape
                cv = _ConvexHull(anchors.T)
                # and get all vertices and points in the correct sorted
                # order
                edges = cv.vertices
                vertices = cv.points
                # to close the loop of vertices, we will append the first
                # one to the list
                edges = _np.append(edges, edges[0])

            # ensure vertices are (N,3) arrays
            vertices = _np.pad(vertices, ((0, 0), (0, 3 - vertices.shape[1])))

            # also rotate and translate the platform anchors
            vertices = (position[:, _np.newaxis] + dcm.dot(vertices.T)).T

            if self._NUMBER_OF_AXES == 2:
                vertices = vertices[_np.newaxis, edges.T,
                           0:self._NUMBER_OF_AXES]
            else:
                vertices = vertices[edges, 0:self._NUMBER_OF_AXES]

            pc_args = {
                'edgecolors': [0.0, 0.0, 0.0],
                'facecolors': [0.9, 0.9, 0.9],
            }
            self._axes().add_collection(
                self._poly_collection(vertices,
                                      **pc_args))

        # plot every platform anchor using the platform's current position
        # and orientation
        self._render_component_list(platform,
                                    'anchors',
                                    transformation=platform.pose.transformation,
                                    **kwargs)

        # platform center
        self._axes().plot(*self._prepare_plot_coordinates(
            self._extract_coordinates(position)),
                          marker='o',
                          markersize=2,
                          color=[0.0, 0.0, 1.0],
                          linestyle='none',
                          )

        # render reference coordinate system of platform
        self.render_coordinate_system(position, _np.eye(3))
        # render rotated coordinate system of platform
        if platform.motion_pattern.can_rotate:
            self.render_coordinate_system(position,
                                          dcm)

    def render_platform_anchor(self,
                               anchor:
                               '_platform_anchor.PlatformAnchor',
                               *args,
                               transformation: _HomogenousTransformation = None,
                               **kwargs):
        # default value for transformation, if the platform has no pose
        if transformation is None:
            transformation = _HomogenousTransformation()

        # plot the anchor at its final coordinate
        self._axes().plot(*self._prepare_plot_coordinates(
            self._extract_coordinates(
                transformation.apply(
                    anchor.linear.position))),
                          marker='o',
                          markersize=2,
                          color=[0.0, 0.0, 1.0],
                          linestyle='none'
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

    def render_workspace_grid(self,
                              workspace: '_grid.GridResult',
                              *args,
                              **kwargs):
        only_inside = kwargs.pop('only_inside', False)
        # plot the points inside the workspace
        self._axes().plot(
            *self._prepare_plot_coordinates(
                self._extract_coordinates(workspace.inside.T)),
            marker='o',
            markersize=3,
            color=[0.0, 1.0, 0.0],
            linestyle='none',
        )
        if not only_inside:
            self._axes().plot(
                *self._prepare_plot_coordinates(
                    self._extract_coordinates(workspace.outside.T)),
                marker='o',
                markersize=1.5,
                color=[1.0, 0.0, 0.0],
                linestyle='none',
            )

    def render_workspace_hull(self,
                              workspace: '_hull.HullResult',
                              *args,
                              **kwargs):
        pc_args = {
            'edgecolors': [0.0, 0.0, 0.0],
            'facecolors': [0.9, 0.9, 0.9],
            'alpha':      0.75,
        }
        self._axes().add_collection(
            self._poly_collection(workspace.vertices[workspace.faces, :],
                                  **pc_args))

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


__all__ = [
    'Matplotlib',
]

from __future__ import annotations

import warnings
from abc import ABC

import numpy as _np
from mayavi import mlab as _mlab
from scipy.spatial import Delaunay as _Delaunay
from scipy.spatial.qhull import QhullError

from cdpyr import geometry as _geometry, robot as _robot
from cdpyr.analysis.kinematics import kinematics as _kinematics
from cdpyr.analysis.workspace import grid as _grid, hull as _hull
from cdpyr.helper.data import update_recursive
from cdpyr.kinematics.transformation import Homogenous as \
    _HomogenousTransformation
from cdpyr.typing import Matrix, Vector
from cdpyr.visualization.engine import engine as _engine

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"


class Mayavi(_engine.Engine, ABC):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def close(self, *args, **kwargs):
        _mlab.close()

    def draw(self, *args, **kwargs):
        _mlab.show()

    def reset(self):
        _mlab.clf()

    def show(self):
        _mlab.show()

    def render_cable(self,
                     cable: _robot.Cable,
                     *args,
                     **kwargs):
        pass

    def render_cuboid(self,
                      cuboid: _geometry.Cuboid,
                      *args,
                      **kwargs):
        """
        Render a cuboid by rendering it as a rectangle with only the width
        and depth used because the height is assumed to be along the vertical
        axis with is perpendicular to the plane of a planar robot
        Parameters
        ----------
        cuboid
        args
        kwargs

        Returns
        -------

        """
        # get transformation to apply
        transform = kwargs.get('transformation', _HomogenousTransformation())

        faces = cuboid.faces
        vertices = cuboid.vertices

        # scale vertices to account for the dimensions
        vertices = transform.apply((vertices).T).T

        _mlab.triangular_mesh(
                *self._prepare_plot_coordinates(
                        self._extract_coordinates(vertices.T)),
                faces,
                **update_recursive(
                        dict(
                                name='cuboid',
                                representation='surface',
                                color=self._RGB2rgb((178, 178, 178)),
                                line_width=0.10,
                        ),
                        kwargs.pop('mesh', {}))
        )

    def render_coordinate_system(self,
                                 position: Vector = None,
                                 dcm: Matrix = None,
                                 **kwargs):
        # default position value
        if position is None:
            position = _np.zeros((3,))

        # default orientation of the coordinate system
        if dcm is None:
            dcm = _np.eye(3)

        marker_style = kwargs.pop('marker', {})
        axes_styles = kwargs.pop('axes', {})

        # draw center of the coordinate system
        _mlab.points3d(
                *self._prepare_plot_coordinates(
                        self._extract_coordinates(position)),
                **update_recursive(
                        dict(
                                color=(0, 0, 0),
                                scale_factor=0.10,
                                resolution=3,
                        ),
                        marker_style
                )
        )

        # scaling of coordiante axis length
        scale = kwargs.pop('scale', 0.25)

        # plot each coordinate axis i.e., x, y, z or which of them are available
        name = kwargs.pop('name', 'axis {}')
        for idx in range(self._NUMBER_OF_COORDINATES):
            try:
                name_ = name.format(
                        self.AXES_NAMES[idx],
                        axis=self.AXES_NAMES[idx])
            except KeyError:
                name_ = f'{name}: {self.AXES_NAMES[idx]}'
            _mlab.quiver3d(
                    *self._prepare_plot_coordinates(
                            self._extract_coordinates(
                                    _np.vstack((position,
                                                position + scale *
                                                dcm.dot(
                                                        self.COORDINATE_DIRECTIONS[
                                                            idx]))).T)),
                    **update_recursive(
                            dict(
                                    color=self.COORDINATE_DIRECTIONS[idx],
                                    line_width=0.10,
                                    name=name_,
                            ),
                            axes_styles
                    )
            )

    def render_cylinder(self,
                        cylinder: _geometry.Cylinder,
                        *args,
                        **kwargs):
        # get transformation to apply
        transform = kwargs.get('transformation', _HomogenousTransformation())

        # quicker access to width, depth, and height of cuboid
        radii = cylinder.radius
        height = cylinder.height

        theta = _np.linspace(0, 2 * _np.pi, num=36, endpoint=True)
        z = _np.linspace(-height / 2, height / 2, num=2, endpoint=True)
        theta, z = _np.meshgrid(theta, z)
        x = radii[0] * _np.cos(theta)
        y = radii[1] * _np.sin(theta)

        vertices = _np.stack((x, y, z), axis=1).T

        # apply transformation to the vertices
        try:
            vertices = transform.apply(vertices)
        except ValueError:
            vertices = _np.asarray(
                    [transform.apply(page) for page in vertices.T]).T
            vertices = _np.stack([transform.apply(page) for page in vertices.T],
                                 axis=0)

        # outside surface
        _mlab.surf(
                *self._prepare_plot_coordinates(
                        self._extract_coordinates(
                                _np.swapaxes(vertices, 0, 1))),
        )
        # # top and bottom caps
        for ring in vertices:
            _mlab.surf(
                    *self._prepare_plot_coordinates(
                            self._extract_coordinates(ring)
                    ),
            )

    def render_drivetrain(self,
                          drivetrain: _robot.Drivetrain,
                          *args,
                          **kwargs):
        pass

    def render_drum(self,
                    drum: _robot.Drum,
                    *args,
                    **kwargs):
        pass

    def render_ellipsoid(self,
                         ellipsoid: _geometry.Ellipsoid,
                         *args,
                         **kwargs):
        # get transformation to apply
        transform = kwargs.get('transformation', _HomogenousTransformation())

        # quicker access to width, depth, and height of cuboid
        radii = ellipsoid.radius

        az_ = _np.linspace(-_np.pi, _np.pi, num=36, endpoint=True)
        el_ = _np.linspace(-_np.pi / 2, _np.pi / 2, num=18, endpoint=True)
        az, el = _np.meshgrid(az_, el_)
        x = radii[0] * _np.cos(el) * _np.cos(az)
        y = radii[1] * _np.cos(el) * _np.sin(az)
        z = radii[2] * _np.sin(el)

        vertices = _np.stack((x, y, z), axis=1).T

        # apply transformation to the vertices
        try:
            vertices = transform.apply(vertices)
        except ValueError:
            vertices = _np.asarray(
                    [transform.apply(page) for page in vertices.T]).T
            vertices = _np.stack([transform.apply(page) for page in vertices.T],
                                 axis=0)

        # outside surface
        _mlab.surf(
                *self._prepare_plot_coordinates(
                        self._extract_coordinates(
                                _np.swapaxes(vertices, 0, 1))),
                **update_recursive(
                        dict(
                                name='ellipsoid',
                                color=self._RGB2rgb((178, 178, 178)),
                                line_width=0.10,
                        ),
                        kwargs
                )
        )

        # create a new linearly spaced elevation vector which spans from
        # all the way the south pole to the north pole
        el_ = _np.linspace(-_np.pi, _np.pi, num=36, endpoint=True)

        # calculate the circles of the principal planes (XY, YZ, XZ)
        circles = [
                (_np.vstack((
                        radii[0] * _np.cos(az_),
                        radii[1] * _np.sin(az_),
                        _np.zeros_like(az_),
                )), 'rgb(0, 0, 255)'),
                (_np.vstack((
                        _np.zeros_like(el_),
                        radii[1] * _np.cos(el_),
                        radii[2] * _np.sin(el_),
                )), 'rgb(255, 0, 0)'),
                (_np.vstack((
                        radii[0] * _np.cos(el_),
                        _np.zeros_like(el_),
                        radii[2] * _np.sin(el_),
                )), 'rgb(0, 255, 0)')
        ]

        for circle, color in circles:
            _mlab.surf(
                    *self._prepare_plot_coordinates(
                            self._extract_coordinates(
                                    transform.apply(circle))
                    ),
            )

    def render_frame(self,
                     frame: _robot.Frame,
                     *args,
                     **kwargs):
        # render all anchors
        self._render_component_list(frame, 'anchors', **kwargs)

        # render world coordinate system
        self.render_coordinate_system(name='world center')

    def render_frame_anchor(self,
                            anchor: _robot.FrameAnchor,
                            *args,
                            **kwargs):
        # get loop index
        aidx = kwargs.pop('loop_index', -1)

        # plot coordinate system
        self.render_coordinate_system(anchor.linear.position,
                                      anchor.angular.dcm,
                                      name=f'frame anchor {aidx}')

    def render_gearbox(self,
                       gearbox: _robot.Gearbox,
                       *args,
                       **kwargs):
        pass

    def render_kinematics(self,
                          kinematics: _kinematics.Result,
                          *args,
                          **kwargs):
        # ask the kinematics result object to calculate the cable shape
        cable_shapes = kinematics.cable_shapes

        # and plot each kinematic chain
        for index_chain in range(cable_shapes.shape[1]):
            _mlab.plot3d(
                    *self._prepare_plot_coordinates(
                            self._extract_coordinates(
                                    cable_shapes[:, index_chain, :])),
            )

    def render_motor(self,
                     motor: _robot.Motor,
                     *args,
                     **kwargs):
        pass

    def render_platform(self,
                        platform: _robot.Platform,
                        *args,
                        **kwargs):
        # platform position and orientation
        position = platform.pose.linear.position
        dcm = platform.pose.angular.dcm

        # temporary platform loop index
        pidx = kwargs.pop('loop_index', -1)

        # if the platform has a geometry assigned, we will plot the geometry
        # and only add the anchor points to it
        if platform.geometry is not None:
            self.render(platform.geometry,
                        transformation=platform.pose.transformation,
                        name=f'platform {pidx}')
        # otherwise, without a platform geometry, we will triangulate the
        # anchor points and plot the platform shape via that
        else:
            # render bounding box of platform
            if not platform.is_point:
                # get original anchors as (K,M) matrix
                anchors = self._extract_coordinates(platform.bi)

                # in 3D, we perform delaunay triangulation of the corners and
                # retrieve the convex hull from there
                try:
                    delau = _Delaunay(anchors.T)
                except QhullError as e:
                    warnings.warn(RuntimeWarning(e))
                    return

                edges = delau.convex_hull
                vertices = delau.points

                # ensure vertices are (N,3) arrays
                vertices = _np.pad(vertices,
                                   ((0, 0), (0, 3 - vertices.shape[1])))

                # also rotate and translate the platform anchors
                vertices = (position[:, _np.newaxis] + dcm.dot(vertices.T)).T

                # 3D plot
                # first, plot the mesh of the platform i.e., its volume
                _mlab.triangular_mesh(
                        *self._prepare_plot_coordinates(
                                self._extract_coordinates(
                                        vertices.T)),
                        edges,
                        **update_recursive(
                                dict(
                                        color=(0, 0, 0),
                                        line_width=0.10,
                                ),
                                kwargs
                        )
                )
                # close all edges by appending the first column
                edges = _np.hstack((edges, edges[:, 0, _np.newaxis]))
                # and loop over each edge to plot
                for edge in edges:
                    _mlab.plot3d(
                            *self._prepare_plot_coordinates(
                                    vertices[edge, :].T),
                            **update_recursive(
                                    dict(
                                            color=self._RGB2rgb((13, 13, 13)),
                                            line_width=0.10,
                                    ),
                                    kwargs
                            )
                    )

        # render all anchors
        self._render_component_list(platform,
                                    'anchors',
                                    transformation=platform.pose.transformation,
                                    platform_index=pidx,
                                    **kwargs
                                    )

        # render reference coordinate system of platform
        self.render_coordinate_system(position,
                                      name=f'platform {pidx}: center')

        # render rotated coordinate system of platform
        if platform.can_rotate:
            self.render_coordinate_system(position,
                                          dcm,
                                          name=f'platform {pidx}')

    def render_platform_anchor(self,
                               anchor: _robot.PlatformAnchor,
                               *args,
                               transformation: _HomogenousTransformation = None,
                               **kwargs):
        # default value for transformation, if the platform has no pose
        if transformation is None:
            transformation = _HomogenousTransformation()

        # anchor index from outside
        aidx = kwargs.pop('loop_index', -1)
        # platform index from outside
        pidx = kwargs.pop('platform_index', -1)

        _mlab.points3d(
                *self._prepare_plot_coordinates(
                        self._extract_coordinates(
                                transformation.apply(
                                        anchor.linear.position))),
                **update_recursive(
                        dict(
                                name=f'platform {pidx}: anchor {aidx}',
                                color=(1, 0, 0),
                                scale_factor=0.10,
                                resolution=3,
                        ),
                        kwargs
                )
        )

    def render_polyhedron(self,
                          polyhedron: _geometry.Polyhedron,
                          *args,
                          **kwargs):
        # render the polyehedron as mesh
        _mlab.triangular_mesh(
                *self._prepare_plot_coordinates(
                        self._extract_coordinates(
                                polyhedron.vertices.T)),
                polyhedron.faces,
                **update_recursive(
                        dict(
                                color=self._RGB2rgb((178, 178, 178)),
                                line_width=0.10,
                        ),
                        kwargs.pop('mesh', {})
                )
        )

        # and render each edge
        for face, vertices in polyhedron:
            _mlab.plot3d(
                    *self._prepare_plot_coordinates(
                            self._extract_coordinates(vertices.T)),
                    **update_recursive(
                            dict(
                                    color=(0, 0, 0),
                                    line_width=0.10,
                                    tube_radius=None,
                            ),
                            kwargs.pop('lines', {})
                    )
            )

    def render_pulley(self,
                      pulley: _robot.Pulley,
                      *args,
                      **kwargs):
        pass

    def render_robot(self,
                     robot: _robot.Robot,
                     *args,
                     **kwargs):
        # first, render the frame
        frame_style = kwargs.pop('frame', {})
        if frame_style is not False:
            self.render(robot.frame, **frame_style)

        # loop over the components to list
        self._render_component_list(robot, 'platforms', **kwargs)

    def render_tube(self,
                    tube: _geometry.Tube,
                    *args,
                    **kwargs):
        self.render(tube.inner, *args, **kwargs)
        self.render(tube.outer, *args, **kwargs)

    def render_workspace_grid(self,
                              workspace: _grid.Result,
                              *args,
                              **kwargs):
        # option to plot only the points inside the workspace
        only_inside = kwargs.pop('only_inside', False)

        # plot the points inside the workspace
        _mlab.points3d(
                *self._prepare_plot_coordinates(
                        self._extract_coordinates(workspace.inside.T)),
                **update_recursive(
                        dict(
                                name='workspace: inside',
                                color=(0, 1, 0),
                                scale_factor=0.10,
                                resolution=3,
                        ),
                        kwargs
                )
        )

        if not only_inside:
            # plot the points outside the workspace
            _mlab.points3d(
                    *self._prepare_plot_coordinates(
                            self._extract_coordinates(
                                    workspace.outside.T)),
                    **update_recursive(
                            dict(
                                    name='workspace: outside',
                                    color=(1, 0, 0),
                                    scale_factor=0.10,
                                    resolution=3,
                            ),
                            kwargs
                    )
            )

    def render_workspace_hull(self,
                              workspace: _hull.Result,
                              *args,
                              **kwargs):
        if self._NUMBER_OF_AXES != 3:
            raise NotImplementedError()

        # as simple as that
        self.render_polyhedron(workspace,
                               *args,
                               **kwargs
                               # update_recursive(
                               #         dict(
                               #                 mesh=dict(
                               #                         color=(1, 0, 0),
                               #                         opacity=0.50,
                               #                 ),
                               #                 lines=dict(
                               #                         line_width=0.10,
                               #                 )
                               #         ),
                               #         **kwargs
                               # )
                               )

    # def _prepare_plot_coordinates(self,
    #                               coordinates: Union[Vector, Matrix],
    #                               axes: Sequence = None):
    #     # default value for the axes be ('x', 'y', 'z') if not given elsewise
    #     if axes is None:
    #         axes = self.AXES_NAMES
    #
    #     # check if we are dealing with single arrays i.e., (AxC) arrays where
    #     # A is the number of plot axes and C the number of coordinates
    #     is_single = coordinates.ndim == 3 and coordinates.shape[1] == 1
    #
    #     # prepare data using parent method
    #     prepared = _engine.Engine._prepare_plot_coordinates(self, coordinates)
    #
    #     # and now strip
    #     if is_single:
    #         prepared = prepared[:, 0, :]
    #
    #     # return result as a dictionary of ('e0': [], 'e1': [], ..., 'en': [])
    #     return dict(zip(axes[0:self._NUMBER_OF_AXES], prepared))


class Linear(Mayavi):
    _NUMBER_OF_COORDINATES = 1
    _NUMBER_OF_AXES = 2

    def __init__(self, **kwargs):
        raise NotImplementedError()


class Planar(Mayavi):
    _NUMBER_OF_COORDINATES = 2
    _NUMBER_OF_AXES = 2

    def __init__(self, **kwargs):
        raise NotImplementedError()


class Spatial(Mayavi):
    _NUMBER_OF_COORDINATES = 3
    _NUMBER_OF_AXES = 3


__all__ = [
        'Linear',
        'Planar',
        'Spatial',
]

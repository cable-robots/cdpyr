from abc import ABC
from typing import Mapping, Sequence, Union

import numpy as _np
from cdpyr.analysis.kinematics import kinematics as _kinematics
from cdpyr.analysis.workspace import grid as _grid, hull as _hull
from cdpyr.geometry import (
    cuboid as _cuboid,
    cylinder as _cylinder,
    ellipsoid as _ellipsoid,
    polyhedron as _polyhedron,
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
    motor as _motor,
    platform as _platform,
    pulley as _pulley,
    robot as _robot,
)
from cdpyr.robot.anchor import (
    frame_anchor as _frame_anchor,
    platform_anchor as _platform_anchor,
)
from cdpyr.typing import Matrix, Vector
from cdpyr.visualization.engine import engine as _engine
from plotly import graph_objects as go
from scipy.spatial import ConvexHull as _ConvexHull, Delaunay as _Delaunay

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"


def update_recursive(defaults: Mapping, update: Mapping):
    for k, v in update.items():
        if isinstance(v, Mapping):
            defaults[k] = update_recursive(defaults.get(k, {}), v)
        else:
            defaults[k] = v
    return defaults


class Plotly(_engine.Engine, ABC):
    _figure: go.Figure

    COORDINATE_NAMES = ['x', 'y', 'z']

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._figure = None

    @property
    def figure(self):
        if self._figure is None:
            self._figure = go.Figure()

        return self._figure

    @figure.setter
    def figure(self, figure: go.Figure):
        self._figure = figure

    @figure.deleter
    def figure(self):
        del self._figure

    @property
    def _scatter(self):
        if self._NUMBER_OF_AXES == 3:
            return go.Scatter3d
        else:
            return go.Scatter

    @property
    def _mesh(self):
        if self._NUMBER_OF_AXES == 3:
            return go.Mesh3d
        else:
            raise NotImplementedError()

    @property
    def _surface(self):
        if self._NUMBER_OF_AXES == 3:
            return go.Surface
        else:
            raise NotImplementedError()

    def close(self, *args, **kwargs):
        pass

    def draw(self, *args, **kwargs):
        self.figure.update_layout(**kwargs)

    def reset(self):
        self.figure = go.Figure()

    def show(self):
        self.figure.show()

    def render_cable(self,
                     cable: '_cable.Cable',
                     *args,
                     **kwargs):
        pass

    def render_cuboid(self,
                      cuboid: '_cuboid.Cuboid',
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

        if self._NUMBER_OF_COORDINATES == 1:
            faces = _np.asarray(
                    [0, 1, 0]
            )
        elif self._NUMBER_OF_COORDINATES == 2:
            faces = _np.asarray(
                    [0, 1, 2, 3, 0]
            )
        else:
            pass

        faces = cuboid.faces
        vertices = cuboid.vertices

        # scale vertices to account for the dimensions
        vertices = transform.apply((vertices).T).T

        if self._NUMBER_OF_AXES == 3:
            self.figure.add_trace(
                    self._mesh(
                            **self._prepare_plot_coordinates(
                                    self._extract_coordinates(vertices.T)),
                            **self._prepare_plot_coordinates(faces.T,
                                                             ('i', 'j', 'k')),
                            facecolor=['rgb(178, 178, 178)'] * faces.shape[0],
                            vertexcolor=['rgb(0, 0, 0)'] * vertices.shape[0],
                            flatshading=True,
                            opacity=0.75,
                            showscale=False,
                            name='cuboid',
                            hoverinfo='skip',
                            hovertext='',
                    )
            )

            # close faces
            faces = _np.append(faces, faces[:, 0, _np.newaxis], axis=1)

            # draw each edge separately
            for face in faces:
                self.figure.add_trace(
                        self._scatter(
                                **self._prepare_plot_coordinates(
                                        self._extract_coordinates(
                                                vertices[face, :].T)),
                                mode='lines',
                                line=dict(
                                        color='rgb(0, 0, 0)',
                                ),
                                name='cuboid face',
                                hoverinfo='skip',
                                hovertext='',
                                showlegend=False,
                        )
                )
        else:
            self.figure.add_trace(
                    self._scatter(
                            **self._prepare_plot_coordinates(
                                    self._extract_coordinates(
                                            vertices.T[:, faces])),
                            mode='lines',
                            fill='toself',
                            line=dict(
                                    color='rgb(13, 13, 13)'
                            ),
                            fillcolor='rgb(178, 178, 178)',
                            showlegend=False,
                            name='cuboid',
                            hoverinfo='skip',
                            hovertext='',
                    )
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

        # draw center of the coordinate system
        self.figure.add_trace(
                self._scatter(
                        **self._prepare_plot_coordinates(
                                self._extract_coordinates(position)),
                        **update_recursive(dict(
                                mode='markers',
                                marker=dict(
                                        color='Black',
                                        size=3 if self._NUMBER_OF_AXES == 3
                                        else 5,
                                ),
                                showlegend=False,
                        ), kwargs)
                )
        )

        # scaling of coordiante axis length
        scale = kwargs.pop('scale', 0.25)

        # plot each coordinate axis i.e., x, y, z or which of them are available
        for idx in range(self._NUMBER_OF_COORDINATES):
            # convert rgb in range of [0...1] to RGB in range of [0...255]
            rgb = self._rgb2RGB(self.COORDINATE_DIRECTIONS[idx])

            # plot the axis as a line (currently, a quiver isn't supported in
            # 2D... no idea why, plot.ly?!)
            self.figure.add_trace(
                    self._scatter(
                            **self._prepare_plot_coordinates(
                                    self._extract_coordinates(
                                            _np.vstack((position,
                                                        position + scale *
                                                        dcm.dot(
                                                                self.COORDINATE_DIRECTIONS[
                                                                    idx]))).T)),
                            **update_recursive(dict(
                                    mode='lines',
                                    line=dict(
                                            color=f'rgb({rgb[0]},{rgb[1]},'
                                                  f'{rgb[2]})',
                                            width=4 if self._NUMBER_OF_AXES
                                                       == 3 else 2,
                                    ),
                                    name=f'{kwargs.get("name")}: axis {idx}',
                                    hoverinfo='text',
                                    hovertext=f'{kwargs.get("name")}: axis '
                                              f'{idx}',
                                    showlegend=False,
                            ), kwargs)
                    )
            )

    def render_cylinder(self,
                        cylinder: '_cylinder.Cylinder',
                        *args, **kwargs):
        # get transformation to apply
        transform = kwargs.get('transformation', _HomogenousTransformation())

        # quicker access to width, depth, and height of cuboid
        radii = cylinder.radius
        height = cylinder.height

        if self._NUMBER_OF_COORDINATES == 1:
            x = [-radii[0], radii[0]]
            y = [0, 0]
            z = [0, 0]
        elif self._NUMBER_OF_COORDINATES == 2:
            theta = _np.linspace(0, 2 * _np.pi, num=36, endpoint=True)
            x = radii[0] * _np.cos(theta)
            y = radii[1] * _np.sin(theta)
            z = _np.zeros_like(x)
        elif self._NUMBER_OF_COORDINATES == 3:
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

        if self._NUMBER_OF_AXES == 3:
            # outside surface
            self.figure.add_trace(
                    self._surface(
                            **self._prepare_plot_coordinates(
                                    self._extract_coordinates(
                                            _np.swapaxes(vertices, 0, 1))),
                            opacity=0.75,
                            colorscale=[[0, 'rgb(178, 178, 178)'],
                                        [1, 'rgb(178, 178, 178)']],
                            showscale=False,
                            cmin=0,
                            cmax=1,
                            name='cylinder',
                            hoverinfo='skip',
                            hovertext='',
                    )
            )
            # # top and bottom caps
            for ring in vertices:
                self.figure.add_trace(
                        self._scatter(
                                **self._prepare_plot_coordinates(
                                        self._extract_coordinates(ring)
                                ),
                                mode='lines',
                                line=dict(
                                        color='rgb(0, 0, 0)',
                                ),
                                name='cylinder caps',
                                hoverinfo='skip',
                                hovertext='',
                                showlegend=False,
                        )
                )
        else:
            self.figure.add_trace(
                    self._scatter(
                            **self._prepare_plot_coordinates(
                                    self._extract_coordinates(vertices)),
                            mode='lines',
                            fill='toself',
                            line=dict(
                                    color='rgb(13, 13, 13)'
                            ),
                            fillcolor='rgb(178, 178, 178)',
                            showlegend=False,
                            name='cuboid',
                            hoverinfo='skip',
                            hovertext='',
                    )
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

    def render_ellipsoid(self, ellipsoid: '_ellipsoid.Ellipsoid', *args,
                         **kwargs):
        # get transformation to apply
        transform = kwargs.get('transformation', _HomogenousTransformation())

        # quicker access to width, depth, and height of cuboid
        radii = ellipsoid.radius

        if self._NUMBER_OF_COORDINATES == 1:
            x = [-radii[0], radii[0]]
            y = [0, 0]
            z = [0, 0]
        elif self._NUMBER_OF_COORDINATES == 2:
            theta = _np.linspace(0, 2 * _np.pi, num=36, endpoint=True)
            x = radii[0] * _np.cos(theta)
            y = radii[1] * _np.sin(theta)
            z = _np.zeros_like(x)
        elif self._NUMBER_OF_COORDINATES == 3:
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

        if self._NUMBER_OF_AXES == 3:
            # outside surface
            self.figure.add_trace(
                    self._surface(
                            **self._prepare_plot_coordinates(
                                    self._extract_coordinates(
                                            _np.swapaxes(vertices, 0, 1))),
                            opacity=0.75,
                            colorscale=[[0, 'rgb(178, 178, 178)'],
                                        [1, 'rgb(178, 178, 178)']],
                            showscale=False,
                            cmin=0,
                            cmax=1,
                            name='cylinder',
                            hoverinfo='skip',
                            hovertext='',
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
                self.figure.add_trace(
                        self._scatter(
                                **self._prepare_plot_coordinates(
                                        self._extract_coordinates(
                                                transform.apply(circle))
                                ),
                                mode='lines',
                                line=dict(
                                        color=color,
                                ),
                                name='cylinder caps',
                                hoverinfo='skip',
                                hovertext='',
                                showlegend=False,
                        )
                )
        else:
            self.figure.add_trace(
                    self._scatter(
                            **self._prepare_plot_coordinates(
                                    self._extract_coordinates(vertices)),
                            mode='lines',
                            fill='toself',
                            line=dict(
                                    color='rgb(13, 13, 13)'
                            ),
                            fillcolor='rgb(178, 178, 178)',
                            showlegend=False,
                            name='cuboid',
                            hoverinfo='skip',
                            hovertext='',
                    )
            )

    def render_frame(self,
                     frame: '_frame.Frame',
                     *args,
                     **kwargs):
        # render all anchors
        self._render_component_list(frame, 'anchors', **kwargs)

        # render world coordinate system
        self.render_coordinate_system(name='world center',
                                      hoverinfo='text',
                                      hovertext='world center')

    def render_frame_anchor(self,
                            anchor: '_frame_anchor.FrameAnchor',
                            *args,
                            **kwargs):
        # get loop index
        aidx = kwargs.pop('loop_index', -1)

        # plot coordinate system
        self.render_coordinate_system(anchor.linear.position,
                                      anchor.angular.dcm,
                                      name=f'frame anchor {aidx}',
                                      hovertext=f'frame anchor {aidx}',
                                      hoverinfo='text'
                                      )

    def render_gearbox(self,
                       gearbox: '_gearbox.Gearbox',
                       *args,
                       **kwargs):
        pass

    def render_kinematics(self, kinematics: '_kinematics.Result',
                          *args, **kwargs):
        # ask the kinematics result object to calculate the cable shape
        cable_shapes = kinematics.cable_shapes

        # and plot each kinematic chain
        for index_chain in range(cable_shapes.shape[1]):
            self.figure.add_trace(
                    self._scatter(
                            **self._prepare_plot_coordinates(
                                    self._extract_coordinates(
                                            cable_shapes[:, index_chain, :])),
                            mode='lines',
                            line_color='rgb(255, 0, 0)',
                            name='',
                            hoverinfo='skip',
                            hovertext='',
                            showlegend=False
                    )
            )

    def render_motor(self,
                     motor: '_motor.Motor',
                     *args,
                     **kwargs):
        pass

    def render_platform(self,
                        platform: '_platform.Platform',
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
                        name=f'platform {pidx}',
                        hoverinfo='text',
                        hovertext=f'platform {pidx}', )
        # otherwise, without a platform geometry, we will triangulate the
        # anchor points and plot the platform shape via that
        else:
            # render bounding box of platform
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
                vertices = _np.pad(vertices,
                                   ((0, 0), (0, 3 - vertices.shape[1])))

                # also rotate and translate the platform anchors
                vertices = (position[:, _np.newaxis] + dcm.dot(vertices.T)).T

                # 3D plot
                if self._NUMBER_OF_AXES == 3:
                    # first, plot the mesh of the platform i.e., its volume
                    self.figure.add_trace(
                            self._mesh(
                                    **self._prepare_plot_coordinates(
                                            self._extract_coordinates(
                                                    vertices.T)),
                                    **self._prepare_plot_coordinates(edges.T,
                                                                     ('i', 'j',
                                                                      'k')),
                                    color='rgb(0, 0, 0)',
                                    facecolor=['rgb(178, 178, 178)'] *
                                              edges.shape[0],
                                    flatshading=True,
                                    name='',
                                    hoverinfo='skip',
                                    hovertext='',
                            )
                    )
                    # close all edges by appending the first column
                    edges = _np.hstack((edges, edges[:, 0, _np.newaxis]))
                    # and loop over each edge to plot
                    for edge in edges:
                        self.figure.add_trace(
                                self._scatter(
                                        **self._prepare_plot_coordinates(
                                                vertices[edge, :].T),
                                        mode='lines',
                                        line=dict(
                                                color='rgb(13, 13, 13)',
                                        ),
                                        name='',
                                        hoverinfo='skip',
                                        hovertext='',
                                        showlegend=False
                                )
                        )
                # 2D plot
                else:
                    self.figure.add_trace(
                            self._scatter(
                                    **self._prepare_plot_coordinates(
                                            self._extract_coordinates(
                                                    vertices[edges, :].T)),
                                    mode='lines',
                                    fill='toself',
                                    line_color='rgb(13, 13, 13)',
                                    fillcolor='rgb(178, 178, 178)',
                                    name='',
                                    hoverinfo='skip',
                                    hovertext='',
                                    showlegend=False
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
                                      name=f'platform {pidx}: center',
                                      hoverinfo='text',
                                      hovertext=f'platform {pidx}: center',
                                      line=dict(
                                              dash='dash' if platform.can_rotate
                                              else 'solid',
                                      )
                                      )

        # render rotated coordinate system of platform
        if platform.can_rotate:
            self.render_coordinate_system(position,
                                          dcm,
                                          name=f'platform {pidx}',
                                          hovertext=f'platform {pidx}',
                                          hoverinfo='text',
                                          line=dict(
                                                  dash='solid',
                                          )
                                          )

    def render_platform_anchor(self,
                               anchor:
                               '_platform_anchor.PlatformAnchor',
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

        self.figure.add_trace(
                self._scatter(
                        **self._prepare_plot_coordinates(
                                self._extract_coordinates(
                                        transformation.apply(
                                                anchor.linear.position))),
                        **update_recursive(dict(
                                mode='markers',
                                marker=dict(
                                        color='Red',
                                        size=3 if self._NUMBER_OF_AXES == 3
                                        else 5,
                                ),
                                name=f'platform {pidx}: anchor {aidx}',
                                hoverinfo='text',
                                hovertext=f'platform {pidx}: anchor {aidx}',
                                showlegend=False,
                        ), kwargs)
                )
        )

    def render_polyhedron(self, polyhedron: '_polyhedron.Polyhedron', *args,
                          **kwargs):
        # render the polyehedron as mesh
        self.figure.add_trace(
                self._mesh(
                        **self._prepare_plot_coordinates(
                                self._extract_coordinates(
                                        polyhedron.vertices.T)),
                        **self._prepare_plot_coordinates(polyhedron.faces.T,
                                                         ('i', 'j', 'k')),
                        **update_recursive(
                                dict(
                                        facecolor=['rgb(178, 178, 178)'] *
                                                  polyhedron.faces.shape[0],
                                        vertexcolor=['rgb(255, 0, 0)'] *
                                                    polyhedron.vertices.shape[
                                                        0],
                                        flatshading=True,
                                        opacity=0.75,
                                        contour=dict(
                                                show=True,
                                                color='rgb(0, 0, 0)',
                                        ),
                                        name='polyhedron',
                                        hoverinfo='skip',
                                        hovertext='',
                                ),
                                kwargs.pop('mesh', {})
                        )
                )
        )

        # and render each edge
        for face, vertices in polyhedron:
            self.figure.add_trace(
                    self._scatter(
                            **self._prepare_plot_coordinates(
                                    self._extract_coordinates(vertices.T)),
                            **update_recursive(
                                    dict(
                                            mode='lines',
                                            line=dict(
                                                    color='rgb(0, 0, 0)',
                                            ),
                                            name='polyhedron face',
                                            hoverinfo='skip',
                                            hovertext='',
                                            showlegend=False,
                                    ),
                                    kwargs.pop('lines', {})
                            )
                    )
            )

    def render_pulley(self,
                      pulley: '_pulley.Pulley',
                      *args,
                      **kwargs):
        pass

    def render_robot(self,
                     robot: '_robot.Robot',
                     *args,
                     **kwargs):
        # first, render the frame
        frame_style = kwargs.pop('frame', {})
        if frame_style is not False:
            self.render(robot.frame, **frame_style)

        # loop over the components to list
        self._render_component_list(robot, 'platforms', **kwargs)

    def render_sphere(self,
                      sphere: '_sphere.Sphere',
                      *args,
                      **kwargs):
        pass

    def render_tube(self,
                    tube: '_tube.Tube',
                    *args,
                    **kwargs):
        self.render(tube._inner, *args, **kwargs)
        self.render(tube._outer, *args, **kwargs)

    def render_workspace_grid(self,
                              workspace: '_grid.Result',
                              *args,
                              **kwargs):
        # option to plot only the points inside the workspace
        only_inside = kwargs.pop('only_inside', False)

        # plot the points inside the workspace
        self.figure.add_trace(
                self._scatter(
                        **self._prepare_plot_coordinates(
                                self._extract_coordinates(workspace.inside.T)),
                        mode='markers',
                        marker=dict(
                                color='rgb(0, 255, 0)',
                                size=4 if self._NUMBER_OF_AXES == 2 else 6,
                        ),
                        name='workspace: inside',
                        hoverinfo='text',
                        hovertext='',
                        showlegend=False,
                        **kwargs,
                )
        )
        if not only_inside:
            # plot the points outside the workspace
            self.figure.add_trace(
                    self._scatter(
                            **self._prepare_plot_coordinates(
                                    self._extract_coordinates(
                                            workspace.outside.T)),
                            mode='markers',
                            marker=dict(
                                    color='rgb(255, 0, 0)',
                                    size=3 if self._NUMBER_OF_AXES == 3 else 5,
                            ),
                            name='workspace: outside',
                            hoverinfo='text',
                            hovertext='',
                            showlegend=False,
                            **kwargs,
                    )
            )

    def render_workspace_hull(self,
                              workspace: '_hull.Result',
                              *args,
                              **kwargs):
        if self._NUMBER_OF_AXES != 3:
            raise NotImplementedError()

        # as simple as that
        self.render_polyhedron(workspace,
                               *args,
                               facecolor=['rgb(178, 178, 178)'] *
                                         workspace.faces.shape[0],
                               vertexcolor=['rgb(255, 0, 0)'] *
                                           workspace.vertices.shape[0],
                               **kwargs)

    def _prepare_plot_coordinates(self, coordinates: Union[Vector, Matrix],
                                  axes: Sequence = None):
        # default value for the axes be ('x', 'y', 'z') if not given elsewise
        if axes is None:
            axes = self.AXES_NAMES

        # check if we are dealing with single arrays i.e., (AxC) arrays where
        # A is the number of plot axes and C the number of coordinates
        is_single = coordinates.ndim == 3 and coordinates.shape[1] == 1

        # prepare data using parent method
        prepared = _engine.Engine._prepare_plot_coordinates(self, coordinates)

        # and now strip
        if is_single:
            prepared = prepared[:, 0, :]

        # return result as a dictionary of ('e0': [], 'e1': [], ..., 'en': [])
        return dict(zip(axes[0:self._NUMBER_OF_AXES], prepared))


class Linear(Plotly):
    _NUMBER_OF_COORDINATES = 1
    _NUMBER_OF_AXES = 2

    def draw(self, *args, **kwargs):
        super().draw(*args,
                     **update_recursive(
                             dict(
                                     yaxis=dict(
                                             scaleanchor="x",
                                             scaleratio=1,
                                             showline=False,
                                             showticklabels=False,
                                             showgrid=False,
                                     )
                             ),
                             kwargs)
                     )


class Planar(Plotly):
    _NUMBER_OF_COORDINATES = 2
    _NUMBER_OF_AXES = 2

    def draw(self, *args, **kwargs):
        super().draw(*args,
                     **update_recursive(
                             dict(
                                     yaxis=dict(
                                             scaleanchor="x",
                                             scaleratio=1,
                                     ),
                             ),
                             kwargs)
                     )


class Spatial(Plotly):
    _NUMBER_OF_COORDINATES = 3
    _NUMBER_OF_AXES = 3

    def draw(self, *args, **kwargs):
        super().draw(*args,
                     **update_recursive(
                             dict(
                                     yaxis=dict(
                                             scaleanchor="x",
                                             scaleratio=1,
                                     )
                             ),
                             kwargs)
                     )


__all__ = [
        'Plotly',
]

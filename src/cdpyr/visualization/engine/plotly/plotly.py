from abc import (
    ABC,
)
from collections import Mapping
from typing import (
    Sequence,
    Union
)

import numpy as _np
from plotly import graph_objects as go
from scipy.spatial import (
    ConvexHull as _ConvexHull,
    Delaunay as _Delaunay,
)

from cdpyr.analysis.workspace.grid import grid_result as _grid
from cdpyr.analysis.workspace.hull import hull_result as _hull
from cdpyr.geometry import (
    cuboid as _cuboid,
    cylinder as _cylinder,
    elliptic_cylinder as _el_cylinder,
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
from cdpyr.visualization.engine import engine as _engine

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"


def update_recursive(defaults, update):
    for k, v in update.items():
        if isinstance(v, Mapping):
            defaults[k] = update_recursive(defaults.get(k, {}), v)
        else:
            defaults[k] = v
    return defaults


class Plotly(_engine.Engine, ABC):
    _figure: go.Figure

    COORDINATE_NAMES = ['x', 'y', 'z']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
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

    def close(self, *args, **kwargs):
        pass

    def draw(self, *args, **kwargs):
        self.figure.update_layout(
            scene=dict(
                aspectmode='data',
                aspectratio=dict(
                    x=1.00,
                    y=1.00,
                    z=1.00
                )
            ),
            **kwargs
        )

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

        # quicker access to width and height of cuboid
        dimensions = _np.asarray((cuboid.width, cuboid.depth, cuboid.height))

        if self._NUMBER_OF_AXES == 1:
            vertices = _np.asarray([
                [-1.0, 1.0, 0.0]
            ])
            edges = _np.asarray([
                [0, 1]
            ])
        elif self._NUMBER_OF_AXES == 2:
            vertices = _np.asarray((
                (-1.0, 1.0, 0.0),
                (1.0, 1.0, 0.0),
                (1.0, -1.0, 0.0),
                (-1.0, -1.0, 0.0),
            ))
            edges = _np.asarray([
                [0, 1, 2, 3]
            ])
        elif self._NUMBER_OF_AXES == 3:
            vertices = _np.asarray((
                (-1.0, 1.0, 1.0),
                (1.0, 1.0, 1.0),
                (1.0, -1.0, 1.0),
                (-1.0, -1.0, 1.0),
                (-1.0, 1.0, -1.0),
                (1.0, 1.0, -1.0),
                (1.0, -1.0, -1.0),
                (-1.0, -1.0, -1.0),
            ))
            edges = _np.asarray((
                (0, 1, 2, 3),
                (0, 1, 5, 4),
                (1, 2, 6, 5),
                (2, 3, 7, 6),
                (3, 0, 4, 7),
                (4, 5, 6, 7),
            ))

        # scale vertices to account for the dimensions
        vertices = transform.apply((vertices * dimensions).T)
        # close the circle and append first edge to the list of edges
        edges = _np.hstack((edges, edges[:, 0, _np.newaxis]))

        # off to plotting
        self.figure.add_trace(
            go.Scatter(
                **self._prepare_plot_coordinates(
                    self._extract_coordinates(vertices[:, edges])),
                mode='lines',
                fill='toself',
                line=dict(
                    color='rgb(13, 13, 13)',
                ),
                fillcolor='rgb(178, 178, 178)',
                name='cuboid',
                hoverinfo='skip',
                hovertext='',
                showlegend=False
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
                        size=3 if self._NUMBER_OF_AXES == 3 else 5,
                    ),
                    showlegend=False,
                ), kwargs)
            )
        )

        # plot each coordinate axis i.e., x, y, z or which of them are available
        for idx in range(self._NUMBER_OF_COORDINATES):
            # plotdata = self._build_plotdata_kwargs(_np.hstack((
            #     # where to place the point
            #     position,
            #     # and where to point it to
            #     position + 0.25 * dcm.dot(
            #         self._parse_coordinate(self.COORDINATE_DIRECTIONS[idx]))
            # )))
            # convert rgb in range of [0...1] to RGB in range of [0...255]
            rgb = self._rgb2RGB(self.COORDINATE_DIRECTIONS[idx])

            # plot the axis as a line (currently, a quiver isn't supported in
            # 2D... no idea why, plot.ly?!)
            self.figure.add_trace(
                self._scatter(
                    **self._prepare_plot_coordinates(
                        self._extract_coordinates(_np.hstack((
                            position, position + 0.25 * dcm.dot(
                                self.COORDINATE_DIRECTIONS[idx])
                        )))),
                    **update_recursive(dict(
                        mode='lines',
                        line_color=f'rgb({rgb[0]},{rgb[1]},{rgb[2]})',
                        name=f'{kwargs.get("name")}: axis {idx}',
                        hoverinfo='text',
                        hovertext=f'{kwargs.get("name")}: axis {idx}',
                        showlegend=False,
                    ), kwargs)
                )
            )

    def render_cylinder(self,
                        cylinder: '_cylinder.Cylinder',
                        *args, **kwargs):
        pass

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
                                 cylinder: '_el_cylinder.EllipticCylinder',
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

    def render_kinematic_chain(self,
                               kinematic_chain:
                               '_kinematic_chain.KinematicChain',
                               *args,
                               **kwargs):
        pass

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
                        go.Mesh3d(
                            **self._prepare_plot_coordinates(
                                self._extract_coordinates(vertices.T)),
                            **self._prepare_plot_coordinates(edges.T,
                                                             ('i', 'j', 'k')),
                            color='rgb(0, 0, 0)',
                            facecolor=['rgb(178, 178, 178)'] * edges.shape[0],
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
                            go.Scatter3d(
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
                                          else 'solid'
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
                **self._prepare_plot_coordinates(self._extract_coordinates(
                    transformation.apply(anchor.linear.position))),
                **update_recursive(dict(
                    mode='markers',
                    marker=dict(
                        color='Red',
                        size=3 if self._NUMBER_OF_AXES == 3 else 5,
                    ),
                    name=f'platform {pidx}: anchor {aidx}',
                    hoverinfo='text',
                    hovertext=f'platform {pidx}: anchor {aidx}',
                    showlegend=False,
                ), kwargs)
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
        for list_name in ('platforms', 'kinematic_chains'):
            self._render_component_list(robot, list_name, **kwargs)

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
        # option to plot only the points inside the workspace
        only_inside = kwargs.pop('only_inside', False)

        # find the correct scatter object
        scatter = go.Scatter3d if self._NUMBER_OF_AXES == 3 else go.Scatter

        # plot the points inside the workspace
        self.figure.add_trace(
            scatter(
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
                scatter(
                    **self._prepare_plot_coordinates(
                        self._extract_coordinates(workspace.outside.T)),
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
                              workspace: '_hull.HullResult',
                              *args,
                              **kwargs):
        if self._NUMBER_OF_AXES != 3:
            raise NotImplementedError()

        # as simple as that
        self.figure.add_trace(
            go.Mesh3d(
                **self._prepare_plot_coordinates(self._extract_coordinates(workspace.vertices.T)),
                **self._prepare_plot_coordinates(workspace.faces.T, ('i', 'j', 'k')),
                facecolor=['rgb(255, 0, 0)'] * workspace.faces.shape[0],
                vertexcolor=['rgb(0, 0, 0)'] * workspace.vertices.shape[0],
                flatshading=True,
                opacity=0.75,
                contour=dict(
                    show=True,
                    color='rgb(0, 0, 0)',
                ),
                name='workspace',
                hoverinfo='skip',
                hovertext='',
                **kwargs,
            )
        )

    def _prepare_plot_coordinates(self, coordinates: Union[Vector, Matrix],
                                  axes: Sequence = None):
        # default value for the axes be ('x', 'y', 'z') if not given elsewise
        if axes is None:
            axes = self.AXES_NAMES

        # return result as a dictionary of ('e0': [], 'e1': [], ..., 'en': [])
        return dict(zip(axes[0:self._NUMBER_OF_AXES],
                        super()._prepare_plot_coordinates(coordinates)))


__all__ = [
    'Plotly',
]

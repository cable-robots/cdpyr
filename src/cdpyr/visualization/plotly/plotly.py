from abc import ABC, abstractmethod
from collections import Mapping
from typing import AnyStr, Sequence

import numpy as _np
from plotly import graph_objects as go
from scipy.spatial import ConvexHull as _ConvexHull, Delaunay as _Delaunay

from cdpyr.geometry import (
    cuboid as _cuboid,
    cylinder as _cylinder,
    sphere as _sphere,
    tube as _tube,
)
from cdpyr.kinematics.transformation import Homogenous as \
    _HomogenousTransformation
from cdpyr.robot import (
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
from cdpyr.typing import Matrix, Vector
from cdpyr.visualization import visualizer as _visualizer

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"


def update_recursive(defaults, update):
    for k, v in update.items():
        if isinstance(v, Mapping):
            defaults[k] = update_recursive(defaults.get(k, {}), v)
        else:
            defaults[k] = v
    return defaults


class Plotly(_visualizer.Visualizer):
    _figure: go.Figure

    COORDINATE_NAMES = ['x', 'y', 'z']

    def __init__(self, *args, **kwargs):
        super().__init__()
        self._figure = None
        self._NUMBER_OF_COORDINATES = 2
        self._NUMBER_OF_AXES = 2

    @property
    def figure(self):
        if self._figure is None:
            self.figure = go.Figure()

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

    def close(self):
        pass

    def draw(self):
        self._figure.update_layout()

    def reset(self):
        self._figure.layout = {}
        self.figure = go.Figure()

    def show(self):
        self._figure.update_layout(
            yaxis=dict(
                scaleanchor="x",
                scaleratio=1,
            ),
            scene=dict(
                aspectmode='data',
                aspectratio=dict(
                    x=1.00,
                    y=1.00,
                    z=1.00
                )
            )
        )
        self._figure.show()

    def render_cuboid(self,
                      cuboid: '_cuboid.Cuboid',
                      *args, **kwargs):
        pass

    def render_coordinate_system(self,
                                 position: Vector = None,
                                 dcm: Matrix = None,
                                 **kwargs):
        # default position
        position = self._parse_coordinate(position)

        # default rotation
        dcm = self._parse_dcm(dcm)

        # draw center of the coordinate system
        self.figure.add_trace(
            self._scatter(
                **self._build_plotdata_kwargs(position),
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
            plotdata = self._build_plotdata_kwargs(_np.hstack((
                # where to place the point
                position,
                # and where to point it to
                position + 0.25 * dcm.dot(
                    self._parse_coordinate(self.COORDINATE_DIRECTIONS[idx]))
            )))
            # convert rgb in range of [0...1] to RGB in range of [0...255]
            rgb = self._rgb2RGB(self.COORDINATE_DIRECTIONS[idx])

            # plot the axis as a line (currently, a quiver isn't supported in
            # 2D... no idea why, plot.ly?!)
            self.figure.add_trace(
                self._scatter(
                    **plotdata,
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
        # prepare position and orientation of the anchor
        position = self._parse_coordinate(anchor.linear.position)
        dcm = self._parse_dcm(anchor.angular.dcm)

        # get loop index
        aidx = kwargs.pop('loop_index', -1)

        # plot coordinate system
        self.render_coordinate_system(position,
                                      dcm,
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

        # TODO remove temporary loop variables
        # temporary platform loop index
        pidx = kwargs.pop('loop_index', -1)

        # render bounding box of platform
        if not platform.is_point:
            # get anchors in platform coordinates
            anchors = self._parse_coordinate(platform.bi)

            # in 3D, we perform delaunay triangulation of the corners and retrieve the convex hull from there
            if self._NUMBER_OF_AXES == 3:
                delau = _Delaunay(anchors.T)

                vertices = delau.convex_hull
                points = delau.points
            # in any other case, we simply calculate the convex hull of the anchors
            else:
                # calculate convex hull of the platform shape
                cv = _ConvexHull(anchors.T)
                # and get all vertices and points in the correct sorted order
                vertices = cv.vertices
                points = cv.points
                # to close the loop of vertices, we will append the first one to the list
                vertices = _np.append(vertices, vertices[0])

            # also rotate and translate the platform anchors
            anchors_rotated = self._parse_coordinate(position) \
                              + self._parse_dcm(dcm).dot(points.T)

            # 3D plot
            if self._NUMBER_OF_AXES == 3:
                # first, plot the mesh of the platform i.e., its volume
                self.figure.add_trace(
                    go.Mesh3d(
                        **self._build_plotdata_kwargs(anchors_rotated),
                        **self._build_plotdata_kwargs(vertices.T,
                                                      ['i', 'j', 'k']),
                        color='rgb(0, 0, 0)',
                        facecolor=['rgb(178, 178, 178)'] * vertices.shape[0],
                        flatshading=True,
                        name='',
                        hoverinfo='skip',
                        hovertext='',
                    )
                )
                vertices = _np.hstack((vertices, vertices[:,0,_np.newaxis]))
                for vertex in vertices:
                    # # close the vertex
                    # vertex = _np.append(vertex, vertex[0])
                    # then, we will plot the edges so that they are visible
                    self.figure.add_trace(
                        go.Scatter3d(
                            **self._build_plotdata_kwargs([anchors_rotated[0,vertex], anchors_rotated[1,vertex], anchors_rotated[2,vertex]]),
                            mode='lines',
                            line_color='rgb(13, 13, 13)',
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
                        **self._build_plotdata_kwargs(anchors_rotated[:,vertices]),
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
                                    transform=platform.pose.transformation,
                                    platform_index=pidx,
                                    **kwargs
                                    )

        # render reference coordinate system of platform
        self.render_coordinate_system(position,
                                      name=f'platform {pidx}',
                                      hovertext=f'platform {pidx}',
                                      hoverinfo='text',
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
                               transform: _HomogenousTransformation = None,
                               **kwargs):
        # prepare position and orientation of the anchor
        position = anchor.linear.position
        dcm = anchor.angular.dcm

        # default value for transformation, if the platform has no pose
        if transform is None:
            transform = _HomogenousTransformation()

        aidx = kwargs.pop('loop_index', -1)
        pidx = kwargs.pop('platform_index', -1)

        # transform the position
        position = self._parse_coordinate(transform.apply(position))

        self.figure.add_trace(
            self._scatter(
                **self._build_plotdata_kwargs(position),
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

    def _parse_coordinate(self, coordinate: Vector = None) -> _np.ndarray:
        if coordinate is None:
            coordinate = [0.0] * self._NUMBER_OF_AXES

        # anything into a numpy array
        coordinate = _np.asarray(coordinate)

        # scalars into vectors
        if coordinate.ndim == 0:
            coordinate = _np.asarray([coordinate])

        # turrn vectors into matrices
        if coordinate.ndim == 1:
            coordinate = coordinate[:, _np.newaxis]

        # add rows of zeros below the coordinate to make it a valid matrix
        # coordinate = _np.vstack((coordinate, _np.zeros((self._NUMBER_OF_AXES -
        # self._NUMBER_OF_COORDINATES[0:self._NUMBER_OF_COORDINATES,:],
        # coordinate.shape[1]))))
        return _np.vstack((coordinate[0:self._NUMBER_OF_COORDINATES, :],
                           _np.zeros((
                               self._NUMBER_OF_AXES -
                               self._NUMBER_OF_COORDINATES,
                               coordinate.shape[1]))))

    def _parse_dcm(self, dcm: Matrix = None):
        if dcm is None:
            dcm = _np.eye(self._NUMBER_OF_AXES)

        return _np.asarray(dcm)[0:self._NUMBER_OF_AXES, 0:self._NUMBER_OF_AXES]

    def _build_plotdata_kwargs(self,
                               coordinates: Matrix,
                               axes: Sequence[AnyStr] = None):
        if axes is None:
            axes = self.COORDINATE_NAMES

        return dict(zip(axes[0:self._NUMBER_OF_AXES],
                        [[ax] if isinstance(ax, float) else ax for ax in
                         coordinates]))


__all__ = [
    'Plotly',
]

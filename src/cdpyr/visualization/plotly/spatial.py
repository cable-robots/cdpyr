import itertools
from typing import Optional

import numpy as _np
from plotly import graph_objects as go
from scipy.spatial import Delaunay as _Delaunay

from cdpyr.geometry import (
    cuboid as _cuboid,
    cylinder as _cylinder,
    elliptic_cylinder as _elliptic_cylinder,
    sphere as _sphere,
    tube as _tube,
)
from cdpyr.kinematics.transformation import Homogenous as \
    _HomogenousTransformation
from cdpyr.typing import Matrix, Num
from cdpyr.visualization.plotly import plotly as _plotly

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"


class Spatial(_plotly.Plotly):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._NUMBER_OF_COORDINATES = 3
        self._NUMBER_OF_AXES = 3

    def render_cuboid(self,
                      cuboid: '_cuboid.Cuboid',
                      *args, **kwargs):
        # get transformation to apply
        transform = kwargs.get('transformation', _HomogenousTransformation())

        # generate a mesh of data
        width = cuboid.width
        depth = cuboid.depth
        height = cuboid.height

        # plot the tube surrounding surface
        points = _np.asarray(self._apply_transformation(*_np.hstack(
            _np.asarray([
                x, y, z,
            ])[:, _np.newaxis]
            for x, y, z in
            itertools.product((-width / 2, width / 2), (-depth / 2, depth / 2),
                              (-height / 2, height / 2))
        ), transform))

        # plot the top and bottom closing
        delau = _Delaunay(points.T)

        # get convex hull and points of cuboid Delaunay triangulation
        vertices = delau.convex_hull
        points = delau.points

        # first, plot the mesh of the platform i.e., its volume
        self.figure.add_trace(
            go.Mesh3d(
                **self._build_plotdata_kwargs(points.T),
                **self._build_plotdata_kwargs(vertices.T,
                                              ['i', 'j', 'k']),
                color='rgb(0, 0, 0)',
                facecolor=['rgb(178, 178, 178)'] * vertices.shape[
                    0],
                flatshading=True,
                name='',
                hoverinfo='skip',
                hovertext='',
            )
        )
        # then plot each edge/vertex of the platform
        vertices = _np.hstack(
            (vertices, vertices[:, 0, _np.newaxis]))
        for vertex in vertices:
            self.figure.add_trace(
                go.Scatter3d(
                    **self._build_plotdata_kwargs([
                        points[vertex, 0],
                        points[vertex, 1],
                        points[vertex, 2]
                    ]),
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

    def render_cylinder(self,
                        cylinder: '_cylinder.Cylinder',
                        *args,
                        **kwargs):
        return self._render_generic_cylinder(
            *args,
            height=cylinder.height,
            major_radius=cylinder.radius,
            minor_radius=cylinder.radius,
            **kwargs)

    def render_elliptic_cylinder(self,
                                 cylinder:
                                 '_elliptic_cylinder.EllipticCylinder',
                                 *args,
                                 **kwargs):
        return self._render_generic_cylinder(
            *args,
            height=cylinder.height,
            major_radius=cylinder.major_radius,
            minor_radius=cylinder.minor_radius,
            **kwargs)

    def render_sphere(self,
                      sphere: '_sphere.Sphere',
                      *args,
                      **kwargs):
        # get transformation to apply
        transform = kwargs.get('transformation', _HomogenousTransformation())

        # generate a mesh of data
        radius = sphere.radius
        azimuth = _np.linspace(-_np.pi, _np.pi, num=93, endpoint=True)
        elevation = _np.linspace(-_np.pi / 2, _np.pi / 2, num=17, endpoint=True)

        # triangulate through all the coordinates on the sphere surface
        delau = _Delaunay(_np.asarray(transform.apply(_np.hstack(
            radius * _np.asarray([
                _np.cos(az) * _np.cos(el),
                _np.sin(az) * _np.cos(el),
                _np.sin(el),
            ])[:, _np.newaxis]
            for az in azimuth
            for el in elevation
        ))).transpose())

        # a linspace from [0, 2*pi]
        pi_linspace = _np.linspace(0, 2 * _np.pi, num=93, endpoint=True)

        # calculate the xy, yz, xz ring coordinates
        azs = [pi_linspace, _np.pi / 2 * _np.ones_like(pi_linspace),
               _np.zeros_like(pi_linspace)]
        els = [_np.zeros_like(pi_linspace), pi_linspace, pi_linspace]
        rings = [radius * _np.asarray([
            _np.cos(az) * _np.cos(el),
            _np.sin(az) * _np.cos(el),
            _np.sin(el),
        ]) for az, el in zip(azs, els)]

        # get vertices and points of the sphere's complex hull
        vertices = delau.convex_hull
        points = delau.points

        # first, plot the mesh of the platform i.e., its volume
        self.figure.add_trace(
            go.Mesh3d(
                **self._build_plotdata_kwargs(points.T),
                **self._build_plotdata_kwargs(vertices.T,
                                              ['i', 'j', 'k']),
                color='rgb(0, 0, 0)',
                facecolor=['rgb(178, 178, 178)'] * vertices.shape[
                    0],
                flatshading=True,
                name='',
                hoverinfo='skip',
                hovertext='',
            )
        )

        # loop over each ring to plot
        for ring in rings:
            # plot ring
            self.figure.add_trace(
                go.Scatter3d(
                    **self._build_plotdata_kwargs(ring),
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

    def render_tube(self,
                    tube: '_tube.Tube',
                    *args,
                    **kwargs):
        # get properties from tube
        height = tube.height

        # loop over the inner and outer radius
        for radius in (tube.inner_radius, tube.outer_radius):
            self._render_generic_cylinder(height, radius, radius, **kwargs)

    def _render_generic_cylinder(self,
                                 height: Num,
                                 major_radius: Num,
                                 *args,
                                 minor_radius: Optional[Num] = None,
                                 **kwargs):
        # get transformation to apply
        transform = kwargs.pop('transformation', _HomogenousTransformation())

        # get properties from tube
        if minor_radius is None:
            minor_radius = major_radius

        # generate meshes of data for ...
        # ... surface
        azimuth = _np.linspace(0, 2 * _np.pi, num=37, endpoint=True)
        elevation = _np.linspace(-height / 2, height / 2, num=11, endpoint=True)

        # perform triangulation on transformed coordinates of the cylinder shape
        delau = _Delaunay(_np.asarray(
            self._apply_transformation(
                *_np.vstack(
                    [
                        major_radius * _np.cos(az),
                        minor_radius * _np.sin(az),
                        el,
                    ]
                    for el in elevation
                    for az in azimuth
                ).T,
                transform)
        ).transpose())

        # calculate the upper and lower ring coordinates
        rings = [_np.asarray([[
            major_radius * _np.cos(az),
            minor_radius * _np.sin(az),
            el,
        ] for az in azimuth]) for el in [elevation[0], elevation[-1]]]

        # get vertices and points of the surface triangulation
        vertices = delau.convex_hull
        points = delau.points

        # first, plot the mesh of the platform i.e., its volume
        self.figure.add_trace(
            go.Mesh3d(
                **self._build_plotdata_kwargs(points.T),
                **self._build_plotdata_kwargs(vertices.T,
                                              ['i', 'j', 'k']),
                color='rgb(0, 0, 0)',
                facecolor=['rgb(178, 178, 178)'] * vertices.shape[
                    0],
                flatshading=True,
                name='',
                hoverinfo='skip',
                hovertext='',
            )
        )

        # loop over each ring to plot
        for ring in rings:
            # plot ring
            self.figure.add_trace(
                go.Scatter3d(
                    **self._build_plotdata_kwargs(ring.transpose()),
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

    def _apply_transformation(self,
                              x: Matrix,
                              y: Matrix,
                              z: Matrix,
                              transformation: _HomogenousTransformation):
        xyz = transformation.apply(_np.stack((x, y, z), axis=0))

        try:
            return xyz[0, :, :], xyz[1, :, :], xyz[2, :, :]
        except IndexError:
            return xyz[0, :], xyz[1, :], xyz[2, :]


__all__ = [
    'Spatial',
]

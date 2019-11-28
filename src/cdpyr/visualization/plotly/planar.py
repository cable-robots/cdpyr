from typing import Optional

import numpy as _np
from plotly import graph_objects as go

from cdpyr.analysis.workspace.grid import grid_result as _grid
from cdpyr.analysis.workspace.hull import hull_result as _hull
from cdpyr.geometry import (
    cuboid as _cuboid,
    cylinder as _cylinder,
    elliptic_cylinder as _elliptic_cylinder,
    sphere as _sphere,
    tube as _tube
)
from cdpyr.kinematics.transformation import Homogenous as \
    _HomogenousTransformation
from cdpyr.typing import (
    Matrix,
    Num
)
from cdpyr.visualization.plotly import plotly as _plotly

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"


class Planar(_plotly.Plotly):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._NUMBER_OF_COORDINATES = 2
        self._NUMBER_OF_AXES = 2

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
        width = cuboid.width
        depth = cuboid.depth

        # calculate vertices and edges of the cuboid
        vertices = _np.vstack(self._apply_transformation(*_np.vstack([
            [-width / 2, depth / 2],
            [width / 2, depth / 2],
            [width / 2, -depth / 2],
            [-width / 2, -depth / 2],
        ]).T, transform))
        edges = [0, 1, 2, 3, 0]

        # off to plotting
        self.figure.add_trace(
            go.Scatter(
                **self._build_plotdata_kwargs(vertices[:, edges]),
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

    def render_cylinder(self,
                        cylinder: '_cylinder.Cylinder',
                        *args,
                        **kwargs):
        return self._render_generic_cylinder(
            cylinder.radius,
            *args,
            minor_radius=cylinder.radius,
            name='cylinder',
            **kwargs)

    def render_elliptic_cylinder(self,
                                 cylinder:
                                 '_elliptic_cylinder.EllipticCylinder',
                                 *args,
                                 **kwargs):
        return self._render_generic_cylinder(
            cylinder.major_radius,
            *args,
            minor_radius=cylinder.minor_radius,
            name='cylinder',
            **kwargs)

    def render_sphere(self,
                      sphere: '_sphere.Sphere',
                      *args,
                      **kwargs):
        return self._render_generic_cylinder(
            sphere.radius,
            *args,
            minor_radius=sphere.radius,
            name='sphere',
            **kwargs)

    def render_tube(self,
                    tube: '_tube.Tube',
                    *args,
                    **kwargs):
        # loop over the inner and outer radius
        for radius in (tube.inner_radius, tube.outer_radius):
            self._render_generic_cylinder(radius, radius, **kwargs)

    def render_workspace_grid(self,
                              workspace: '_grid.GridResult',
                              *args,
                              **kwargs):
        pass

    def render_workspace_hull(self,
                              workspace: '_hull.HullResult',
                              *args,
                              **kwargs):
        pass

    def _render_generic_cylinder(self,
                                 major_radius: Num,
                                 *args,
                                 minor_radius: Optional[Num] = None,
                                 **kwargs):
        # get transformation to apply
        transform = kwargs.pop('transformation', _HomogenousTransformation())

        # default minor radius to major radius if not given
        if minor_radius is None:
            minor_radius = major_radius

        # generate meshes of data for ...
        # ... surface
        azimuth = _np.linspace(0, 2 * _np.pi, num=37, endpoint=True)

        # perform triangulation on transformed coordinates of the cylinder shape
        surrounding = _np.vstack(self._apply_transformation(
            *_np.vstack([
                [
                    major_radius * _np.cos(az),
                    minor_radius * _np.sin(az),
                ]
                for az in azimuth
            ]).T,
            transform)).T

        # first, plot the mesh of the platform i.e., its volume
        self.figure.add_trace(
            go.Scatter(
                **self._build_plotdata_kwargs(surrounding.T),
                mode='lines',
                fill='toself',
                line=dict(
                    color='rgb(13, 13, 13)',
                ),
                fillcolor='rgb(178, 178, 178)',
                hoverinfo='skip',
                hovertext='',
                showlegend=False,
                **kwargs,
            )
        )

    def _apply_transformation(self,
                              x: Matrix,
                              y: Matrix,
                              transformation: _HomogenousTransformation):
        z = _np.zeros_like(x)
        xy = transformation.apply(_np.stack((x, y, z), axis=0))

        try:
            return xy[0, :, :], xy[1, :, :]
        except IndexError:
            return xy[0, :], xy[1, :]


__all__ = [
    'Planar',
]

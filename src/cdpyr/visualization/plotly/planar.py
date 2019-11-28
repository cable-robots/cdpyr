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
    tube as _tube,
)
from cdpyr.kinematics.transformation import Homogenous as \
    _HomogenousTransformation
from cdpyr.typing import (
    Num
)
from cdpyr.visualization.plotly import plotly as _plotly

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"


class Planar(_plotly.Plotly):
    _NUMBER_OF_COORDINATES = 2
    _NUMBER_OF_AXES = 2

    def render_cylinder(self,
                        cylinder: '_cylinder.Cylinder',
                        *args,
                        **kwargs):
        self._render_generic_cylinder(cylinder.radius,
                                      *args,
                                      minor_radius=cylinder.radius,
                                      name='cylinder',
                                      **kwargs)

    def render_elliptic_cylinder(self,
                                 cylinder:
                                 '_elliptic_cylinder.EllipticCylinder',
                                 *args,
                                 **kwargs):
        self._render_generic_cylinder(cylinder.major_radius,
                                      *args,
                                      minor_radius=cylinder.minor_radius,
                                      name='cylinder',
                                      **kwargs)

    def render_sphere(self,
                      sphere: '_sphere.Sphere',
                      *args,
                      **kwargs):
        self._render_generic_cylinder(sphere.radius,
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
        surrounding = transform.apply(_np.vstack([
            [
                major_radius * _np.cos(az),
                minor_radius * _np.sin(az),
                0 * az
            ]
            for az in azimuth
        ]).T)

        # first, plot the mesh of the platform i.e., its volume
        self.figure.add_trace(
            go.Scatter(
                **self._prepare_plot_coordinates(
                    self._extract_coordinates(surrounding), self.AXES_NAMES),
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


__all__ = [
    'Planar',
]

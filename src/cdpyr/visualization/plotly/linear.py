from cdpyr.analysis.workspace.grid import grid_result as _grid
from cdpyr.analysis.workspace.hull import hull_result as _hull
from cdpyr.geometry import (
    cuboid as _cuboid,
    cylinder as _cylinder,
    elliptic_cylinder as _elliptic_cylinder,
    sphere as _sphere,
    tube as _tube,
)
from cdpyr.visualization.plotly import plotly as _plotly

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"


class Linear(_plotly.Plotly):
    _NUMBER_OF_COORDINATES = 1
    _NUMBER_OF_AXES = 2

    def draw(self):
        self.figure.update_layout(
            yaxis=dict(
                scaleanchor="x",
                scaleratio=1,
                showline=False,
                showticklabels=False,
                showgrid=False
            )
        )
        super().draw()

    # def render_cuboid(self,
    #                   cuboid: '_cuboid.Cuboid',
    #                   *args,
    #                   **kwargs):
    #     raise NotImplementedError()

    # def render_cylinder(self,
    #                     cylinder: '_cylinder.Cylinder',
    #                     *args,
    #                     **kwargs):
    #     raise NotImplementedError()
    #
    # def render_elliptic_cylinder(self,
    #                              cylinder:
    #                              '_elliptic_cylinder.EllipticCylinder',
    #                              *args,
    #                              **kwargs):
    #     raise NotImplementedError()
    #
    # def render_sphere(self,
    #                   sphere: '_sphere.Sphere',
    #                   *args,
    #                   **kwargs):
    #     raise NotImplementedError()
    #
    # def render_tube(self,
    #                 tube: '_tube.Tube',
    #                 *args,
    #                 **kwargs):
    #     raise NotImplementedError()
    #
    # def render_workspace_grid(self,
    #                           workspace: '_grid.GridResult',
    #                           *args,
    #                           **kwargs):
    #     pass
    #
    # def render_workspace_hull(self,
    #                           workspace: '_hull.HullResult',
    #                           *args,
    #                           **kwargs):
    #     pass


__all__ = [
    'Linear',
]
#

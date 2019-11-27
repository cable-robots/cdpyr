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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._NUMBER_OF_COORDINATES = 1
        self._NUMBER_OF_AXES = 2

    def draw(self):
        self.figure.update_layout(
                yaxis=dict(
                        showline=False,
                        showticklabels=False,
                        showgrid=False
                )
        )
        super().draw()

    def render_cuboid(self,
                      cuboid: '_cuboid.Cuboid',
                      *args,
                      **kwargs):
        pass

    def render_cylinder(self,
                        cylinder: '_cylinder.Cylinder',
                        *args,
                        **kwargs):
        pass

    def render_elliptic_cylinder(self,
                                 cylinder:
                                 '_elliptic_cylinder.EllipticCylinder',
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


__all__ = [
        'Linear',
]

from typing import Optional, Tuple, Union

from magic_repr import make_repr

from cdpyr.geometry.geometry import Geometry  # , GeometrySchema
from cdpyr.kinematics.transformation.angular import (
    Angular as AngularTransformation,
    # AngularSchema as AngularTransformationSchema,
)
from cdpyr.mechanics.inertia import Inertia  # , InertiaSchema
from cdpyr.typing import Matrix, Num, Vector


class Pulley(object):
    _geometry: Geometry
    _inertia: Inertia
    _angular: AngularTransformation

    def __init__(self,
                 geometry: Optional[Geometry] = None,
                 inertia: Optional[Union[Tuple[Vector, Matrix], Inertia]] = None,
                 rotation: Optional[
                     Union[Matrix, AngularTransformation]] = None
                 ):
        self.geometry = geometry or Geometry()
        self.inertia = inertia or Inertia()
        self.angular = rotation or AngularTransformation()

    @property
    def geometry(self):
        return self._geometry

    @geometry.setter
    def geometry(self, geometry: Geometry):
        self._geometry = geometry

    @geometry.deleter
    def geometry(self):
        del self._geometry

    @property
    def inertia(self):
        return self._inertia

    @inertia.setter
    def inertia(self, inertia: Union[Tuple[Vector, Matrix], Inertia]):
        if not isinstance(inertia, Inertia):
            inertia = Inertia(linear=inertia[0], angular=inertia[1])

        self._inertia = inertia

    @inertia.deleter
    def inertia(self):
        del self._inertia

    @property
    def angular(self):
        return self._angular

    @angular.setter
    def angular(self, angular: AngularTransformation):
        self._angular = angular

    @angular.deleter
    def angular(self):
        del self.angular


Pulley.__repr__ = make_repr(
    'geometry',
    'inertia',
    'angular'
)

__all__ = [
    'Pulley',
]

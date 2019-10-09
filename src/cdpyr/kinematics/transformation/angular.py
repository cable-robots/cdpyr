import numpy as np_
from magic_repr import make_repr
from scipy.spatial.transform import Rotation

from cdpyr.typing import Matrix, Vector

from cdpyr import validator as _validator


class Angular(object):
    _angular_rotation: Rotation = Rotation.from_quat([0.0, 0.0, 0.0, 1.0])
    _angular_velocity: np_.ndarray = np_.array([0.0, 0.0, 0.0])
    _angular_acceleration: np_.ndarray = np_.array([0.0, 0.0, 0.0])
    _rotation_sequence: str = 'zyx'

    """
    A kinematic angular transformation object.

    This object represents a kinematic transformation on the orientation or 
    angular space. It allows for describing and reading the angular 
    orientation in different ways like DCM (orientation matrix), quaternion, 
    rotation vectors, or Euler angles.
    
    Attributes
    ----------
    rotation : Rotation
    
    sequence : str
    
    dcm : ndarray
    
    quaternion : ndarray
    
    rotvec : ndarray
    
    euler : ndaray
    
    angular_velocity : ndarray
    
    angular_acceleration : ndarray
    """

    def __init__(self,
                 euler: Vector = None,
                 quaternion: Vector = None,
                 dcm: Matrix = None,
                 rotvec: Vector = None,
                 angular_velocity: Vector = None,
                 angular_acceleration: Vector = None,
                 rotation_sequence: str = None
                 ):
        """
        Parameters
        ----------
        euler : iterable or (3, ) ndarray, optional
            Euler angles of the rotation. Interpreted according to the value of
            ``rotation_sequence``
        quaternion : iterable or (4, ) ndarray, optional
            Quaternion representation of the rotation in scalar-last notation.
        dcm : iterable or (3, 3) ndarray, optional
            Conventional rotation matrix representation of the rotation
        rotvec : iterable or (3, ) ndarray, optional
            A rotation vector is a 3 dimensional vector which is
            co-directional to the axis of rotation and whose norm gives the
            angle of rotation (in radians)
        angular_velocity : iterable or (3, ) ndarray, optional
            Angular velocity at the current instance as give in the local
            coordinate system. Defaults to [0., 0., 0.]
        angular_acceleration : iterable or (3, ) ndarray, optional
            Angular acceleration as given in the local coordinate system.
            Defaults to [0., 0., 0.]
        rotation_sequence : str
            Valid rotation sequences to instantiate the object with. Refers
            to the Euler extrinsic or intrinsic parameter. Defaults to 'zyx'

        See Also
        --------
        scipy.spatial.transform.Rotation: Underlying implementation of the
        rotation object
        """

        self.sequence = rotation_sequence or 'zyx'
        if euler is not None and \
            quaternion is None and \
            dcm is None and \
            rotvec is None:
            self.euler = euler
        if euler is None and \
            quaternion is not None and \
            dcm is None and \
            rotvec is None:
            self.quaternion = quaternion
        if euler is None and \
            quaternion is None and \
            dcm is not None and \
            rotvec is None:
            self.dcm = dcm
        if euler is None and \
            quaternion is None and \
            dcm is None and rotvec is\
            not None:
            self.rotvec = rotvec

        self.angular_velocity = angular_velocity \
            if angular_velocity is not None \
            else [0.0, 0.0, 0.0]
        self.angular_acceleration = angular_acceleration \
            if angular_acceleration is not None \
            else [0.0, 0.0, 0.0]

    @property
    def rotation(self):
        return self._angular_rotation

    @rotation.setter
    def rotation(self, rotation: Rotation):
        self._angular_rotation = rotation

    @rotation.deleter
    def rotation(self):
        del self._angular_rotation

    @property
    def sequence(self):
        return self._rotation_sequence

    @sequence.setter
    def sequence(self, sequence: str):
        self._rotation_sequence = sequence

    @sequence.deleter
    def sequence(self):
        del self._rotation_sequence

    @property
    def euler(self):
        return self._angular_rotation.as_euler(self.sequence)

    @euler.setter
    def euler(self, euler: Vector):
        self.rotation = Rotation.from_euler(self.sequence, euler)

    @euler.deleter
    def euler(self):
        del self.rotation

    @property
    def dcm(self):
        return self._angular_rotation.as_dcm()

    @dcm.setter
    def dcm(self, dcm: Matrix):
        self.rotation = Rotation.from_dcm(dcm)

    @dcm.deleter
    def dcm(self):
        del self.rotation

    @property
    def quaternion(self):
        return self._angular_rotation.as_quat()

    @quaternion.setter
    def quaternion(self, quaternion: Vector):
        self.rotation = Rotation.from_quat(quaternion)

    @quaternion.deleter
    def quaternion(self):
        del self.rotation

    @property
    def rotvec(self):
        return self._angular_rotation.as_rotvec()

    @rotvec.setter
    def rotvec(self, rotvec: Vector):
        self.rotation = Rotation.from_rotvec(rotvec)

    @rotvec.deleter
    def rotvec(self):
        del self.rotation

    @property
    def angular_velocity(self):
        return self._angular_velocity

    @angular_velocity.setter
    def angular_velocity(self, velocity: Vector):
        velocity = np_.asarray(velocity)

        if velocity.ndim != 1:
            raise ValueError(
                'invalid dimension. angular_velocity must be a 1-dimensional '
                'list or array')

        if velocity.shape != (3,):
            raise ValueError(
                'invalid shape. angular_velocity must be a 3-element list or '
                'a (3,) numpy array')

        self._angular_velocity = velocity

    @angular_velocity.deleter
    def angular_velocity(self):
        del self._angular_velocity

    @property
    def angular_acceleration(self):
        return self._angular_acceleration

    @angular_acceleration.setter
    def angular_acceleration(self, acceleration: Vector):
        acceleration = np_.asarray(acceleration)

        if acceleration.ndim != 1:
            raise ValueError(
                'invalid dimension. angular_acceleration must be a '
                '1-dimensional list or array')

        if acceleration.shape != (3,):
            raise ValueError(
                'invalid shape. angular_acceleration must be a 3-element list '
                'or a (3,) numpy array')

        self._angular_acceleration = acceleration

    @angular_acceleration.deleter
    def angular_acceleration(self):
        del self._angular_acceleration


Angular.__repr__ = make_repr(
    'dcm',
    'angular_velocity',
    'angular_acceleration'
)

__all__ = [
    'Angular',
]

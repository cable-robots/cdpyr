import re
from typing import AnyStr, Optional, Union

import numpy as np_
from magic_repr import make_repr

from cdpyr import validator as _validator
from cdpyr.kinematics.transformation import transformation as _transformation
from cdpyr.typing import Matrix, Num, Vector

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"


class Angular(_transformation.Transformation):
    """
    A kinematic angular transformation object.

    This object represents a kinematic transformation on the orientation or
    angular space. It allows for describing and reading the angular
    orientation in different ways like DCM (orientation matrix), quaternion,
    rotation vectors, or Euler angles.

    Attributes
    ----------
    sequence : AnyStr

    dcm : ndarray

    quaternion : ndarray

    rotvec : ndarray

    euler : ndaray

    angular_velocity : ndarray

    angular_acceleration : ndarray
    """

    _quaternion: Vector = np_.asarray([0.0, 0.0, 0.0, 1.0])
    _angular_velocity: np_.ndarray = np_.asarray((0., 0., 0.))
    _angular_acceleration: np_.ndarray = np_.asarray((0., 0., 0.))
    """
    Intrinsic orientation about local Z, then local Y, then local X axis
    """
    sequence: AnyStr = 'XYZ'

    _AXIS_TO_IND = {'x': 0, 'y': 1, 'z': 2}

    def __init__(self,
                 dcm: Optional[Matrix] = None,
                 angular_velocity: Optional[Vector] = None,
                 angular_acceleration: Optional[Vector] = None,
                 quaternion: Optional[Vector] = None,
                 rotvec: Optional[Vector] = None,
                 euler: Optional[Vector] = None,
                 sequence: Optional[AnyStr] = None,
                 **kwargs):
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
        sequence : AnyStr
            Valid rotation sequences to instantiate the object with. Refers
            to the Euler extrinsic or intrinsic parameter. Defaults to 'zyx'

        See Also
        --------
        scipy.spatial.transform.Rotation: Underlying implementation of the
        rotation object
        """

        super().__init__(**kwargs)

        # by default, we will have an extrinsic rotation about [x,y,z] given
        # as [a,b,c] so that it is Rz(c) * Ry(b) * Rx(a)
        self.sequence = sequence or 'xyz'
        if euler is not None \
                and quaternion is None \
                and dcm is None \
                and rotvec is None:
            self.euler = euler
        elif euler is None \
                and quaternion is not None \
                and dcm is None \
                and rotvec is None:
            self.quaternion = quaternion
        elif euler is None \
                and quaternion is None \
                and dcm is not None \
                and rotvec is None:
            self.dcm = dcm
        elif euler is None \
                and quaternion is None \
                and dcm is None \
                and rotvec is not None:
            self.rotvec = rotvec
        else:
            self.quaternion = [0.0, 0.0, 0.0, 1.0]

        self.angular_velocity = angular_velocity \
            if angular_velocity is not None \
            else [0.0, 0.0, 0.0]
        self.angular_acceleration = angular_acceleration \
            if angular_acceleration is not None \
            else [0.0, 0.0, 0.0]

    @staticmethod
    def random(num: int = None):
        if num is None:
            return Angular(quaternion=np_.random.random(4))
        else:
            return (Angular(quaternion=quaternion) for quaternion in
                    np_.random.random((num, 4)))

    @staticmethod
    def rotation_x(angle: Union[Num, Vector], degree: bool = False):
        # always deal with numpy arrays
        angle = np_.asarray(angle)
        if angle.ndim == 0:
            angle = np_.asarray([angle])

        # convert angles given in degree to radian
        if degree:
            angle = np_.deg2rad(angle)

        # if only one angle is given, return the angular object right away
        if angle.size == 1:
            return Angular(sequence='x', euler=angle[0])
        # more than one angle given, so let's return a generator object over
        # each angle
        else:
            # create a generator object
            return (Angular(sequence='x', euler=[a]) for a in angle)

    @staticmethod
    def rotation_y(angle: Union[Num, Vector], degree: bool = False):
        # always deal with numpy arrays
        angle = np_.asarray(angle)
        if angle.ndim == 0:
            angle = np_.asarray([angle])

        # convert angles given in degree to radian
        if degree:
            angle = np_.deg2rad(angle)

        # if only one angle is given, return the angular object right away
        if angle.size == 1:
            return Angular(sequence='y', euler=angle[0])
        # more than one angle given, so let's return a generator object over
        # each angle
        else:
            # create a generator object
            return (Angular(sequence='y', euler=[a]) for a in angle)

    @staticmethod
    def rotation_z(angle: Union[Num, Vector], degree: bool = False):
        # always deal with numpy arrays
        angle = np_.asarray(angle)
        if angle.ndim == 0:
            angle = np_.asarray([angle])

        # convert angles given in degree to radian
        if degree:
            angle = np_.deg2rad(angle)

        # if only one angle is given, return the angular object right away
        if angle.size == 1:
            return Angular(sequence='z', euler=angle[0])
        # more than one angle given, so let's return a generator object over
        # each angle
        else:
            # create a generator object
            return (Angular(sequence='z', euler=[a]) for a in angle)

    def apply(self, coordinates: Union[Vector, Matrix]):
        # deal only with numpy arrays
        coordinates = np_.asarray(coordinates)

        # check if we have a single coordinate
        single = coordinates.ndim == 1

        # ensure coordinates is a 3xM array
        if single:
            coordinates = coordinates[:, np_.newaxis]

        # first, apply the transformation
        transformed = self.dcm.dot(coordinates)

        # return a single transformed coordinate, or all
        return transformed[:, 0] if single else transformed

    @property
    def euler(self):
        """Represent as Euler angles.

        Any orientation can be expressed as a composition of 3 elementary
        rotations. Once the axis sequence has been chosen, Euler angles define
        the angle of rotation around each respective axis [1]_.

        The algorithm from [2]_ has been used to calculate Euler angles for the
        rotation about a given sequence of axes.

        Euler angles suffer from the problem of gimbal lock [3]_, where the
        representation loses a degree of freedom and it is not possible to
        determine the first and third angles uniquely. In this case,
        a warning is raised, and the third angle is set to zero. Note however
        that the returned angles still represent the correct rotation.

        Parameters
        ----------
        seq : string, length 3
            3 characters belonging to the set {'X', 'Y', 'Z'} for intrinsic
            rotations, or {'x', 'y', 'z'} for extrinsic rotations [1]_.
            Adjacent axes cannot be the same.
            Extrinsic and intrinsic rotations cannot be mixed in one function
            call.
        degrees : boolean, optional
            Returned angles are in degrees if this flag is True, else they are
            in radians. Default is False.

        Returns
        -------
        angles : ndarray, shape (3,) or (N, 3)
            Shape depends on shape of inputs used to initialize object.
            The returned angles are in the range:

            - First angle belongs to [-180, 180] degrees (both inclusive)
            - Third angle belongs to [-180, 180] degrees (both inclusive)
            - Second angle belongs to:

                - [-90, 90] degrees if all axes are different (like xyz)
                - [0, 180] degrees if first and third axes are the same
                  (like zxz)

        References
        ----------
        .. [1] https://en.wikipedia.org/wiki/Euler_angles
        #Definition_by_intrinsic_rotations
        .. [2] Malcolm D. Shuster, F. Landis Markley, "General formula for
               extraction the Euler angles", Journal of guidance, control, and
               dynamics, vol. 29.1, pp. 215-221. 2006
        .. [3] https://en.wikipedia.org/wiki/Gimbal_lock#In_applied_mathematics

        Examples
        --------
        >>> from scipy.spatial.transform import Rotation as R

        Represent a single rotation:

        >>> r = R.from_rotvec([0, 0, np_.pi/2])
        >>> r.as_euler('zxy', degrees=True)
        array([90.,  0.,  0.])
        >>> r.as_euler('zxy', degrees=True).shape
        (3,)

        Represent a stack of single rotation:

        >>> r = R.from_rotvec([[0, 0, np_.pi/2]])
        >>> r.as_euler('zxy', degrees=True)
        array([[90.,  0.,  0.]])
        >>> r.as_euler('zxy', degrees=True).shape
        (1, 3)

        Represent multiple rotations in a single object:

        >>> r = R.from_rotvec([
        ... [0, 0, np_.pi/2],
        ... [0, -np_.pi/3, 0],
        ... [np_.pi/4, 0, 0]])
        >>> r.as_euler('zxy', degrees=True)
        array([[ 90.,   0.,   0.],
               [  0.,   0., -60.],
               [  0.,  45.,   0.]])
        >>> r.as_euler('zxy', degrees=True).shape
        (3, 3)

        """
        seq = self.sequence

        if len(seq) != 3:
            raise ValueError(f'Expected 3 axes, got `{seq}` instead.')

        intrinsic = (re.match(r'^[XYZ]{1,3}$', seq) is not None)
        extrinsic = (re.match(r'^[xyz]{1,3}$', seq) is not None)
        if not (intrinsic or extrinsic):
            raise ValueError(
                    f'Expected axes from `seq` to be from [`x`, `y`, `z`] or ['
                    f'`X`, `Y`, `Z`], got `{seq}` instead.')

        if any(seq[i] == seq[i + 1] for i in range(2)):
            raise ValueError(
                    f'Expected consecutive axes to be different, got `{seq}` '
                    f'instead.')

        return self._compute_euler_from_dcm(self.dcm, seq.lower(), extrinsic)

    @euler.setter
    def euler(self, angles: Vector):
        angles = np_.asarray(angles)
        if angles.ndim == 0:
            angles = np_.asarray([angles])

        _validator.linalg.dimensions(angles, 1, 'euler')
        _validator.linalg.shape(angles, (len(self.sequence),), 'euler')

        """Initialize from Euler angles.

        Rotations in 3 dimensions can be represented by a sequece of 3
        rotations around a sequence of axes. In theory, any three axes spanning
        the 3D Euclidean space are enough. In practice the axes of rotation are
        chosen to be the basis vectors.

        The three rotations can either be in a global frame of reference
        (extrinsic) or in a body centred frame of refernce (intrinsic), which
        is attached to, and moves with, the object under rotation [1]_.

        Parameters
        ----------
        seq : string
            Specifies sequence of axes for rotations. Up to 3 characters
            belonging to the set {'X', 'Y', 'Z'} for intrinsic rotations, or
            {'x', 'y', 'z'} for extrinsic rotations. Extrinsic and intrinsic
            rotations cannot be mixed in one function call.
        angles : float or array_like, shape (N,) or (N, [1 or 2 or 3])
            Euler angles specified in radians (`degrees` is False) or degrees
            (`degrees` is True).
            For a single character `seq`, `angles` can be:

            - a single value
            - array_like with shape (N,), where each `angle[i]`
              corresponds to a single rotation
            - array_like with shape (N, 1), where each `angle[i, 0]`
              corresponds to a single rotation

            For 2- and 3-character wide `seq`, `angles` can be:

            - array_like with shape (W,) where `W` is the width of
              `seq`, which corresponds to a single rotation with `W` axes
            - array_like with shape (N, W) where each `angle[i]`
              corresponds to a sequence of Euler angles describing a single
              rotation

        degrees : bool, optional
            If True, then the given angles are assumed to be in degrees.
            Default is False.

        Returns
        -------
        rotation : `Rotation` instance
            Object containing the rotation represented by the sequence of
            rotations around given axes with given angles.

        References
        ----------
        .. [1] https://en.wikipedia.org/wiki/Euler_angles
        #Definition_by_intrinsic_rotations

        Examples
        --------
        >>> from scipy.spatial.transform import Rotation as R

        Initialize a single rotation along a single axis:

        >>> r = R.from_euler('x', 90, degrees=True)
        >>> r.as_quat().shape
        (4,)

        Initialize a single rotation with a given axis sequence:

        >>> r = R.from_euler('zyx', [90, 45, 30], degrees=True)
        >>> r.as_quat().shape
        (4,)

        Initialize a stack with a single rotation around a single axis:

        >>> r = R.from_euler('x', [90], degrees=True)
        >>> r.as_quat().shape
        (1, 4)

        Initialize a stack with a single rotation with an axis sequence:

        >>> r = R.from_euler('zyx', [[90, 45, 30]], degrees=True)
        >>> r.as_quat().shape
        (1, 4)

        Initialize multiple elementary rotations in one object:

        >>> r = R.from_euler('x', [90, 45, 30], degrees=True)
        >>> r.as_quat().shape
        (3, 4)

        Initialize multiple rotations in one object:

        >>> r = R.from_euler('zyx', [[90, 45, 30], [35, 45, 90]], degrees=True)
        >>> r.as_quat().shape
        (2, 4)

        """
        # get configured sequence
        seq = self.sequence

        # how many rotations are needed?
        num_axes = len(seq)

        # ensure we have between 1 and 3 axes to deal with
        if num_axes < 1 or num_axes > 3:
            raise ValueError(
                    f'Expected axis specification to be a non-empty string of '
                    f'up to 3 characters, got `{seq}` instead')

        # figure out if user requested intrinsic or extrinsic orientation
        intrinsic = (re.match(r'^[XYZ]{1,3}$', seq) is not None)
        extrinsic = (re.match(r'^[xyz]{1,3}$', seq) is not None)
        if not (intrinsic or extrinsic):
            raise ValueError(
                    f'Expected axes from `seq` to be from [`x`, `y`, `z`] or ['
                    f'`X`, `Y`, `Z`], got `{seq}` instead.')

        if any(seq[i] == seq[i + 1] for i in range(num_axes - 1)):
            raise ValueError(
                    f'Expected consecutive axes to be different, got `{seq}` '
                    f'instead.')

        # and store the quaternion inside
        self._quaternion = self._elementary_quat_compose(seq.lower(), angles,
                                                         intrinsic)

    @euler.deleter
    def euler(self):
        del self.quaternion

    @property
    def dcm(self):
        # unpack quaternion
        x, y, z, w = self.quaternion

        # pre-calculate some squares
        x2 = x * x
        y2 = y * y
        z2 = z * z
        w2 = w * w

        # and pre-calculate some cross-product valued
        xy = x * y
        zw = z * w
        xz = x * z
        yw = y * w
        yz = y * z
        xw = x * w

        return np_.asarray((
                (
                        x2 - y2 - z2 + w2,
                        2 * (xy - zw),
                        2 * (xz + yw),
                ), (
                        2 * (xy + zw),
                        - x2 + y2 - z2 + w2,
                        2 * (yz - xw)
                ), (
                        2 * (xz - yw),
                        2 * (yz + xw),
                        - x2 - y2 + z2 + w2
                )
        ))

    @dcm.setter
    def dcm(self, dcm: Matrix):
        dcm = np_.asarray(dcm)

        _validator.linalg.rotation_matrix(dcm, 'dcm')

        decision_matrix = np_.empty((4,))
        decision_matrix[:3] = dcm.diagonal(axis1=0, axis2=1)
        decision_matrix[-1] = decision_matrix[:3].sum(axis=0)
        choices = decision_matrix.argmax(axis=0)

        quat = np_.empty((4,))

        if choices != 3:
            i = choices
            j = (i + 1) % 3
            k = (j + 1) % 3

            quat[i] = 1 - decision_matrix[-1] + 2 * dcm[i, i]
            quat[j] = dcm[j, i] + dcm[i, j]
            quat[k] = dcm[k, i] + dcm[i, k]
            quat[3] = dcm[k, j] - dcm[j, k]
        else:
            quat[0] = dcm[2, 1] - dcm[1, 2]
            quat[1] = dcm[0, 2] - dcm[2, 0]
            quat[2] = dcm[1, 0] - dcm[0, 1]
            quat[3] = 1 + decision_matrix[-1]

        self.quaternion = quat / np_.linalg.norm(quat)

    @dcm.deleter
    def dcm(self):
        del self.quaternion

    @property
    def quaternion(self):
        return self._quaternion

    @quaternion.setter
    def quaternion(self, quaternion: Vector):
        quaternion = np_.asarray(quaternion)

        _validator.linalg.dimensions(quaternion, 1, 'quaternion')
        _validator.linalg.shape(quaternion, (4,), 'quaternion')

        # store a normalized value of the quaternion
        self._quaternion = quaternion / np_.linalg.norm(quaternion)

    @quaternion.deleter
    def quaternion(self):
        del self._quaternion

    @property
    def rotvec(self):
        quat = self.quaternion.copy()
        # w > 0 to ensure 0 <= angle <= pi
        quat[quat[3] < 0] *= -1

        angle = 2 * np_.arctan2(np_.linalg.norm(quat[:3]), quat[3])

        if angle <= 1e-3:
            return (2 + angle ** 2 / 12 + 7 * angle ** 4 / 2880) * quat[:3]
        else:
            return (angle / np_.sin(angle / 2)) * quat[:3]

    @rotvec.setter
    def rotvec(self, rotvec: Vector):
        rotvec = np_.asarray(rotvec)

        _validator.linalg.dimensions(rotvec, 1, 'rotvec')
        _validator.linalg.shape(rotvec, (3,), 'rotvec')

        norm = np_.linalg.norm(rotvec)
        if norm <= 1e-3:
            scale = (0.5 - norm ** 2 / 48 + norm ** 4 / 3840)
        else:
            scale = (np_.sin(norm / 2) / norm)

        self.quaternion = np_.hstack((scale * rotvec, np_.cos(norm / 2)))

    @rotvec.deleter
    def rotvec(self):
        del self.quaternion

    @property
    def angular_velocity(self):
        return self._angular_velocity

    @angular_velocity.setter
    def angular_velocity(self, velocity: Vector):
        velocity = np_.asarray(velocity)

        _validator.linalg.space_coordinate(velocity, 'angular_velocity')

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

        _validator.linalg.space_coordinate(acceleration, 'angular_acceleration')

        self._angular_acceleration = acceleration

    @angular_acceleration.deleter
    def angular_acceleration(self):
        del self._angular_acceleration

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            raise TypeError()

        if self is other:
            return True

        return np_.allclose(self.quaternion, other.quaternion) \
               and np_.allclose(self.angular_velocity, other.angular_velocity) \
               and np_.allclose(self.angular_acceleration,
                                other.angular_acceleration)

    def __ne__(self, other):
        return not self == other

    def __lt__(self, other):
        if not isinstance(other, self.__class__):
            raise TypeError()

        if self is other:
            return False

        return (self.euler < other.euler).any() \
               or (self.angular_velocity < other.angular_velocity).any() \
               or (self.angular_acceleration < other.angular_acceleration).any()

    def __le__(self, other):
        if not isinstance(other, self.__class__):
            raise TypeError()

        if self is other:
            return True

        return (self.euler <= other.euler).any() \
               or (self.angular_velocity <= other.angular_velocity).any() \
               or (
                       self.angular_acceleration <=
                       other.angular_acceleration).any()

    def __gt__(self, other):
        if not isinstance(other, self.__class__):
            raise TypeError()

        if self is other:
            return False

        return (self.euler > other.euler).any() \
               or (self.angular_velocity > other.angular_velocity).any() \
               or (self.angular_acceleration > other.angular_acceleration).any()

    def __ge__(self, other):
        if not isinstance(other, self.__class__):
            raise TypeError()

        if self is other:
            return True

        return (self.euler >= other.euler).any() \
               or (self.angular_velocity >= other.angular_velocity).any() \
               or (
                       self.angular_acceleration >=
                       other.angular_acceleration).any()

    def __hash__(self):
        return hash((id(self.angular_acceleration),
                     id(self.angular_velocity),
                     id(self.quaternion)))

    def _elementary_basis_vector(self, axis):
        b = np_.zeros(3)
        b[self._AXIS_TO_IND[axis]] = 1
        return b

    def _compute_euler_from_dcm(self, dcm, seq, extrinsic=False):
        # The algorithm assumes intrinsic frame transformations. For
        # representation
        # the paper uses transformation matrices, which are transpose of the
        # direction cosine matrices used by our Rotation class.
        # Adapt the algorithm for our case by
        # 1. Instead of transposing our representation, use the transpose of the
        #    O matrix as defined in the paper, and be careful to swap indices
        # 2. Reversing both axis sequence and angles for extrinsic rotations

        if extrinsic:
            seq = seq[::-1]

        if dcm.ndim == 2:
            dcm = dcm[None, :, :]
        num_rotations = dcm.shape[0]

        # Step 0
        # Algorithm assumes axes as column vectors, here we use 1D vectors
        n1 = self._elementary_basis_vector(seq[0])
        n2 = self._elementary_basis_vector(seq[1])
        n3 = self._elementary_basis_vector(seq[2])

        # Step 2
        sl = np_.dot(np_.cross(n1, n2), n3)
        cl = np_.dot(n1, n3)

        # angle offset is lambda from the paper referenced in [2] from
        # docstring of
        # `as_euler` function
        offset = np_.arctan2(sl, cl)
        c = np_.vstack((n2, np_.cross(n1, n2), n1))

        # Step 3
        rot = np_.array([
                [1, 0, 0],
                [0, cl, sl],
                [0, -sl, cl],
        ])
        res = np_.einsum('...ij,...jk->...ik', c, dcm)
        dcm_transformed = np_.einsum('...ij,...jk->...ik', res, c.T.dot(rot))

        # Step 4
        angles = np_.empty((num_rotations, 3))
        # Ensure less than unit norm
        positive_unity = dcm_transformed[:, 2, 2] > 1
        negative_unity = dcm_transformed[:, 2, 2] < -1
        dcm_transformed[positive_unity, 2, 2] = 1
        dcm_transformed[negative_unity, 2, 2] = -1
        angles[:, 1] = np_.arccos(dcm_transformed[:, 2, 2])

        # Steps 5, 6
        eps = 1e-7
        safe1 = (np_.abs(angles[:, 1]) >= eps)
        safe2 = (np_.abs(angles[:, 1] - np_.pi) >= eps)

        # Step 4 (Completion)
        angles[:, 1] += offset

        # 5b
        safe_mask = np_.logical_and(safe1, safe2)
        angles[safe_mask, 0] = np_.arctan2(dcm_transformed[safe_mask, 0, 2],
                                           -dcm_transformed[safe_mask, 1, 2])
        angles[safe_mask, 2] = np_.arctan2(dcm_transformed[safe_mask, 2, 0],
                                           dcm_transformed[safe_mask, 2, 1])

        if extrinsic:
            # For extrinsic, set first angle to zero so that after reversal we
            # ensure that third angle is zero
            # 6a
            angles[~safe_mask, 0] = 0
            # 6b
            angles[~safe1, 2] = np_.arctan2(
                    dcm_transformed[~safe1, 1, 0] - dcm_transformed[
                        ~safe1, 0, 1],
                    dcm_transformed[~safe1, 0, 0] + dcm_transformed[
                        ~safe1, 1, 1]
            )
            # 6c
            angles[~safe2, 2] = -np_.arctan2(
                    dcm_transformed[~safe2, 1, 0] + dcm_transformed[
                        ~safe2, 0, 1],
                    dcm_transformed[~safe2, 0, 0] - dcm_transformed[
                        ~safe2, 1, 1]
            )
        else:
            # For instrinsic, set third angle to zero
            # 6a
            angles[~safe_mask, 2] = 0
            # 6b
            angles[~safe1, 0] = np_.arctan2(
                    dcm_transformed[~safe1, 1, 0] - dcm_transformed[
                        ~safe1, 0, 1],
                    dcm_transformed[~safe1, 0, 0] + dcm_transformed[
                        ~safe1, 1, 1]
            )
            # 6c
            angles[~safe2, 0] = np_.arctan2(
                    dcm_transformed[~safe2, 1, 0] + dcm_transformed[
                        ~safe2, 0, 1],
                    dcm_transformed[~safe2, 0, 0] - dcm_transformed[
                        ~safe2, 1, 1]
            )

        # Step 7
        if seq[0] == seq[2]:
            # lambda = 0, so we can only ensure angle2 -> [0, pi]
            adjust_mask = np_.logical_or(angles[:, 1] < 0,
                                         angles[:, 1] > np_.pi)
        else:
            # lambda = + or - pi/2, so we can ensure angle2 -> [-pi/2, pi/2]
            adjust_mask = np_.logical_or(angles[:, 1] < -np_.pi / 2,
                                         angles[:, 1] > np_.pi / 2)

        # Dont adjust gimbal locked angle sequences
        adjust_mask = np_.logical_and(adjust_mask, safe_mask)

        angles[adjust_mask, 0] += np_.pi
        angles[adjust_mask, 1] = 2 * offset - angles[adjust_mask, 1]
        angles[adjust_mask, 2] -= np_.pi

        angles[angles < -np_.pi] += 2 * np_.pi
        angles[angles > np_.pi] -= 2 * np_.pi

        # Step 8
        if not np_.all(safe_mask):
            raise RuntimeWarning(
                    'Gimbal lock detected. Setting third angle to zero since '
                    'it '
                    'is not possible to uniquely determine all angles.')

        # Reverse role of extrinsic and intrinsic rotations, but let third
        # angle be
        # zero for gimbal locked cases
        if extrinsic:
            angles = angles[:, ::-1]

        return angles[0] if num_rotations == 1 else angles

    def _make_elementary_quat(self, axis, angles):
        quat = np_.zeros((4,))

        quat[3] = np_.cos(angles / 2)
        quat[self._AXIS_TO_IND[axis]] = np_.sin(angles / 2)
        return quat

    def _compose_quat(self, p, q):
        product = np_.empty((4,))
        product[3] = p[3] * q[3] - p[:3].dot(q[:3])
        product[:3] = (p[3] * q[:3] + q[3] * p[:3] +
                       np_.cross(p[:3], q[:3]))
        return product

    def _elementary_quat_compose(self, seq, angles, intrinsic=False):
        result = self._make_elementary_quat(seq[0], angles[0])

        for idx, axis in enumerate(seq[1:], start=1):
            if intrinsic:
                result = self._compose_quat(
                        result,
                        self._make_elementary_quat(axis, angles[idx]))
            else:
                result = self._compose_quat(
                        self._make_elementary_quat(axis, angles[idx]),
                        result)
        return result

    __repr__ = make_repr(
            'dcm',
            'angular_velocity',
            'angular_acceleration',
            'sequence'
    )


__all__ = [
        'Angular',
]

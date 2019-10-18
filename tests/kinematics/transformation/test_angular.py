from typing import Sequence, AnyStr

import numpy as np
import scipy.linalg
from pytest import approx, mark
from scipy.spatial.transform import Rotation

import cdpyr


class AngularTransformationTestSuite(object):

    def test_empty_object(self):
        angular = cdpyr.kinematics.transformation.Angular()

        assert isinstance(angular, cdpyr.kinematics.transformation.Angular)

        assert angular.euler.shape == (3,)
        assert angular.euler == approx([0., 0., 0.])
        assert angular.angular_velocity.shape == (3,)
        assert angular.angular_velocity == approx([0., 0., 0.])
        assert angular.angular_acceleration.shape == (3,)
        assert angular.angular_acceleration == approx([0., 0., 0.])

    @mark.parametrize(
        ("eul", "seq"),
        [
            (np.random.random((3,)).tolist(), 'xyz'),  # 3-tuple
            (np.random.random((3,)).tolist(), 'zyx'),  # 3-tuple
            (np.random.random((3,)).tolist(), 'yzx'),  # 3-tuple
            (np.random.random((3,)).tolist(), 'xzy'),  # 3-tuple
            (np.random.random((3,)).tolist(), 'zxy'),  # 3-tuple
            (np.random.random((3,)).tolist(), 'yxz'),  # 3-tuple
            (np.random.random((3,)).tolist(), 'xyx'),  # 3-tuple
            (np.random.random((3,)).tolist(), 'yxy'),  # 3-tuple
            (np.random.random((3,)).tolist(), 'xzx'),  # 3-tuple
            (np.random.random((3,)).tolist(), 'zxz'),  # 3-tuple
            (np.random.random((3,)).tolist(), 'yzy'),  # 3-tuple
            (np.random.random((3,)).tolist(), 'zyz'),  # 3-tuple
            (np.random.random((3,)).tolist(), 'XYZ'),  # 3-tuple
            (np.random.random((3,)).tolist(), 'ZYX'),  # 3-tuple
            (np.random.random((3,)).tolist(), 'YZX'),  # 3-tuple
            (np.random.random((3,)).tolist(), 'XZY'),  # 3-tuple
            (np.random.random((3,)).tolist(), 'ZXY'),  # 3-tuple
            (np.random.random((3,)).tolist(), 'YXZ'),  # 3-tuple
            (np.random.random((3,)).tolist(), 'XYX'),  # 3-tuple
            (np.random.random((3,)).tolist(), 'YXY'),  # 3-tuple
            (np.random.random((3,)).tolist(), 'XZX'),  # 3-tuple
            (np.random.random((3,)).tolist(), 'ZXZ'),  # 3-tuple
            (np.random.random((3,)).tolist(), 'YZY'),  # 3-tuple
            (np.random.random((3,)).tolist(), 'ZYZ'),  # 3-tuple
        ]
    )
    def test_with_euler_from_list_as_keyword_argument(self, eul: Sequence,
                                                      seq: AnyStr):
        angular = cdpyr.kinematics.transformation.Angular(
            euler=eul,
            rotation_sequence=seq
        )

        rot: Rotation = Rotation.from_euler(seq, eul)

        assert angular.euler.shape == (len(eul),)
        assert angular.euler == approx(eul)
        assert angular.dcm == approx(rot.as_dcm())
        assert angular.angular_velocity.shape == (3,)
        assert angular.angular_velocity == approx([0., 0., 0.])
        assert angular.angular_acceleration.shape == (3,)
        assert angular.angular_acceleration == approx([0., 0., 0.])

    @mark.parametrize(
        ("eul", "seq"),
        [
            (np.pi * (np.random.random((3,)) - 0.5), 'xyz'),  # 3x1 vector
            (np.pi * (np.random.random((3,)) - 0.5), 'zyx'),  # 3x1 vector
            (np.pi * (np.random.random((3,)) - 0.5), 'yzx'),  # 3x1 vector
            (np.pi * (np.random.random((3,)) - 0.5), 'xzy'),  # 3x1 vector
            (np.pi * (np.random.random((3,)) - 0.5), 'zxy'),  # 3x1 vector
            (np.pi * (np.random.random((3,)) - 0.5), 'yxz'),  # 3x1 vector
            (np.pi * (np.random.random((3,)) - 0.5), 'XYZ'),  # 3x1 vector
            (np.pi * (np.random.random((3,)) - 0.5), 'ZYX'),  # 3x1 vector
            (np.pi * (np.random.random((3,)) - 0.5), 'YZX'),  # 3x1 vector
            (np.pi * (np.random.random((3,)) - 0.5), 'XZY'),  # 3x1 vector
            (np.pi * (np.random.random((3,)) - 0.5), 'ZXY'),  # 3x1 vector
            (np.pi * (np.random.random((3,)) - 0.5), 'YXZ'),  # 3x1 vector
        ]
    )
    def test_with_euler_from_numpyarray_as_keyword_argument(self,
                                                            eul: np.ndarray,
                                                            seq: AnyStr):
        angular = cdpyr.kinematics.transformation.Angular(
            euler=eul,
            rotation_sequence=seq
        )

        rot: Rotation = Rotation.from_euler(seq, eul)

        assert angular.euler.shape == eul.shape
        assert angular.euler == approx(eul)
        assert angular.dcm == approx(rot.as_dcm())
        assert angular.angular_velocity.shape == (3,)
        assert angular.angular_velocity == approx([0., 0., 0.])
        assert angular.angular_acceleration.shape == (3,)
        assert angular.angular_acceleration == approx([0., 0., 0.])

    @mark.parametrize(
        "quat",
        [
            ((np.random.random((4,)) - 0.5).tolist()),  # 4-tuple
            ((np.random.random((4,)) - 0.5).tolist()),  # 4-tuple
            ((np.random.random((4,)) - 0.5).tolist()),  # 4-tuple
            ((np.random.random((4,)) - 0.5).tolist()),  # 4-tuple
            ((np.random.random((4,)) - 0.5).tolist()),  # 4-tuple
            ((np.random.random((4,)) - 0.5).tolist()),  # 4-tuple
            ((np.random.random((4,)) - 0.5).tolist()),  # 4-tuple
            ((np.random.random((4,)) - 0.5).tolist()),  # 4-tuple
            ((np.random.random((4,)) - 0.5).tolist()),  # 4-tuple
            ((np.random.random((4,)) - 0.5).tolist()),  # 4-tuple
            ((np.random.random((4,)) - 0.5).tolist()),  # 4-tuple
            ((np.random.random((4,)) - 0.5).tolist()),  # 4-tuple
        ]
    )
    def test_with_quaternion_from_list_as_keyword_argument(self,
                                                           quat: Sequence):
        angular = cdpyr.kinematics.transformation.Angular(
            quaternion=quat
        )

        rot: Rotation = Rotation.from_quat(quat)
        quat = np.asarray(quat)

        assert angular.quaternion.shape == quat.shape
        assert angular.quaternion == approx(quat / scipy.linalg.norm(quat))
        assert angular.dcm == approx(rot.as_dcm())
        assert angular.angular_velocity.shape == (3,)
        assert angular.angular_velocity == approx([0., 0., 0.])
        assert angular.angular_acceleration.shape == (3,)
        assert angular.angular_acceleration == approx([0., 0., 0.])

    @mark.parametrize(
        "quat",
        [
            (np.random.random((4,)) - 0.5),  # 4x1 vector
            (np.random.random((4,)) - 0.5),  # 4x1 vector
            (np.random.random((4,)) - 0.5),  # 4x1 vector
            (np.random.random((4,)) - 0.5),  # 4x1 vector
            (np.random.random((4,)) - 0.5),  # 4x1 vector
            (np.random.random((4,)) - 0.5),  # 4x1 vector
            (np.random.random((4,)) - 0.5),  # 4x1 vector
            (np.random.random((4,)) - 0.5),  # 4x1 vector
            (np.random.random((4,)) - 0.5),  # 4x1 vector
            (np.random.random((4,)) - 0.5),  # 4x1 vector
            (np.random.random((4,)) - 0.5),  # 4x1 vector
            (np.random.random((4,)) - 0.5),  # 4x1 vector
        ]
    )
    def test_with_quaternion_from_numpyarray_as_keyword_argument(self,
                                                                 quat:
                                                                 np.ndarray):
        angular = cdpyr.kinematics.transformation.Angular(
            quaternion=quat
        )

        rot: Rotation = Rotation.from_quat(quat)

        assert angular.quaternion.shape == quat.shape
        assert angular.quaternion == approx(quat / scipy.linalg.norm(quat))
        assert angular.dcm == approx(rot.as_dcm())
        assert angular.angular_velocity.shape == (3,)
        assert angular.angular_velocity == approx([0., 0., 0.])
        assert angular.angular_acceleration.shape == (3,)
        assert angular.angular_acceleration == approx([0., 0., 0.])

    @mark.parametrize(
        "rotvec",
        [
            ((np.random.random((3,)) - 0.5).tolist()),  # 4-tuple
            ((np.random.random((3,)) - 0.5).tolist()),  # 4-tuple
            ((np.random.random((3,)) - 0.5).tolist()),  # 4-tuple
            ((np.random.random((3,)) - 0.5).tolist()),  # 4-tuple
            ((np.random.random((3,)) - 0.5).tolist()),  # 4-tuple
            ((np.random.random((3,)) - 0.5).tolist()),  # 4-tuple
            ((np.random.random((3,)) - 0.5).tolist()),  # 4-tuple
            ((np.random.random((3,)) - 0.5).tolist()),  # 4-tuple
            ((np.random.random((3,)) - 0.5).tolist()),  # 4-tuple
            ((np.random.random((3,)) - 0.5).tolist()),  # 4-tuple
            ((np.random.random((3,)) - 0.5).tolist()),  # 4-tuple
            ((np.random.random((3,)) - 0.5).tolist()),  # 4-tuple
        ]
    )
    def test_with_rotationvector_from_list_as_keyword_argument(self,
                                                               rotvec:
                                                               Sequence):
        angular = cdpyr.kinematics.transformation.Angular(
            rotvec=rotvec
        )

        rot: Rotation = Rotation.from_rotvec(rotvec)

        rotvec = np.asarray(rotvec)

        assert angular.rotvec.shape == rotvec.shape
        assert angular.rotvec == approx(rotvec)
        assert angular.dcm == approx(rot.as_dcm())
        assert angular.angular_velocity.shape == (3,)
        assert angular.angular_velocity == approx([0., 0., 0.])
        assert angular.angular_acceleration.shape == (3,)
        assert angular.angular_acceleration == approx([0., 0., 0.])

    @mark.parametrize(
        "rotvec",
        [
            (np.random.random((3,)) - 0.5),  # 4x1 vector
            (np.random.random((3,)) - 0.5),  # 4x1 vector
            (np.random.random((3,)) - 0.5),  # 4x1 vector
            (np.random.random((3,)) - 0.5),  # 4x1 vector
            (np.random.random((3,)) - 0.5),  # 4x1 vector
            (np.random.random((3,)) - 0.5),  # 4x1 vector
            (np.random.random((3,)) - 0.5),  # 4x1 vector
            (np.random.random((3,)) - 0.5),  # 4x1 vector
            (np.random.random((3,)) - 0.5),  # 4x1 vector
            (np.random.random((3,)) - 0.5),  # 4x1 vector
            (np.random.random((3,)) - 0.5),  # 4x1 vector
            (np.random.random((3,)) - 0.5),  # 4x1 vector
        ]
    )
    def test_with_rotationvector_from_numpyarray_as_keyword_argument(self,
                                                                     rotvec:
                                                                     np.ndarray):
        angular = cdpyr.kinematics.transformation.Angular(
            rotvec=rotvec
        )

        rot: Rotation = Rotation.from_rotvec(rotvec)

        assert angular.rotvec.shape == rotvec.shape
        assert angular.rotvec == approx(rotvec)
        assert angular.dcm == approx(rot.as_dcm())
        assert angular.angular_velocity.shape == (3,)
        assert angular.angular_velocity == approx([0., 0., 0.])
        assert angular.angular_acceleration.shape == (3,)
        assert angular.angular_acceleration == approx([0., 0., 0.])

    @mark.parametrize(
        "dcm",
        [
            (Rotation.random().as_dcm().tolist()),
        ]
    )
    def test_with_dcm_from_list_as_keyword_argument(self,
                                                    dcm:
                                                    Sequence[Sequence]):
        angular = cdpyr.kinematics.transformation.Angular(
            dcm=dcm
        )

        dcm = np.asarray(dcm)

        assert angular.dcm.shape == dcm.shape
        assert angular.dcm == approx(dcm)
        assert angular.angular_velocity.shape == (3,)
        assert angular.angular_velocity == approx([0., 0., 0.])
        assert angular.angular_acceleration.shape == (3,)
        assert angular.angular_acceleration == approx([0., 0., 0.])

    @mark.parametrize(
        "dcm",
        [
            (Rotation.random().as_dcm()),
        ]
    )
    def test_with_dcm_from_numpyarray_as_keyword_argument(self,
                                                          dcm:
                                                          np.ndarray):
        angular = cdpyr.kinematics.transformation.Angular(
            dcm=dcm
        )

        assert angular.dcm.shape == dcm.shape
        assert angular.dcm == approx(dcm)
        assert angular.angular_velocity.shape == (3,)
        assert angular.angular_velocity == approx([0., 0., 0.])
        assert angular.angular_acceleration.shape == (3,)
        assert angular.angular_acceleration == approx([0., 0., 0.])

    @mark.parametrize(
        "vel",
        [
            (np.random.random((3,)).tolist()),  # 3x1 vector
        ]
    )
    def test_with_velocity_from_list_as_keyword_argument(self, vel: Sequence):
        angular = cdpyr.kinematics.transformation.Angular(
            angular_velocity=vel
        )

        assert angular.quaternion.shape == (4,)
        assert angular.quaternion == approx([0., 0., 0., 1.])
        assert angular.angular_velocity.shape == (len(vel),)
        assert angular.angular_velocity == approx(vel)
        assert angular.angular_acceleration.shape == (3,)
        assert angular.angular_acceleration == approx([0., 0., 0.])

    @mark.parametrize(
        "vel",
        [
            (np.random.random((3,))),  # 3x1 vector
        ]
    )
    def test_with_velocity_from_numpyarray_as_keyword_argument(self,
                                                               vel: np.ndarray):
        angular = cdpyr.kinematics.transformation.Angular(
            angular_velocity=vel
        )

        assert angular.quaternion.shape == (4,)
        assert angular.quaternion == approx([0., 0., 0., 1.])
        assert angular.angular_velocity.shape == vel.shape
        assert angular.angular_velocity == approx(vel)
        assert angular.angular_acceleration.shape == (3,)
        assert angular.angular_acceleration == approx([0., 0., 0.])

    @mark.parametrize(
        "acc",
        [
            (np.random.random((3,)).tolist()),  # 3x1 vector
        ]
    )
    def test_with_acceleration_from_list_as_keyword_argument(self,
                                                             acc: Sequence):
        angular = cdpyr.kinematics.transformation.Angular(
            angular_acceleration=acc
        )

        assert angular.quaternion.shape == (4,)
        assert angular.quaternion == approx([0., 0., 0., 1.])
        assert angular.angular_velocity.shape == (3,)
        assert angular.angular_velocity == approx([0., 0., 0.])
        assert angular.angular_acceleration.shape == (len(acc),)
        assert angular.angular_acceleration == approx(acc)

    @mark.parametrize(
        "acc",
        [
            (np.random.random((3,))),  # 3x1 vector
        ]
    )
    def test_with_acceleration_from_numpyarray_as_keyword_argument(self,
                                                                   acc:
                                                                   np.ndarray):
        angular = cdpyr.kinematics.transformation.Angular(
            angular_acceleration=acc
        )

        assert angular.quaternion.shape == (4,)
        assert angular.quaternion == approx([0., 0., 0., 1.])
        assert angular.angular_velocity.shape == (3,)
        assert angular.angular_velocity == approx([0., 0., 0.])
        assert angular.angular_acceleration.shape == acc.shape
        assert angular.angular_acceleration == approx(acc)

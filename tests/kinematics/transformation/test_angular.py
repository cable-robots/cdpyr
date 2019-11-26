from typing import (
    AnyStr,
    Sequence
)
import itertools

import numpy as np
import pytest
import scipy.linalg
from scipy.spatial.transform import Rotation

from cdpyr.kinematics.transformation import Angular


class AngularTransformationTestSuite(object):

    def test_empty_object(self):
        angular = Angular()

        assert isinstance(angular, Angular)

        assert angular.euler.shape == (3,)
        assert angular.euler == pytest.approx([0., 0., 0.])
        assert angular.angular_velocity.shape == (3,)
        assert angular.angular_velocity == pytest.approx([0., 0., 0.])
        assert angular.angular_acceleration.shape == (3,)
        assert angular.angular_acceleration == pytest.approx([0., 0., 0.])

    @pytest.mark.parametrize(
        ("eul", "seq"),
        [
            (np.pi * (np.random.random((3,)) - 0.5), ''.join(seq)) for seq in
            itertools.chain(itertools.permutations(('x', 'y', 'z'), 3),
                            itertools.permutations(('X', 'Y', 'Z'), 3))
        ]
    )
    def test_with_euler_from_list_as_keyword_argument(self, eul: Sequence,
                                                      seq: AnyStr):
        angular = Angular(
            sequence=seq,
            euler=eul
        )

        rot: Rotation = Rotation.from_euler(seq, eul)

        assert angular.euler.shape == (len(eul),)
        assert angular.euler == pytest.approx(eul)
        assert angular.dcm == pytest.approx(rot.as_dcm())
        assert angular.angular_velocity.shape == (3,)
        assert angular.angular_velocity == pytest.approx([0., 0., 0.])
        assert angular.angular_acceleration.shape == (3,)
        assert angular.angular_acceleration == pytest.approx([0., 0., 0.])

    @pytest.mark.parametrize(
        ("eul", "seq"),
        [
            (np.pi * (np.random.random((3,)) - 0.5), ''.join(seq)) for seq in
            itertools.chain(itertools.permutations(('x', 'y', 'z'), 3),
                            itertools.permutations(('X', 'Y', 'Z'), 3))
        ]
    )
    def test_with_euler_from_numpyarray_as_keyword_argument(self,
                                                            eul: np.ndarray,
                                                            seq: AnyStr):
        angular = Angular(
            sequence=seq,
            euler=eul
        )

        rot: Rotation = Rotation.from_euler(seq, eul)

        assert angular.euler.shape == eul.shape
        assert angular.euler == pytest.approx(eul)
        assert angular.dcm == pytest.approx(rot.as_dcm())
        assert angular.angular_velocity.shape == (3,)
        assert angular.angular_velocity == pytest.approx([0., 0., 0.])
        assert angular.angular_acceleration.shape == (3,)
        assert angular.angular_acceleration == pytest.approx([0., 0., 0.])

    @pytest.mark.parametrize(
        "quat",
        [quat.tolist() for quat in Rotation.random(25).as_quat()]
    )
    def test_with_quaternion_from_list_as_keyword_argument(self,
                                                           quat: Sequence):
        angular = Angular(
            quaternion=quat
        )

        rot: Rotation = Rotation.from_quat(quat)
        quat = np.asarray(quat)

        assert angular.quaternion.shape == quat.shape
        assert angular.quaternion == pytest.approx(
            quat / scipy.linalg.norm(quat))
        assert angular.dcm == pytest.approx(rot.as_dcm())
        assert angular.angular_velocity.shape == (3,)
        assert angular.angular_velocity == pytest.approx([0., 0., 0.])
        assert angular.angular_acceleration.shape == (3,)
        assert angular.angular_acceleration == pytest.approx([0., 0., 0.])

    @pytest.mark.parametrize(
        "quat",
        [quat for quat in Rotation.random(25).as_quat()]
    )
    def test_with_quaternion_from_numpyarray_as_keyword_argument(self,
                                                                 quat:
                                                                 np.ndarray):
        angular = Angular(
            quaternion=quat
        )

        rot: Rotation = Rotation.from_quat(quat)

        assert angular.quaternion.shape == quat.shape
        assert angular.quaternion == pytest.approx(
            quat / scipy.linalg.norm(quat))
        assert angular.dcm == pytest.approx(rot.as_dcm())
        assert angular.angular_velocity.shape == (3,)
        assert angular.angular_velocity == pytest.approx([0., 0., 0.])
        assert angular.angular_acceleration.shape == (3,)
        assert angular.angular_acceleration == pytest.approx([0., 0., 0.])

    @pytest.mark.parametrize(
        "rotvec",
        [rotvec.tolist() for rotvec in Rotation.random(25).as_rotvec()]
    )
    def test_with_rotationvector_from_list_as_keyword_argument(self,
                                                               rotvec:
                                                               Sequence):
        angular = Angular(
            rotvec=rotvec
        )

        rot: Rotation = Rotation.from_rotvec(rotvec)

        rotvec = np.asarray(rotvec)

        assert angular.rotvec.shape == rotvec.shape
        assert angular.rotvec == pytest.approx(rotvec)
        assert angular.dcm == pytest.approx(rot.as_dcm())
        assert angular.angular_velocity.shape == (3,)
        assert angular.angular_velocity == pytest.approx([0., 0., 0.])
        assert angular.angular_acceleration.shape == (3,)
        assert angular.angular_acceleration == pytest.approx([0., 0., 0.])

    @pytest.mark.parametrize(
        "rotvec",
        [rotvec for rotvec in Rotation.random(25).as_rotvec()]
    )
    def test_with_rotationvector_from_numpyarray_as_keyword_argument(self,
                                                                     rotvec:
                                                                     np.ndarray):
        angular = Angular(
            rotvec=rotvec
        )

        rot: Rotation = Rotation.from_rotvec(rotvec)

        assert angular.rotvec.shape == rotvec.shape
        assert angular.rotvec == pytest.approx(rotvec)
        assert angular.dcm == pytest.approx(rot.as_dcm())
        assert angular.angular_velocity.shape == (3,)
        assert angular.angular_velocity == pytest.approx([0., 0., 0.])
        assert angular.angular_acceleration.shape == (3,)
        assert angular.angular_acceleration == pytest.approx([0., 0., 0.])

    @pytest.mark.parametrize(
        "dcm",
        [dcm for dcm in Rotation.random(25).as_dcm()]
    )
    def test_with_dcm_from_list_as_keyword_argument(self,
                                                    dcm:
                                                    Sequence[Sequence]):
        angular = Angular(
            dcm=dcm
        )

        dcm = np.asarray(dcm)

        assert angular.dcm.shape == dcm.shape
        assert angular.dcm == pytest.approx(dcm)
        assert angular.angular_velocity.shape == (3,)
        assert angular.angular_velocity == pytest.approx([0., 0., 0.])
        assert angular.angular_acceleration.shape == (3,)
        assert angular.angular_acceleration == pytest.approx([0., 0., 0.])

    @pytest.mark.parametrize(
        "dcm",
        [dcm for dcm in Rotation.random(25).as_dcm()]
    )
    def test_with_dcm_from_numpyarray_as_keyword_argument(self,
                                                          dcm:
                                                          np.ndarray):
        angular = Angular(
            dcm=dcm
        )

        assert angular.dcm.shape == dcm.shape
        assert angular.dcm == pytest.approx(dcm)
        assert angular.angular_velocity.shape == (3,)
        assert angular.angular_velocity == pytest.approx([0., 0., 0.])
        assert angular.angular_acceleration.shape == (3,)
        assert angular.angular_acceleration == pytest.approx([0., 0., 0.])

    @pytest.mark.parametrize(
        "vel",
        [vel.tolist() for vel in np.random.random((25, 3))]
    )
    def test_with_velocity_from_list_as_keyword_argument(self, vel: Sequence):
        angular = Angular(
            angular_velocity=vel
        )

        assert angular.quaternion.shape == (4,)
        assert angular.quaternion == pytest.approx([0., 0., 0., 1.])
        assert angular.angular_velocity.shape == (len(vel),)
        assert angular.angular_velocity == pytest.approx(vel)
        assert angular.angular_acceleration.shape == (3,)
        assert angular.angular_acceleration == pytest.approx([0., 0., 0.])

    @pytest.mark.parametrize(
        "vel",
        [vel for vel in np.random.random((25, 3))]
    )
    def test_with_velocity_from_numpyarray_as_keyword_argument(self,
                                                               vel: np.ndarray):
        angular = Angular(
            angular_velocity=vel
        )

        assert angular.quaternion.shape == (4,)
        assert angular.quaternion == pytest.approx([0., 0., 0., 1.])
        assert angular.angular_velocity.shape == vel.shape
        assert angular.angular_velocity == pytest.approx(vel)
        assert angular.angular_acceleration.shape == (3,)
        assert angular.angular_acceleration == pytest.approx([0., 0., 0.])

    @pytest.mark.parametrize(
        "acc",
        [acc.tolist() for acc in np.random.random((25, 3))]
    )
    def test_with_acceleration_from_list_as_keyword_argument(self,
                                                             acc: Sequence):
        angular = Angular(
            angular_acceleration=acc
        )

        assert angular.quaternion.shape == (4,)
        assert angular.quaternion == pytest.approx([0., 0., 0., 1.])
        assert angular.angular_velocity.shape == (3,)
        assert angular.angular_velocity == pytest.approx([0., 0., 0.])
        assert angular.angular_acceleration.shape == (len(acc),)
        assert angular.angular_acceleration == pytest.approx(acc)

    @pytest.mark.parametrize(
        "acc",
        [acc for acc in np.random.random((25, 3))]
    )
    def test_with_acceleration_from_numpyarray_as_keyword_argument(self,
                                                                   acc:
                                                                   np.ndarray):
        angular = Angular(
            angular_acceleration=acc
        )

        assert angular.quaternion.shape == (4,)
        assert angular.quaternion == pytest.approx([0., 0., 0., 1.])
        assert angular.angular_velocity.shape == (3,)
        assert angular.angular_velocity == pytest.approx([0., 0., 0.])
        assert angular.angular_acceleration.shape == acc.shape
        assert angular.angular_acceleration == pytest.approx(acc)


if __name__ == "__main__":
    pytest.main()

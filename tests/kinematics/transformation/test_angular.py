import itertools

import numpy as np
import pytest
from scipy.spatial.transform import Rotation

from cdpyr.kinematics.transformation import Angular
from cdpyr.typing import Matrix, Vector


class AngularTransformationTestSuite(object):

    @pytest.mark.parametrize(
            ('dcm', 'ang_vel', 'ang_acc'),
            (
                    itertools.product(
                            (None, np.eye(3)) + tuple(dcm for dcm in
                                                      Rotation.random(
                                                              25).as_dcm()),
                            (None, np.zeros((3,)), np.random.random((3,))),
                            (None, np.zeros((3,)), np.random.random((3,))),
                    )
            )
    )
    def test_init_with_dcm(self, dcm: Matrix, ang_vel: Vector, ang_acc: Vector):
        angular = Angular(dcm, angular_velocity=ang_vel,
                          angular_acceleration=ang_acc)

        dcm = np.asarray(dcm if dcm is not None else np.eye(3))
        ang_vel = np.asarray(
                ang_vel if ang_vel is not None else [0.0, 0.0, 0.0])
        ang_acc = np.asarray(
                ang_acc if ang_acc is not None else [0.0, 0.0, 0.0])

        assert angular.dcm.shape == dcm.shape
        assert angular.angular_velocity.shape == ang_vel.shape
        assert angular.angular_acceleration.shape == ang_acc.shape
        assert angular.dcm == pytest.approx(dcm)
        assert angular.angular_velocity == pytest.approx(ang_vel)
        assert angular.angular_acceleration == pytest.approx(ang_acc)

    @pytest.mark.parametrize(
            ('euler_seq', 'ang_vel', 'ang_acc'),
            (
                    itertools.product(
                            ((np.pi * (np.random.random((3,)) - 0.5),
                              ''.join(seq)) for seq in itertools.chain(
                                    itertools.permutations(('x', 'y', 'z'), 3),
                                    itertools.permutations(('X', 'Y', 'Z'),
                                                           3))),
                            (None, np.zeros((3,)), np.random.random((3,))),
                            (None, np.zeros((3,)), np.random.random((3,))),
                    )
            )
    )
    def test_init_with_euler(self, euler_seq, ang_vel: Vector, ang_acc: Vector):
        euler, seq = euler_seq
        angular = Angular(euler=euler, sequence=seq, angular_velocity=ang_vel,
                          angular_acceleration=ang_acc)

        euler = np.asarray(euler if euler is not None else [0.0, 0.0, 0.0])
        ang_vel = np.asarray(
                ang_vel if ang_vel is not None else [0.0, 0.0, 0.0])
        ang_acc = np.asarray(
                ang_acc if ang_acc is not None else [0.0, 0.0, 0.0])

        dcm = Rotation.from_euler(seq, euler).as_dcm()

        assert angular.dcm.shape == dcm.shape
        assert angular.angular_velocity.shape == ang_vel.shape
        assert angular.angular_acceleration.shape == ang_acc.shape
        assert angular.dcm == pytest.approx(dcm)
        assert angular.euler == pytest.approx(euler)
        assert angular.angular_velocity == pytest.approx(ang_vel)
        assert angular.angular_acceleration == pytest.approx(ang_acc)

    @pytest.mark.parametrize(
            ('quaternion', 'ang_vel', 'ang_acc'),
            (
                    itertools.product(
                            ([0.0, 0.0, 0.0, 1.0], np.random.random((4,))),
                            (None, np.zeros((3,)), np.random.random((3,))),
                            (None, np.zeros((3,)), np.random.random((3,))),
                    )
            )
    )
    def test_init_with_quaternion(self, quaternion: Vector, ang_vel: Vector,
                                  ang_acc: Vector):
        angular = Angular(quaternion=quaternion, angular_velocity=ang_vel,
                          angular_acceleration=ang_acc)

        quaternion = np.asarray(quaternion)
        ang_vel = np.asarray(
                ang_vel if ang_vel is not None else [0.0, 0.0, 0.0])
        ang_acc = np.asarray(
                ang_acc if ang_acc is not None else [0.0, 0.0, 0.0])

        dcm = Rotation.from_quat(quaternion).as_dcm()
        quaternion /= np.linalg.norm(quaternion)

        assert angular.dcm.shape == dcm.shape
        assert angular.angular_velocity.shape == ang_vel.shape
        assert angular.angular_acceleration.shape == ang_acc.shape
        assert angular.dcm == pytest.approx(dcm)
        assert angular.quaternion == pytest.approx(quaternion)
        assert angular.angular_velocity == pytest.approx(ang_vel)
        assert angular.angular_acceleration == pytest.approx(ang_acc)

    @pytest.mark.parametrize(
            ('rotvec', 'ang_vel', 'ang_acc'),
            (
                    itertools.product(
                            np.pi * (np.random.random((10, 3)) - 0.5),
                            (None, np.zeros((3,)), np.random.random((3,))),
                            (None, np.zeros((3,)), np.random.random((3,))),
                    )
            )
    )
    def test_init_with_rotvec(self, rotvec: Vector, ang_vel: Vector,
                              ang_acc: Vector):
        angular = Angular(rotvec=rotvec, angular_velocity=ang_vel,
                          angular_acceleration=ang_acc)

        rotvec = np.asarray(rotvec)
        ang_vel = np.asarray(
                ang_vel if ang_vel is not None else [0.0, 0.0, 0.0])
        ang_acc = np.asarray(
                ang_acc if ang_acc is not None else [0.0, 0.0, 0.0])

        dcm = Rotation.from_rotvec(rotvec).as_dcm()

        assert angular.dcm.shape == dcm.shape
        assert angular.angular_velocity.shape == ang_vel.shape
        assert angular.angular_acceleration.shape == ang_acc.shape
        assert angular.dcm == pytest.approx(dcm)
        assert angular.rotvec == pytest.approx(rotvec)
        assert angular.angular_velocity == pytest.approx(ang_vel)
        assert angular.angular_acceleration == pytest.approx(ang_acc)

    @pytest.mark.parametrize(
            ('dcm', 'coordinate'),
            (
                    itertools.product(
                            (None, np.eye(3)) + tuple(dcm for dcm in
                                                      Rotation.random(
                                                              25).as_dcm()),
                            (np.zeros((3,)), np.random.random((3,)),
                             np.random.random((3, 5))),
                    )
            )
    )
    def test_apply_transformation(self, dcm: Matrix, coordinate: Vector):
        angular = Angular(dcm)

        dcm = np.asarray(dcm if dcm is not None else np.eye(3))

        expected_transformed = dcm.dot(coordinate)
        transformed = angular.apply(coordinate)

        assert transformed.shape == expected_transformed.shape
        assert transformed == pytest.approx(expected_transformed)


if __name__ == "__main__":
    pytest.main()

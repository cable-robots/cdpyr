import numpy as np
import pytest

from cdpyr.analysis.kinematics.pulley import Pulley as Kinematics
from cdpyr.motion import pose as _pose
from cdpyr.robot import kinematicchain, Robot, sample


class PulleyKinematicsBackwardTestSuite(object):

    @pytest.mark.parametrize(
            ('robot', 'pose'),
            (
                    (sample.robot_1t(), _pose.ZeroPose),
                    (sample.robot_1t(), _pose.PoseGenerator.random_1t()),
                    (sample.robot_2t(), _pose.ZeroPose),
                    (sample.robot_2t(), _pose.PoseGenerator.random_2t()),
                    (sample.robot_3t(), _pose.ZeroPose),
                    (sample.robot_3t(), _pose.PoseGenerator.random_3t()),
                    (sample.robot_1r2t(), _pose.ZeroPose),
                    (sample.robot_1r2t(), _pose.PoseGenerator.random_1r2t()),
                    (sample.robot_2r3t(), _pose.ZeroPose),
                    (sample.robot_2r3t(), _pose.PoseGenerator.random_2r3t()),
                    (sample.robot_3r3t(), _pose.ZeroPose),
                    (sample.robot_3r3t(), _pose.PoseGenerator.random_3r3t()),
            ),
            ids=[
                    '1T_home', '1T_random',
                    '2T_home', '2T_random',
                    '3T_home', '3T_random',
                    '1R2T_home', '1R2T_random',
                    '2R3T_home', '2R3T_random',
                    '3R3T_home', '3R3T_random',
            ],
    )
    def test_backward(self,
                      robot: Robot,
                      pose: _pose.Pose):
        # kinematics object
        ik = Kinematics()

        # solve the inverse kinematics
        res_backward = ik.backward(robot, pose)

        nl, _ = robot.num_dimensionality
        kc: kinematicchain.KinematicChain

        assert res_backward.pose == pose
        assert res_backward.lengths.ndim == 1
        assert res_backward.lengths.shape == (robot.num_kinematic_chains,)
        assert (0 <= res_backward.lengths).all()
        assert res_backward.directions.shape == (robot.num_kinematic_chains, nl)

    @pytest.mark.parametrize(
            ('robot', 'pose'),
            (
                    (sample.robot_1t(), _pose.ZeroPose),
                    (sample.robot_1t(), _pose.PoseGenerator.random_1t()),
                    (sample.robot_2t(), _pose.ZeroPose),
                    (sample.robot_2t(), _pose.PoseGenerator.random_2t()),
                    (sample.robot_3t(), _pose.ZeroPose),
                    (sample.robot_3t(), _pose.PoseGenerator.random_3t()),
                    (sample.robot_1r2t(), _pose.ZeroPose),
                    (sample.robot_1r2t(), _pose.PoseGenerator.random_1r2t()),
                    (sample.robot_2r3t(), _pose.ZeroPose),
                    (sample.robot_2r3t(), _pose.PoseGenerator.random_2r3t()),
                    (sample.robot_3r3t(), _pose.ZeroPose),
                    (sample.robot_3r3t(), _pose.PoseGenerator.random_3r3t()),
            ),
            ids=[
                    '1T_home', '1T_random',
                    '2T_home', '2T_random',
                    '3T_home', '3T_random',
                    '1R2T_home', '1R2T_random',
                    '2R3T_home', '2R3T_random',
                    '3R3T_home', '3R3T_random',
            ],
    )
    def test_forward(self,
                     robot: Robot,
                     pose: _pose.Pose):
        # kinematics object
        ik = Kinematics()

        # first, calculate cable lengths to run forward kinematics
        res_backward = ik.backward(robot, pose)

        # now, solve forward kinematics
        res_forward = ik.forward(robot, res_backward.lengths)

        nl, _ = robot.num_dimensionality
        kc: kinematicchain.KinematicChain

        assert res_forward.pose.linear.position \
               == pytest.approx(res_backward.pose.linear.position,
                                abs=1e-4, rel=1e-4)
        assert res_forward.pose.angular.quaternion \
               == pytest.approx(res_backward.pose.angular.quaternion,
                                abs=1e-4, rel=1e-4)
        assert res_forward.lengths.ndim == 1
        assert res_forward.lengths.shape == (robot.num_kinematic_chains,)
        assert (0 <= res_forward.lengths).all()
        assert res_forward.directions.shape == (robot.num_kinematic_chains, nl)
        for idxkc, kc in enumerate(robot.kinematic_chains):
            fanchor = robot.frame.anchors[kc.frame_anchor].linear.position
            platform = robot.platforms[kc.platform]
            panchor = platform.anchors[kc.platform_anchor].linear.position

            assert res_backward.leave_points[idxkc, 0:nl] \
                   == pytest.approx(fanchor[0:nl])
            assert np.linalg.norm(res_backward.directions[idxkc, 0:nl]) \
                   == pytest.approx(1)


if __name__ == "__main__":
    pytest.main()

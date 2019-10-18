import cdpyr


class StructureMatrixTestSuite(object):

    def test_1t(self, robot_1t, rand_pose_1t, ik_standard):
        sms = cdpyr.analysis.structurematrix.Calculator()

        _, uis = ik_standard.backward(robot_1t, rand_pose_1t)

        structmat = sms(robot_1t, uis)

        assert structmat.shape == (1, robot_1t.num_kinematic_chains)

    def test_2t(self, robot_2t, rand_pose_2t, ik_standard):
        sms = cdpyr.analysis.structurematrix.Calculator()

        _, uis = ik_standard.backward(robot_2t, rand_pose_2t)

        structmat = sms(robot_2t, uis)

        assert structmat.shape == (2, robot_2t.num_kinematic_chains)

    def test_3t(self, robot_3t, rand_pose_3t, ik_standard):
        sms = cdpyr.analysis.structurematrix.Calculator()

        _, uis = ik_standard.backward(robot_3t, rand_pose_3t)

        structmat = sms(robot_3t, uis)

        assert structmat.shape == (3, robot_3t.num_kinematic_chains)

    def test_1r2t(self, robot_1r2t, rand_pose_1r2t, ik_standard):
        sms = cdpyr.analysis.structurematrix.Calculator()

        _, uis = ik_standard.backward(robot_1r2t, rand_pose_1r2t)

        structmat = sms(robot_1r2t, uis, rand_pose_1r2t)

        assert structmat.shape == (3, robot_1r2t.num_kinematic_chains)

    def test_2r3t(self, robot_2r3t, rand_pose_2r3t, ik_standard):
        sms = cdpyr.analysis.structurematrix.Calculator()

        _, uis = ik_standard.backward(robot_2r3t, rand_pose_2r3t)

        structmat = sms(robot_2r3t, uis, rand_pose_2r3t)

        assert structmat.shape == (5, robot_2r3t.num_kinematic_chains)

    def test_3r3t(self, robot_3r3t, rand_pose_3r3t, ik_standard):
        sms = cdpyr.analysis.structurematrix.Calculator()

        _, uis = ik_standard.backward(robot_3r3t, rand_pose_3r3t)

        structmat = sms(robot_3r3t, uis, rand_pose_3r3t)

        assert structmat.shape == (6, robot_3r3t.num_kinematic_chains)

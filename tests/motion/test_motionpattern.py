import cdpyr


class MotionpatternTestSuite(object):

    def test_motionpattern_1t(self):
        mp = cdpyr.motion.Motionpattern._1T

        assert mp.dof_translation == 1
        assert mp.dof_rotation == 0
        assert mp.human == "1T"
        assert mp.moves_linear
        assert not mp.moves_planar
        assert not mp.moves_spatial
        assert mp.is_point
        assert not mp.is_beam
        assert not mp.is_cuboid

    def test_motionpattern_2t(self):
        mp = cdpyr.motion.Motionpattern._2T

        assert mp.dof_translation == 2
        assert mp.dof_rotation == 0
        assert mp.human == "2T"
        assert not mp.moves_linear
        assert mp.moves_planar
        assert not mp.moves_spatial
        assert mp.is_point
        assert not mp.is_beam
        assert not mp.is_cuboid

    def test_motionpattern_3t(self):
        mp = cdpyr.motion.Motionpattern._3T

        assert mp.dof_translation == 3
        assert mp.dof_rotation == 0
        assert mp.human == "3T"
        assert not mp.moves_linear
        assert not mp.moves_planar
        assert mp.moves_spatial
        assert mp.is_point
        assert not mp.is_beam
        assert not mp.is_cuboid

    def test_motionpattern_1r2t(self):
        mp = cdpyr.motion.Motionpattern._1R2T

        assert mp.dof_translation == 2
        assert mp.dof_rotation == 1
        assert mp.human == "1R2T"
        assert not mp.moves_linear
        assert mp.moves_planar
        assert not mp.moves_spatial
        assert not mp.is_point
        assert mp.is_beam
        assert not mp.is_cuboid

    def test_motionpattern_2r3t(self):
        mp = cdpyr.motion.Motionpattern._2R3T

        assert mp.dof_translation == 3
        assert mp.dof_rotation == 2
        assert mp.human == "2R3T"
        assert not mp.moves_linear
        assert not mp.moves_planar
        assert mp.moves_spatial
        assert not mp.is_point
        assert mp.is_beam
        assert not mp.is_cuboid

    def test_motionpattern_3r3t(self):
        mp = cdpyr.motion.Motionpattern._3R3T

        assert mp.dof_translation == 3
        assert mp.dof_rotation == 3
        assert mp.human == "3R3T"
        assert not mp.moves_linear
        assert not mp.moves_planar
        assert mp.moves_spatial
        assert not mp.is_point
        assert not mp.is_beam
        assert mp.is_cuboid

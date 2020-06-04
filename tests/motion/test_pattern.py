from __future__ import annotations

import pytest

import cdpyr

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"


class MotionPatternTestSuite(object):

    def test_motion_pattern_1t(self):
        mp = cdpyr.motion.pattern.MP_1T

        assert mp.dof_translation == 1
        assert mp.dof_rotation == 0
        assert mp.dof == 1 + 0
        assert mp.human == "1T"
        assert mp.moves_linear
        assert not mp.moves_planar
        assert not mp.moves_spatial
        assert mp.is_point
        assert not mp.is_beam
        assert not mp.is_cuboid

    def test_motion_pattern_2t(self):
        mp = cdpyr.motion.pattern.MP_2T

        assert mp.dof_translation == 2
        assert mp.dof_rotation == 0
        assert mp.dof == 2 + 0
        assert mp.human == "2T"
        assert not mp.moves_linear
        assert mp.moves_planar
        assert not mp.moves_spatial
        assert mp.is_point
        assert not mp.is_beam
        assert not mp.is_cuboid

    def test_motion_pattern_3t(self):
        mp = cdpyr.motion.pattern.MP_3T

        assert mp.dof_translation == 3
        assert mp.dof_rotation == 0
        assert mp.dof == 3 + 0
        assert mp.human == "3T"
        assert not mp.moves_linear
        assert not mp.moves_planar
        assert mp.moves_spatial
        assert mp.is_point
        assert not mp.is_beam
        assert not mp.is_cuboid

    def test_motion_pattern_1r2t(self):
        mp = cdpyr.motion.pattern.MP_1R2T

        assert mp.dof_translation == 2
        assert mp.dof_rotation == 1
        assert mp.dof == 2 + 1
        assert mp.human == "1R2T"
        assert not mp.moves_linear
        assert mp.moves_planar
        assert not mp.moves_spatial
        assert not mp.is_point
        assert mp.is_beam
        assert not mp.is_cuboid

    def test_motion_pattern_2r3t(self):
        mp = cdpyr.motion.pattern.MP_2R3T

        assert mp.dof_translation == 3
        assert mp.dof_rotation == 2
        assert mp.dof == 3 + 2
        assert mp.human == "2R3T"
        assert not mp.moves_linear
        assert not mp.moves_planar
        assert mp.moves_spatial
        assert not mp.is_point
        assert mp.is_beam
        assert not mp.is_cuboid

    def test_motion_pattern_3r3t(self):
        mp = cdpyr.motion.pattern.MP_3R3T

        assert mp.dof_translation == 3
        assert mp.dof_rotation == 3
        assert mp.dof == 3 + 3
        assert mp.human == "3R3T"
        assert not mp.moves_linear
        assert not mp.moves_planar
        assert mp.moves_spatial
        assert not mp.is_point
        assert not mp.is_beam
        assert mp.is_cuboid


if __name__ == "__main__":
    pytest.main()

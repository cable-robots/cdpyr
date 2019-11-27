import pytest

from cdpyr.motion.pose import generator

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"


class PoseGeneratorTranslationTestSuite(object):

    def tests_linear_default_step(self):
        poses = generator.translation(0.0, 1.0)

    def tests_linear_custom_step(self):
        poses = generator.translation(0.0, 1.0, steps=25)
        with pytest.raises(Exception):
            poses = generator.translation(0.0, 1.0, steps=[25, 25])

    def tests_planar_default_step(self):
        poses = generator.translation([0.0, 0.0], [1.0, 2.0])

    def tests_planar_custom_step(self):
        poses = generator.translation(
            [0.0, 0.0],
            [1.0, 2.0],
            steps=25)
        poses = generator.translation(
            [0.0, 0.0],
            [1.0, 2.0],
            steps=[25, 25])
        with pytest.raises(Exception):
            poses = generator.translation(
                [0.0, 0.0],
                [1.0, 2.0],
                steps=[25, 25, 25])

    def tests_spatial_default_step(self):
        poses = generator.translation(
            [0.0, 0.0, 0.0],
            [1.0, 2.0, 3.0],
            steps=25)
        poses = generator.translation(
            [0.0, 0.0, 0.0],
            [1.0, 2.0, 3.0],
            steps=[25, 25, 25])
        with pytest.raises(Exception):
            poses = generator.translation(
                [0.0, 0.0, 0.0],
                [1.0, 2.0, 3.0],
                steps=[25, 25])


if __name__ == "__main__":
    pytest.main()

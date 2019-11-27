import numpy as np
import pytest

from cdpyr.motion.pose import generator

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"


class PoseGeneratorOrientationTestSuite(object):

    def tests_linear_default_step(self):
        poses = generator.orientation(0.0, 0.5 * np.pi, 'x')

    def tests_linear_custom_step(self):
        poses = generator.orientation(0.0, 0.5 * np.pi, 'x', steps=25)
        with pytest.raises(Exception):
            poses = generator.orientation(0.0, 0.5 * np.pi, 'x', steps=[25, 25])

    def tests_planar_default_step(self):
        poses = generator.orientation([0.0, 0.0],
                                      [0.5 * np.pi, 1.0 * np.pi],
                                      'xy')

    def tests_planar_custom_step(self):
        poses = generator.orientation(
            [0.0, 0.0],
            [0.5 * np.pi, 1.0 * np.pi],
            'xy',
            steps=25)
        poses = generator.orientation(
            [0.0, 0.0],
            [0.5 * np.pi, 1.0 * np.pi],
            'xy',
            steps=[25, 25])
        with pytest.raises(Exception):
            poses = generator.orientation(
                [0.0, 0.0],
                [0.5 * np.pi, 1.0 * np.pi],
                'xy',
                steps=[25, 25, 25])

    def tests_spatial_default_step(self):
        poses = generator.orientation(
            [0.0, 0.0, 0.0],
            [0.5 * np.pi, 1.0 * np.pi, 1.5 * np.pi],
            'xyz',
            steps=25)
        poses = generator.orientation(
            [0.0, 0.0, 0.0],
            [0.5 * np.pi, 1.0 * np.pi, 1.5 * np.pi],
            'xyz',
            steps=[25, 25, 25])
        with pytest.raises(Exception):
            poses = generator.orientation(
                [0.0, 0.0, 0.0],
                [0.5 * np.pi, 1.0 * np.pi, 1.5 * np.pi],
                'xyz',
                steps=[25, 25])


if __name__ == "__main__":
    pytest.main()

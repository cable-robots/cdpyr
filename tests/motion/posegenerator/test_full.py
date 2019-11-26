import numpy as np
import pytest

from cdpyr.motion.pose import generator_new as generator

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"


class PoseGeneratorFullTestSuite(object):

    def tests_linear_default_step(self):
        poses = generator.full(0.0, 1.0, 0.0, np.pi, 'x')

    def tests_linear_custom_step(self):
        poses = generator.full(0.0, 1.0, 0.0, np.pi, 'x', step=25)
        with pytest.raises(Exception):
            poses = generator.full(0.0, 1.0, 0.0, np.pi, 'x', step=[25, 25])

    def tests_planar_default_step(self):
        poses = generator.full([0.0, 0.0], [1.0, 2.0],
                               [0.0, 0.0], [0.5 * np.pi, 1.0 * np.pi],
                               'xy')

    def tests_planar_custom_step(self):
        poses = generator.full(
            [0.0, 0.0],
            [1.0, 2.0],
            [0.0, 0.0],
            [0.5 * np.pi, 1.0 * np.pi],
            'xy',
            step=25)
        poses = generator.full(
            [0.0, 0.0],
            [1.0, 2.0],
            [0.0, 0.0],
            [0.5 * np.pi, 1.0 * np.pi],
            'xy',
            step=[25, 25])
        with pytest.raises(Exception):
            poses = generator.full(
                [0.0, 0.0],
                [1.0, 2.0],
                [0.0, 0.0],
                [0.5 * np.pi, 1.0 * np.pi],
                'xy',
                step=[25, 25, 25])

    def tests_spatial_default_step(self):
        poses = generator.full(
            [0.0, 0.0, 0.0],
            [1.0, 2.0, 3.0],
            [0.0, 0.0, 0.0],
            [0.5 * np.pi, 1.0 * np.pi, 1.5 * np.pi],
            'xyz',
            step=25)
        poses = generator.full(
            [0.0, 0.0, 0.0],
            [1.0, 2.0, 3.0],
            [0.0, 0.0, 0.0],
            [0.5 * np.pi, 1.0 * np.pi, 1.5 * np.pi],
            'xyz',
            step=[25, 25, 25])
        with pytest.raises(Exception):
            poses = generator.full(
                [0.0, 0.0, 0.0],
                [1.0, 2.0, 3.0],
                [0.0, 0.0, 0.0],
                [0.5 * np.pi, 1.0 * np.pi, 1.5 * np.pi],
                'xyz',
                step=[25, 25])


if __name__ == "__main__":
    pytest.main()

import itertools

import numpy as np
from pytest import mark
from scipy.spatial import transform as _transform

import cdpyr


class FromEulerTestSuite(object):

    @mark.parametrize(
        ("seq"),
        list(''.join(seq) for seq in itertools.chain.from_iterable(
            itertools.permutations(['x', 'y', 'z'], k) for k in range(1, 4)))
    )
    def test_intrinsic(self, seq):
        angles = np.random.random(len(seq))
        assert np.allclose(cdpyr.motion.pose.generator.from_euler(seq, angles),
                           _transform.Rotation.from_euler(seq, angles).as_dcm())

    @mark.parametrize(
        ("seq"),
        list(''.join(seq) for seq in itertools.chain.from_iterable(
            itertools.permutations(['X', 'Y', 'Z'], k) for k in range(1, 4)))
    )
    def test_extrinsic(self, seq):
        angles = np.random.random(len(seq))
        assert np.allclose(cdpyr.motion.pose.generator.from_euler(seq, angles),
                           _transform.Rotation.from_euler(seq, angles).as_dcm())

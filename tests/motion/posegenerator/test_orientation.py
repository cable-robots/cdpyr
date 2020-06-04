from __future__ import annotations

import itertools
from typing import (
    AnyStr,
    Union
)

import numpy as np
import pytest

from cdpyr.motion import pose
from cdpyr.typing import (
    Num,
    Vector
)

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"


class PoseGeneratorOrientationTestSuite(object):

    @pytest.mark.parametrize(
        ['start', 'end', 'sequence', 'steps'],
        itertools.chain(
            ((-np.pi, np.pi, 'x', step) for step in (None, 11)),
            (([-np.pi, np.pi], [np.pi, -np.pi], 'xy', step) for step in
             (None, 11, [11, 9])),
            ((
                [-np.pi, np.pi, -0.5 * np.pi], [np.pi, -np.pi, 0.5 * np.pi],
                'xyz',
                step) for step in (None, 11, [11, 9, 7]))
        )
    )
    def test_works_as_expected(self,
                               start: Vector,
                               end: Vector,
                               sequence: AnyStr,
                               steps: Union[Num, Vector]):
        # get a pose generator
        actual_poses = pose.PoseGenerator.orientation(start, end, sequence, steps=steps)


if __name__ == "__main__":
    pytest.main()

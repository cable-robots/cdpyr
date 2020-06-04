from __future__ import annotations

import itertools
from typing import Union

import pytest

from cdpyr.motion import pose
from cdpyr.typing import (
    Num,
    Vector
)

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"


class PoseGeneratorTranslationTestSuite(object):

    @pytest.mark.parametrize(
        ['start', 'end', 'steps'],
        itertools.chain(
            ((0.0, 1.0, step) for step in (None, 11)),
            (([0.0, 0.0], [1.0, 2.0], step) for step in (None, 11, [11, 9])),
            (([0.0, 0.0, 0.0], [1.0, 2.0, 3.0], step) for step in
             (None, 11, [11, 9, 7]))
        )
    )
    def test_works_as_expected(self,
                               start: Vector,
                               end: Vector,
                               steps: Union[Num, Vector]):
        # get a pose generator
        actual_poses = pose.PoseGenerator.translation(start, end, steps=steps)


if __name__ == "__main__":
    pytest.main()

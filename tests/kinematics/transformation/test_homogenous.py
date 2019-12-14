import itertools
from typing import Union

from scipy.spatial.transform import Rotation

import numpy as np
import pytest

from cdpyr.kinematics.transformation.homogenous import Homogenous
from cdpyr.typing import (
    Vector
)


class HomogenousTransformationTestSuite(object):

    def test_empty_object(self):
        homogenous = Homogenous()

        assert isinstance(homogenous, Homogenous)

        assert homogenous.translation.shape == (3,)
        assert homogenous.translation == pytest.approx([0., 0., 0.])
        assert homogenous.dcm.shape == (3, 3)
        assert homogenous.dcm == pytest.approx(np.eye(3))
        assert homogenous.matrix.shape == (4, 4)
        assert homogenous.matrix[0:3, 0:3] == pytest.approx(np.eye(3))
        assert homogenous.matrix[0:3, -1] == pytest.approx([0., 0., 0.])
        assert homogenous.matrix[-1, -1] == pytest.approx(1)

    @pytest.mark.parametrize(
            ('translation', 'rotation'),
            (
                    itertools.product(
                            (None, np.zeros((3,)), np.random.random((3,))),
                            (None, np.eye(3)) + tuple(Rotation.random(25).as_dcm()),
                    )
            )
    )
    def test_init(self, translation: Union[None, Vector],
                  rotation: Union[None, Vector]):
        homogenous = Homogenous(translation, rotation)

        translation = np.asarray(
                translation if translation is not None else [0.0, 0.0, 0.0])
        rotation = np.asarray(rotation if rotation is not None else np.eye(3))

        assert homogenous.translation.shape == translation.shape
        assert homogenous.dcm.shape == rotation.shape
        assert homogenous.matrix.shape == (4, 4)
        assert homogenous.translation == pytest.approx(translation)
        assert homogenous.dcm == pytest.approx(rotation)
        assert homogenous.matrix[0:3, 0:3] == pytest.approx(rotation)
        assert homogenous.matrix[0:3, -1] == pytest.approx(translation)
        assert homogenous.matrix[-1, -1] == pytest.approx(1)


if __name__ == "__main__":
    pytest.main()

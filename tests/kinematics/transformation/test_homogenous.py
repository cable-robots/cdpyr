from typing import Sequence

import numpy as np
from pytest import approx, mark
from scipy.spatial.transform import Rotation

import cdpyr


class HomogenousTransformationTestSuite(object):

    def test_empty_object(self):
        homogenous = cdpyr.kinematics.transformation.Homogenous()

        assert isinstance(homogenous,
                          cdpyr.kinematics.transformation.Homogenous)

        assert homogenous.translation.shape == (3,)
        assert homogenous.translation == approx([0., 0., 0.])
        assert homogenous.rotation.shape == (3, 3)
        assert homogenous.rotation == approx(np.eye(3))
        assert homogenous.matrix.shape == (4, 4)
        assert homogenous.matrix[0:3, 0:3] == approx(np.eye(3))
        assert homogenous.matrix[0:3, -1] == approx([0., 0., 0.])
        assert homogenous.matrix[-1, -1] == approx(1)

    @mark.parametrize(
        "translation",
        [
            (np.random.random(3).tolist())
        ]
    )
    def test_with_translation_from_list(self, translation: Sequence):
        homogenous = cdpyr.kinematics.transformation.Homogenous(
            translation=translation
        )

        assert homogenous.translation.shape == (len(translation),)
        assert homogenous.translation == approx(translation)
        assert homogenous.rotation.shape == (3, 3)
        assert homogenous.rotation == approx(np.eye(3))
        assert homogenous.matrix.shape == (4, 4)
        assert homogenous.matrix[0:3, 0:3] == approx(np.eye(3))
        assert homogenous.matrix[0:3, -1] == approx(translation)
        assert homogenous.matrix[-1, -1] == approx(1)

    @mark.parametrize(
        "translation",
        [
            (np.random.random(3))
        ]
    )
    def test_with_translation_from_numpyarray(self, translation: np.ndarray):
        homogenous = cdpyr.kinematics.transformation.Homogenous(
            translation=translation
        )

        assert homogenous.translation.shape == translation.shape
        assert homogenous.translation == approx(translation)
        assert homogenous.rotation.shape == (3, 3)
        assert homogenous.rotation == approx(np.eye(3))
        assert homogenous.matrix.shape == (4, 4)
        assert homogenous.matrix[0:3, 0:3] == approx(np.eye(3))
        assert homogenous.matrix[0:3, -1] == approx(translation)
        assert homogenous.matrix[-1, -1] == approx(1)

    @mark.parametrize(
        "rotation",
        [
            (Rotation.random().as_dcm().tolist())
        ]
    )
    def test_with_rotation_from_list(self, rotation: Sequence[Sequence]):
        homogenous = cdpyr.kinematics.transformation.Homogenous(
            rotation=rotation
        )

        assert homogenous.translation.shape == (3, )
        assert homogenous.translation == approx([0., 0., 0.])
        assert homogenous.rotation.shape == (3, 3)
        assert homogenous.rotation == approx(np.asarray(rotation))
        assert homogenous.matrix.shape == (4, 4)
        assert homogenous.matrix[0:3, 0:3] == approx(np.asarray(rotation))
        assert homogenous.matrix[0:3, -1] == approx([0., 0., 0.])
        assert homogenous.matrix[-1, -1] == approx(1)

    @mark.parametrize(
        "rotation",
        [
            (Rotation.random().as_dcm())
        ]
    )
    def test_with_rotation_from_numpyarray(self, rotation: np.ndarray):
        homogenous = cdpyr.kinematics.transformation.Homogenous(
            rotation=rotation
        )

        assert homogenous.translation.shape == (3, )
        assert homogenous.translation == approx([0., 0., 0.])
        assert homogenous.rotation.shape == (3, 3)
        assert homogenous.rotation == approx(rotation)
        assert homogenous.matrix.shape == (4, 4)
        assert homogenous.matrix[0:3, 0:3] == approx(rotation)
        assert homogenous.matrix[0:3, -1] == approx([0., 0., 0.])
        assert homogenous.matrix[-1, -1] == approx(1)

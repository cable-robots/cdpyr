from typing import Sequence

import numpy as np
import pytest
from scipy.spatial.transform import Rotation

import cdpyr


class HomogenousTransformationTestSuite(object):

    def test_empty_object(self):
        homogenous = cdpyr.kinematics.transformation.Homogenous()

        assert isinstance(homogenous,
                          cdpyr.kinematics.transformation.Homogenous)

        assert homogenous.translation.shape == (3,)
        assert homogenous.translation == pytest.approx([0., 0., 0.])
        assert homogenous.dcm.shape == (3, 3)
        assert homogenous.dcm == pytest.approx(np.eye(3))
        assert homogenous.matrix.shape == (4, 4)
        assert homogenous.matrix[0:3, 0:3] == pytest.approx(np.eye(3))
        assert homogenous.matrix[0:3, -1] == pytest.approx([0., 0., 0.])
        assert homogenous.matrix[-1, -1] == pytest.approx(1)

    @pytest.mark.parametrize(
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
        assert homogenous.translation == pytest.approx(translation)
        assert homogenous.dcm.shape == (3, 3)
        assert homogenous.dcm == pytest.approx(np.eye(3))
        assert homogenous.matrix.shape == (4, 4)
        assert homogenous.matrix[0:3, 0:3] == pytest.approx(np.eye(3))
        assert homogenous.matrix[0:3, -1] == pytest.approx(translation)
        assert homogenous.matrix[-1, -1] == pytest.approx(1)

    @pytest.mark.parametrize(
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
        assert homogenous.translation == pytest.approx(translation)
        assert homogenous.dcm.shape == (3, 3)
        assert homogenous.dcm == pytest.approx(np.eye(3))
        assert homogenous.matrix.shape == (4, 4)
        assert homogenous.matrix[0:3, 0:3] == pytest.approx(np.eye(3))
        assert homogenous.matrix[0:3, -1] == pytest.approx(translation)
        assert homogenous.matrix[-1, -1] == pytest.approx(1)

    @pytest.mark.parametrize(
        "dcm",
        [
            (Rotation.random().as_dcm().tolist())
        ]
    )
    def test_with_dcm_from_list(self, dcm: Sequence[Sequence]):
        homogenous = cdpyr.kinematics.transformation.Homogenous(
            dcm=dcm
        )

        assert homogenous.translation.shape == (3,)
        assert homogenous.translation == pytest.approx([0., 0., 0.])
        assert homogenous.dcm.shape == (3, 3)
        assert homogenous.dcm == pytest.approx(np.asarray(dcm))
        assert homogenous.matrix.shape == (4, 4)
        assert homogenous.matrix[0:3, 0:3] == pytest.approx(np.asarray(dcm))
        assert homogenous.matrix[0:3, -1] == pytest.approx([0., 0., 0.])
        assert homogenous.matrix[-1, -1] == pytest.approx(1)

    @pytest.mark.parametrize(
        "dcm",
        [
            (Rotation.random().as_dcm())
        ]
    )
    def test_with_dcm_from_numpyarray(self, dcm: np.ndarray):
        homogenous = cdpyr.kinematics.transformation.Homogenous(
            dcm=dcm
        )

        assert homogenous.translation.shape == (3,)
        assert homogenous.translation == pytest.approx([0., 0., 0.])
        assert homogenous.dcm.shape == (3, 3)
        assert homogenous.dcm == pytest.approx(dcm)
        assert homogenous.matrix.shape == (4, 4)
        assert homogenous.matrix[0:3, 0:3] == pytest.approx(dcm)
        assert homogenous.matrix[0:3, -1] == pytest.approx([0., 0., 0.])
        assert homogenous.matrix[-1, -1] == pytest.approx(1)


if __name__ == "__main__":
    pytest.main()

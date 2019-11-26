import numpy as np
import pytest
from scipy.spatial.transform import Rotation

from cdpyr.kinematics.transformation.homogenous import Homogenous
from cdpyr.typing import (
    Matrix,
    Vector
)


class HomogenousTransformationTestSuite(object):

    def test_empty_object(self):
        homogenous = Homogenous()

        assert isinstance(homogenous,
                          Homogenous)

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
    def test_with_translation_from_list(self, translation: Vector):
        homogenous = Homogenous(
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
    def test_with_translation_from_numpyarray(self, translation: Vector):
        homogenous = Homogenous(
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
    def test_with_dcm_from_list(self, dcm: Matrix):
        homogenous = Homogenous(
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
    def test_with_dcm_from_numpyarray(self, dcm: Matrix):
        homogenous = Homogenous(
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

    @pytest.mark.parametrize(
        ["translation", "coordinate"],
        [
            (np.random.random(3), np.random.random(3)),
        ]
    )
    def test_apply_translation_to_single_coordinate(self,
                                                    translation: Vector,
                                                    coordinate: Vector):
        homogenous = Homogenous(
            translation
        )

        assert homogenous.apply(coordinate) == pytest.approx(
            coordinate + translation)

    @pytest.mark.parametrize(
        ["translation", "coordinate"],
        [
            (np.random.random(3), np.random.random((3, 12))),
        ]
    )
    def test_apply_translation_to_multiple_coordinates(self,
                                                       translation: Vector,
                                                       coordinate: Vector):
        homogenous = Homogenous(
            translation
        )

        assert homogenous.apply(coordinate) == pytest.approx(
            coordinate + translation[:, np.newaxis])

    @pytest.mark.parametrize(
        ["rotation", "coordinate"],
        [
            ((Rotation.random().as_dcm()), np.random.random(3)),
        ]
    )
    def test_apply_rotation_to_single_coordinate(self,
                                                 rotation: Matrix,
                                                 coordinate: Vector):
        homogenous = Homogenous(
            dcm=rotation
        )

        assert homogenous.apply(coordinate) == pytest.approx(
            rotation.dot(coordinate))

    @pytest.mark.parametrize(
        ["rotation", "coordinate"],
        [
            ((Rotation.random().as_dcm()), np.random.random((3, 12))),
        ]
    )
    def test_apply_rotation_to_multiple_coordinates(self,
                                                    rotation: Matrix,
                                                    coordinate: Vector):
        homogenous = Homogenous(
            dcm=rotation
        )

        assert homogenous.apply(coordinate) == pytest.approx(
            rotation.dot(coordinate))

    @pytest.mark.parametrize(
        ["translation", "rotation", "coordinate"],
        [
            (np.random.random(3), Rotation.random().as_dcm(),
             np.random.random(3)),
        ]
    )
    def test_apply_full_to_single_coordinate(self,
                                             translation: Vector,
                                             rotation: Matrix,
                                             coordinate: Vector):
        homogenous = Homogenous(
            translation,
            rotation
        )

        assert homogenous.apply(coordinate) == pytest.approx(
            rotation.dot(coordinate) + translation)

    @pytest.mark.parametrize(
        ["translation", "rotation", "coordinate"],
        [
            (np.random.random(3), Rotation.random().as_dcm(),
             np.random.random((3, 12))),
        ]
    )
    def test_apply_full_to_multiple_coordinates(self,
                                                translation: Vector,
                                                rotation: Matrix,
                                                coordinate: Vector):
        homogenous = Homogenous(
            translation,
            rotation
        )

        assert homogenous.apply(coordinate) == pytest.approx(
            rotation.dot(coordinate) + translation[:, np.newaxis])


if __name__ == "__main__":
    pytest.main()

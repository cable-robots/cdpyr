import numpy as np
import pytest

import cdpyr


class InertiaTestSuite(object):

    def test_empty_inertia(self):
        inertia = cdpyr.mechanics.Inertia()

        assert inertia.linear.ndim == 2
        assert inertia.linear.shape == (3, 3)
        assert np.diag(inertia.linear) == pytest.approx(np.full((3,), np.inf))
        assert np.triu(inertia.linear, 1) == pytest.approx(np.zeros((3, 3)))
        assert np.tril(inertia.linear, -1) == pytest.approx(np.zeros((3, 3)))

        assert inertia.angular.ndim == 2
        assert inertia.angular.shape == (3, 3)
        assert np.diag(inertia.angular) == pytest.approx(np.full((3,), np.inf))
        assert np.triu(inertia.angular, 1) == pytest.approx(np.zeros((3, 3)))
        assert np.tril(inertia.angular, -1) == pytest.approx(np.zeros((3, 3)))

    def test_initialize_passes(self):
        linear_inertia = np.random.random((3, 3))
        angular_inertia = np.random.random((3, 3))

        inertia = cdpyr.mechanics.Inertia(linear_inertia, angular_inertia)

        assert inertia.linear.ndim == 2
        assert inertia.linear.shape == (3, 3)
        assert inertia.linear == pytest.approx(linear_inertia)

        assert inertia.angular.ndim == 2
        assert inertia.angular.shape == (3, 3)
        assert inertia.angular == pytest.approx(angular_inertia)

    def test_initialize_fails(self):
        linear_inertia = np.random.random((3,))
        angular_inertia = np.random.random((3,))

        with pytest.raises(ValueError) as excinfo:
            inertia = cdpyr.mechanics.Inertia(linear_inertia, angular_inertia)

    def test_property_descriptor_passes(self):
        inertia = cdpyr.mechanics.Inertia()

        linear_inertia = np.random.random((3, 3))
        angular_inertia = np.random.random((3, 3))

        # setting the linear inertia
        inertia.linear = linear_inertia

        assert inertia.linear.ndim == 2
        assert inertia.linear.shape == (3, 3)
        assert inertia.linear == pytest.approx(linear_inertia)

        # setting the angular inertia
        inertia.angular = angular_inertia

        assert inertia.angular.ndim == 2
        assert inertia.angular.shape == (3, 3)
        assert inertia.angular == pytest.approx(angular_inertia)

    def test_property_descriptor_passes(self):
        inertia = cdpyr.mechanics.Inertia()
        linear_inertia = np.random.random((3,))
        angular_inertia = np.random.random((3,))

        # setting the linear inertia
        with pytest.raises(ValueError) as excinfo:
            inertia.linear = linear_inertia

        # setting the angular inertia
        with pytest.raises(ValueError) as excinfo:
            inertia.angular = angular_inertia


if __name__ == "__main__":
    pytest.main()

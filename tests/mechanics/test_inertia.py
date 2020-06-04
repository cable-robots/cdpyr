import numpy as np
import pytest

import cdpyr


class InertiaTestSuite(object):

    @pytest.mark.parametrize(
        ('linear', 'angular'),
        (
                (None, None),
                (np.diag(np.random.random((3, ))), np.random.random((3, 3))),
        )
    )
    def test_empty_inertia(self, linear, angular):
        inertia = cdpyr.mechanics.Inertia(linear, angular)

        assert inertia.linear.ndim == 2
        assert inertia.linear.shape == (3, 3)
        if linear is None:
            assert np.diag(inertia.linear) == pytest.approx(np.full((3,), np.inf))
        else:
            assert inertia.linear == pytest.approx(linear)

        assert inertia.angular.ndim == 2
        assert inertia.angular.shape == (3, 3)
        if angular is None:
            assert np.diag(inertia.angular) == pytest.approx(np.full((3,), np.inf))
        else:
            assert inertia.angular == pytest.approx(angular)


if __name__ == "__main__":
    pytest.main()

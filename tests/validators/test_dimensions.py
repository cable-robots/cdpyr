import numpy as np_

from cdpyr import validator


class DimensionsTestSuite(object):

    def test_scalar(self):
        validator.dimensions(1, 0)

    def test_list(self):
        validator.dimensions((1, 2), 1)

    def test_list_of_list(self):
        validator.dimensions(((1, 2), (3, 4)), 2)

    def test_numpyarray(self):
        validator.dimensions(np_.asarray((1, 2)), 1)

    def test_numpyarray(self):
        validator.dimensions(np_.asarray(((1, 2), (3, 4))), 2)

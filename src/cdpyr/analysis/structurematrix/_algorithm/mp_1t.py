import numpy as np_

from cdpyr.analysis.structurematrix._algorithm.algorithm import Algorithm


class MP_1T(Algorithm):

    @staticmethod
    def _calculate(ui: np_.ndarray):
        return np_.vstack(ui).T

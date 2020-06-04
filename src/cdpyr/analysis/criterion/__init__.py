__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"
__all__ = [
        'CableLength',
        'Interference',
        'Singularities',
        'WrenchClosure',
        'WrenchFeasible',
]

from cdpyr.analysis.criterion.cable_length import CableLength
from cdpyr.analysis.criterion.interference import Interference
from cdpyr.analysis.criterion.singularities import Singularities
from cdpyr.analysis.criterion.wrench_closure import WrenchClosure
from cdpyr.analysis.criterion.wrench_feasible import WrenchFeasible

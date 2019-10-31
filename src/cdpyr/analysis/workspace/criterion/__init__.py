from cdpyr.analysis.workspace.criterion import (
    cable_length as _cable_length,
    interference as _interference,
    singularities as _singularities,
    wrench_closure as _wrench_closure,
    wrench_feasible as _wrench_feasible,
)

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"

CABLE_LENGTH = _cable_length.CableLength
INTERFERENCE = _interference.Interference
SINGULARITIES = _singularities.Singularities
WRENCH_CLOSURE = _wrench_closure.WrenchClosure
WRENCH_FEASIBLE = _wrench_feasible.WrenchFeasible

__all__ = [
    'CABLE_LENGTH',
    'INTERFERENCE',
    'SINGULARITIES',
    'WRENCH_CLOSURE',
    'WRENCH_FEASIBLE',
]

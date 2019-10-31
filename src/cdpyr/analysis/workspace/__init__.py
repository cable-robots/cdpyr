from cdpyr.analysis.workspace import (
    archetype,
    criterion,
    grid as _grid,
    hull as _hull,
)

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"

GRID = _grid.Calculator
HULL = _hull.Calculator

GRID_RESULT = _grid.Result
HULL_RESULT = _hull.Result

__all__ = [
    'archetype',
    'criterion',
    'GRID',
    'HULL',
    'GRID_RESULT',
    'HULL_RESULT',
]

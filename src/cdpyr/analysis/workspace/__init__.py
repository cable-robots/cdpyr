__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"
__all__ = [
        'grid',
        'hull',
        'Hull',
        'HullResult',
        'Grid',
        'GridResult',
]

from cdpyr.analysis.workspace import grid, hull
from cdpyr.analysis.workspace.grid import (
    Algorithm as Grid,
    Result as GridResult,
)
from cdpyr.analysis.workspace.hull import (
    Algorithm as Hull,
    Result as HullResult,
)

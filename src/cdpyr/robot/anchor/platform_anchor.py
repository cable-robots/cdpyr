from typing import Sequence

from magic_repr import make_repr

from cdpyr.robot.anchor import anchor as _anchor

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"


class PlatformAnchor(_anchor.Anchor):

    def __init__(self,
                 *args,
                 **kwargs):
        _anchor.Anchor.__init__(self, *args, **kwargs)


    __repr__ = make_repr(
        'position',
        'dcm'
    )


class PlatformAnchorList(_anchor.AnchorList):
    data: Sequence[PlatformAnchor]

    pass

__all__ = [
    'PlatformAnchor',
    'PlatformAnchorList',
]

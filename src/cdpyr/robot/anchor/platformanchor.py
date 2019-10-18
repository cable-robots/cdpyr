from typing import Sequence

from magic_repr import make_repr

from cdpyr.robot.anchor import anchor as _anchor


class PlatformAnchor(_anchor.Anchor):

    def __init__(self,
                 *args,
                 **kwargs):
        _anchor.Anchor.__init__(self, *args, **kwargs)


PlatformAnchor.__repr__ = make_repr(
    'position',
    'dcm'
)


class PlatformAnchorList(_anchor.AnchorList):
    data: Sequence[PlatformAnchor]

    pass


__all__ = [
    'PlatformAnchor',
    'PlatformAnchorList',
    # 'PlatformAnchorSchema',
]

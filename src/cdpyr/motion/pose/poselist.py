from collections import UserList
import prettyprinter


class PoseList(UserList):
    pass
    # def __init__(self, *args, **kwargs):
    #     prettyprinter.cpprint(args)
    #     prettyprinter.cpprint(kwargs)

__all__ = [
    'PoseList',
]

from cdpyr.components.anchor import Anchor
from cdpyr.components.cable import Cable
from cdpyr.components.platform import Platform


class Connectivity(object):
    _cable: Cable
    _frame: Anchor
    _platform: Platform

    def __init__(self):
        pass

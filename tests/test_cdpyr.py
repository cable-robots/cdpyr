from __future__ import annotations

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"

def test_cdpyr():
    import cdpyr

    r = cdpyr.robot.Robot()

    assert r.name == 'default'

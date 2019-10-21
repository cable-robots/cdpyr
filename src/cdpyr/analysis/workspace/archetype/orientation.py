import numpy as np_
from scipy.spatial import transform as _transform

from cdpyr.motion.pose import generator as _generator, pose as _pose

comparator = all


def poses(archetype, coordinate):
    # start pose contains the minimum rotation
    start = _pose.Pose((
        archetype.position,
        _transform.Rotation.from_euler(
            'xyz',
            np_.pi * np_.asarray((-1.0, -1.0, -1.0))
        ).as_dcm()
    ))
    # end pose contains the maximum rotation
    end = _pose.Pose((
        archetype.position,
        _transform.Rotation.from_euler(
            'xyz',
            np_.pi * np_.asarray((1.0, 1.0, 1.0))
        ).as_dcm()
    ))

    # and return the generator
    return _generator.steps(start, end, archetype.step)

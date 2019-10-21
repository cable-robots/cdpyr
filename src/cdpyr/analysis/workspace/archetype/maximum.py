import numpy as np_
from scipy.spatial import transform as _transform

from cdpyr.motion.pose import generator as _generator, pose as _pose

comparator = any


def poses(archetype, coordinate):
    euler = np_.pi * np_.asarray([1, 1, 1])
    # and return the generator
    return _generator.steps(_pose.Pose(
        (coordinate, _transform.Rotation.from_euler('zyx', -euler).as_dcm())),
        _pose.Pose((coordinate,
                    _transform.Rotation.from_euler('zyx',
                                                   +euler).as_dcm())),
        1)

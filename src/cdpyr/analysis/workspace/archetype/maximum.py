import numpy as np_
from scipy.spatial import transform as _transform

from cdpyr.motion.pose import generator as _generator, pose as _pose

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"
comparator = any


def poses(archetype, coordinate):
    # extrinsic rotation of 180° about [x, y, z]
    euler = np_.pi * np_.asarray([1, 1, 1])
    # and return the generator
    return _generator.steps(_pose.Pose(
        (coordinate, _transform.Rotation.from_euler('xyz', -euler).as_dcm())),
        _pose.Pose((coordinate,
                    _transform.Rotation.from_euler('xyz',
                                                   +euler).as_dcm())),
        1)

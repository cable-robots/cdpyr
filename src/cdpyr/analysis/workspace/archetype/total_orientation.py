from scipy.spatial import transform as _transform

from cdpyr.motion.pose import generator as _generator, pose as _pose

comparator = all


def poses(archetype, coordinate):
    # and return the generator
    return _generator.steps(_pose.Pose((coordinate,
                                        _transform.Rotation.from_euler(
                                            archetype.sequence,
                                            archetype.euler_min).as_dcm())),
                            _pose.Pose((coordinate,
                                        _transform.Rotation.from_euler(
                                            archetype.sequence,
                                            archetype.euler_max).as_dcm())),
                            1)

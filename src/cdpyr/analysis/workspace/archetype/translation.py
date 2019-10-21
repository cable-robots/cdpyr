from cdpyr.analysis.workspace.archetype import archetype as _archetype
from cdpyr.motion.pose import generator as _generator, pose as _pose
from cdpyr.typing import Vector

comparator = all


def poses(archetype: '_archetype.Archetype', coordinate: Vector):
    # and return the generator
    return _generator.steps(_pose.Pose((coordinate, archetype.dcm)),
                            _pose.Pose((coordinate, archetype.dcm)),
                            1)

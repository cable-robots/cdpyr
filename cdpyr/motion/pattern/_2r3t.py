from cdpyr.motion.pattern.motionpatternbase import MotionpatternBase


class _2R3T(MotionpatternBase):
    _human: str = '2R3T'
    _translational: int = 3
    _rotational: int = 2

    def structure_matrix(self):
        raise NotImplementedError()

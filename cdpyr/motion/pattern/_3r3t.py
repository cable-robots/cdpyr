from cdpyr.motion.pattern.motionpatternbase import MotionpatternBase


class _3R3T(MotionpatternBase):
    _human: str = '3R3T'
    _translational: int = 3
    _rotational: int = 3

    def structure_matrix(self):
        raise NotImplementedError()

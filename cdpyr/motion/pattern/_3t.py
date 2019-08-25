from cdpyr.motion.pattern.motionpatternbase import MotionpatternBase


class _3T(MotionpatternBase):
    _human: str = '3T'
    _translational: int = 3
    _rotational: int = 0

    def structure_matrix(self):
        raise NotImplementedError()

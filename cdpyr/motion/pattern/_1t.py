from cdpyr.motion.pattern.motionpatternbase import MotionpatternBase


class _1T(MotionpatternBase):
    _human: str = '1T'
    _translational: int = 1
    _rotational: int = 0

    def structure_matrix(self):
        raise NotImplementedError()

from cdpyr.motion.pattern.motionpatternbase import MotionpatternBase


class _1R2T(MotionpatternBase):
    _human: str = '1R2T'
    _translational: int = 2
    _rotational: int = 1

    def structure_matrix(self):
        raise NotImplementedError()

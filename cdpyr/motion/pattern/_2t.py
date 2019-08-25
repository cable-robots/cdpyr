from cdpyr.motion.pattern.motionpatternbase import MotionpatternBase


class _2T(MotionpatternBase):
    _human: str = '2T'
    _translational: int = 2
    _rotational: int = 0

    def structure_matrix(self):
        raise NotImplementedError()

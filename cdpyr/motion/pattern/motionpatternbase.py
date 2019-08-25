from abc import ABC

from magic_repr import make_repr


class MotionpatternBase(ABC):
    _human: str = NotImplementedError()
    _translational: int = NotImplementedError()
    _rotational: int = NotImplementedError()

    def structure_matrix(self):
        raise NotImplementedError()

    @property
    def human(self):
        return self._human

    @human.setter
    def human(self, human: str):
        self._human = human

    @human.deleter
    def human(self):
        del self._human

    @property
    def translation(self):
        return self._translation

    @translation.setter
    def translation(self, translation: int):
        if not 1 <= translation <= 3:
            raise ValueError(
                'translation must be between 1 and 3, was {}'.format(
                    translation))

        self._translation = translation

    @translation.deleter
    def translation(self):
        del self._translation

    @property
    def rotation(self):
        return self._rotation

    @rotation.setter
    def rotation(self, rotation: int):
        if not 0 <= rotation <= 3:
            raise ValueError(
                'rotation must be between 0 and 3, was {}'.format(rotation))

        self._rotation = rotation

    @rotation.deleter
    def rotation(self):
        del self._rotation


MotionpatternBase.__repr__ = make_repr(
    'translation',
    'rotation',
    'human',
)

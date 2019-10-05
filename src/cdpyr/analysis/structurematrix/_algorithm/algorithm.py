import abc


class Algorithm(abc.ABC):

    @staticmethod
    @abc.abstractmethod
    def _calculate(*args, **kwargs):
        raise NotImplementedError()

    def __call__(self, *args, **kwargs):
        return self._calculate(*args, **kwargs)

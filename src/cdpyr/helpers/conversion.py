from __future__ import annotations

from itertools import chain
from operator import attrgetter

from six import moves

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"


def converter(*args, **kwargs):
    def method(self):
        # get factory method
        factory = kwargs.pop('factory')
        # create result as a key-ed object or not
        is_keyed = kwargs.pop('keyed', True)

        if args:
            field_names = args
        elif len(kwargs):
            field_names = []
        else:
            def undercored(name):
                return name.startswith('_')

            def is_method(name):
                return callable(getattr(self, name))

            def good_name(name):
                return not undercored(name) and not is_method(name)

            field_names = filter(good_name, dir(self))
            field_names = sorted(field_names)

        # on this stage, we make from field_names an
        # attribute getters
        field_getters = moves.zip(field_names,
                                  map(attrgetter, field_names))

        # now process keyword args, they must
        # contain callables of one argument
        # and callable should return a field's value
        field_getters = chain(
                field_getters,
                kwargs.items())

        fields = ((name, getter(self)) for name, getter in field_getters)

        return factory((k, v) for k, v in fields) if is_keyed else factory(v for _, v in fields)

    return method


def make_dict(*args, **kwargs):
    return converter(*args, **{'factory': dict, **kwargs}, keyed=True)


def make_tuple(*args, **kwargs):
    return converter(*args, **{'factory': tuple, **kwargs}, keyed=False)


__all__ = [
        'make_dict',
        'make_tuple',
]

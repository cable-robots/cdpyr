from typing import AnyStr, IO, Union

from cdpyr.stream.parser import parser as _parser

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"


class Stream(object):
    _parser: '_parser.Parser'

    def __init__(self, parser: '_parser.Parser'):
        self.parser = parser

    @property
    def parser(self):
        return self._parser

    @parser.setter
    def parser(self, parser: '_parser.Parser'):
        self._parser = parser

    @parser.deleter
    def parser(self):
        del self._parser

    def encode(self, o: object, f: Union[AnyStr, IO], *args, **kwargs):
        """

        :type o: object Any object that is supposed to be encoded
        :type f: IO File-like object to dump encoded object to
        """
        # first, we will encode the object into a string
        s = self.encodes(o, *args, **kwargs)

        try:
            bytes_written = f.write(s)
        except AttributeError:
            with open(f, 'w') as f_:
                bytes_written = f_.write(s)
        finally:
            return bytes_written > 0

    def decode(self, f: Union[AnyStr, IO], *args, **kwargs):
        """

        :type f: IO File-like object to read and decode data from
        """
        try:
            s = f.readlines()
        except AttributeError:
            with open(f, 'r') as f_:
                s = f_.readlines()
        finally:
            return self.decodes('\n'.join(s), *args, **kwargs)

    def encodes(self, o: object, *args, **kwargs):
        """

        :type o: object Any object that is supposed to be encoded
        """
        return self.parser.encode(o, *args, **kwargs)

    def decodes(self, s: AnyStr, *args, **kwargs):
        """

        :type s: AnyStr A string representing the encoded object
        """
        return self.parser.decode(s, *args, **kwargs)

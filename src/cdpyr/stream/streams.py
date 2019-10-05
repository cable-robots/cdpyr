from typing import IO, Union

from cdpyr.stream.parser.parser import Parser


class Stream(object):
    _parser: Parser

    def __init__(self, parser: Union[str, Parser]):
        self.parser = parser

    @property
    def parser(self):
        return self._parser

    @parser.setter
    def parser(self, parser: Parser):
        self._parser = parser

    @parser.deleter
    def parser(self):
        del self._parser

    def encode(self, o: object, f: IO, *args, **kwargs):
        """

        :type o: object Any object that is supposed to be encoded
        :type f: IO File-like object to dump encoded object to
        """
        # first, we will encode the object into a string
        s = self.encodes(o, *args, **kwargs)

        # then we can write this to a file
        f.write(s)

    def decode(self, f: IO, *args, **kwargs):
        """

        :type f: IO File-like object to read and decode data from
        """
        # first, read the file and get its content
        s = f.readlines()
        # and convert the array of lines into a single string
        s = '\n'.join(s)

        # now we can simply decode the string and return the result
        return self.decodes(s, *args, **kwargs)

    def encodes(self, o: object, *args, **kwargs):
        """

        :type o: object Any object that is supposed to be encoded
        """
        return self.parser.encode(o, *args, **kwargs)

    def decodes(self, s: str, *args, **kwargs):
        """

        :type s: str A string representing the encoded object
        """
        return self.parser.decode(s, *args, **kwargs)

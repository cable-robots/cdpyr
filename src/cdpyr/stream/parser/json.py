from __future__ import annotations

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"
__all__ = [
        'Json',
]

import json
from collections import OrderedDict
from typing import AnyStr, Mapping, Union

from cdpyr.stream.parser import parser as _parser


class Json(_parser.Parser):
    EXT = 'json'

    def dumps(self, d: Union[OrderedDict, Mapping], *args, **kwargs) -> AnyStr:
        return json.dumps(d, indent=2, **kwargs)

    def loads(self, s: AnyStr, *args, **kwargs) -> Union[OrderedDict, Mapping]:
        return json.loads(s, **kwargs)

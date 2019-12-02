import json
from collections import OrderedDict
from typing import AnyStr, Union

from cdpyr.stream.parser import parser as _parser


class Json(_parser.Parser):

    def dumps(self, d: Union[OrderedDict, dict], *args, **kwargs) -> AnyStr:
        return json.dumps(d, indent=2, **kwargs)

    def loads(self, s: AnyStr, *args, **kwargs) -> Union[OrderedDict, dict]:
        return json.loads(s, **kwargs)

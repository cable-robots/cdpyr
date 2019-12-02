from collections import OrderedDict
from typing import AnyStr, Union

import yaml

from cdpyr.stream.parser import parser as _parser


class Yaml(_parser.Parser):

    def dumps(self, d: Union[OrderedDict, dict], *args, **kwargs) -> AnyStr:
        return yaml.dump(d, **kwargs)

    def loads(self, s: AnyStr, *args, **kwargs) -> Union[OrderedDict, dict]:
        return yaml.load(s, **kwargs)

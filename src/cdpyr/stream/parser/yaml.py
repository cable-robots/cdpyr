from collections import OrderedDict
from typing import AnyStr, Union, Mapping

import yaml

from cdpyr.stream.parser import parser as _parser


def ordered_dict_representer(dumper, data):
    return dumper.represent_dict(data.items())


def ordered_dict_constructor(loader, node):
    return OrderedDict(loader.construct_pairs(node))


_mapping_tag = yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG

yaml.Dumper.add_representer(OrderedDict, ordered_dict_representer)
yaml.Loader.add_constructor(_mapping_tag, ordered_dict_constructor)


class Yaml(_parser.Parser):

    def dumps(self, d: Union[OrderedDict, Mapping], *args, **kwargs) -> AnyStr:
        return yaml.dump(d, **kwargs)

    def loads(self, s: AnyStr, *args, **kwargs) -> Union[OrderedDict, Mapping]:
        return yaml.load(s, **kwargs)

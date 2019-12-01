from collections import OrderedDict
from typing import (
    AnyStr,
    Sequence,
    Tuple,
    Union
)

import xmltodict

from cdpyr.robot.robot_component import RobotComponent
from cdpyr.stream.parser import parser as _parser


class Xml(_parser.Parser):

    def kwargs(self, o: RobotComponent, **kwargs):
        return super().kwargs(o, root=o.__class__.__name__.lower(), **kwargs)

    def dumps(self, d: Union[OrderedDict, dict],
              *args,
              **kwargs) -> AnyStr:
        return xmltodict.unparse({kwargs.get('root', 'root'): d}, pretty=True)

    def loads(self, s: AnyStr, *args, **kwargs) -> Union[OrderedDict, dict]:
        # first, parse from XML to dictionary
        d = xmltodict.parse(s, force_list=('dcm'), postprocessor=self._postprocessing)
        # then, since there always must be a root object in XML, we will
        # strip this off the dictionary from here
        return d[list(d.keys())[0]]

    def _postprocessing(self, path: Sequence[Tuple[AnyStr, object]], key: str,
                        value):
        """
        Convert list of strings into list of lists (or at least try to convert)

        Parameters
        ----------
        path
        key
        value

        Returns
        -------

        """
        # first, see if the value seems to be a concatenation of numeric values
        # new_value = value
        # if ',' in new_value:
        #     new_value = new_value.split(',')

        if value is not None and (
            ',' in value or isinstance(value, Sequence) and not isinstance(
            value, str)):
            if ',' in value:
                value = value.split(',')
            try:
                new_value = [float(s.strip('()')) for s in value]
            except AttributeError:
                new_value = value
        else:
            try:
                # strip parantheses from the string and convert it to a float
                new_value = float(value.strip('()'))
            except Exception as e:
                new_value = value

        return key, new_value

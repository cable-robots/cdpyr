from typing import AnyStr, Sequence

from cdpyr.stream.parser.parser import Parser


class JSON(Parser):

    def encode(self, obj: object, *args, **kwargs) -> Sequence[AnyStr]:
        pass

    def decode(self, stream: AnyStr, *args, **kwargs) -> object:
        pass

# class RobotEncoder(json.JSONEncoder):
#
#     def default(self, obj):
#         from cdpyr import robot
#
#         if isinstance(obj, robot.Robot):
#             return [obj.real, obj.imag]
#         # Let the base class default method raise the TypeError
#         return json.JSONEncoder.default(self, obj)

from typing import List
import xmltodict
from prettyprinter import cpprint
import numpy as np
import collections
import json


class Anchor(collections.UserDict):

    def __init__(self, position, orientation):
        collections.UserDict.__init__(self)
        self['position'] = position
        self['orientation'] = orientation


class Inertia(collections.UserDict):

    def __init__(self, linear, angular):
        collections.UserDict.__init__(self)
        self['linear'] = linear
        self['angular'] = angular


class Pulley(collections.UserDict):

    def __init__(self, radius, inertia: Inertia, orientation):
        collections.UserDict.__init__(self)
        self['radius'] = radius
        self['inertia'] = inertia
        self['orientation'] = orientation


class Winch(collections.UserDict):
    def __init__(self, radius, inertia: Inertia):
        collections.UserDict.__init__(self)
        self['radius'] = radius
        self['inertia'] = inertia


class Gearbox(collections.UserDict):
    def __init__(self, ratio, inertia: Inertia):
        collections.UserDict.__init__(self)
        self['ratio'] = ratio
        self['inertia'] = inertia


class Motor(collections.UserDict):
    def __init__(self, torques, inertia: Inertia):
        collections.UserDict.__init__(self)
        self['torques'] = torques
        self['inertia'] = inertia


class Drivetrain(collections.UserDict):
    def __init__(self, winch: Winch, gearbox: Gearbox, motor: Motor):
        collections.UserDict.__init__(self)
        self['winch'] = winch
        self['gearbox'] = gearbox
        self['motor'] = motor


class FrameAnchor(Anchor):
    def __init__(self, position, orientation, pulley: Pulley,
                 drivetrain: Drivetrain):
        collections.UserDict.__init__(self)
        Anchor.__init__(self, position=position, orientation=orientation)
        self['pulley'] = pulley
        self['drivetrain'] = drivetrain


class PlatformAnchor(Anchor):
    def __init__(self, position, orientation):
        collections.UserDict.__init__(self)
        Anchor.__init__(self, position=position, orientation=orientation)


class Frame(collections.UserDict):
    def __init__(self, anchors: List[FrameAnchor]):
        collections.UserDict.__init__(self)
        self['anchors'] = anchors


class Platform(collections.UserDict):

    def __init__(self, anchors: List[PlatformAnchor], inertia: Inertia):
        collections.UserDict.__init__(self)
        self['anchors'] = anchors
        self['inertia'] = inertia


class Cable(collections.UserDict):

    def __init__(self, diameter):
        collections.UserDict.__init__(self)
        self['diameter'] = diameter
        self['name'] = 'default'
        self['breaking_load'] = 10000
        self['color'] = 'red'


class Chain(collections.UserDict):
    def __init__(self, frame, platform, anchor, cable):
        collections.UserDict.__init__(self)
        self['frame'] = frame
        self['platform'] = platform
        self['anchor'] = anchor
        self['cable'] = cable


class Robot(collections.UserDict):

    def __init__(self, frame: Frame, platforms: List[Platform], cables:
    List[Cable], chains: List[Chain]):
        collections.UserDict.__init__(self)
        self['frame'] = frame
        self['platforms'] = platforms
        self['chains'] = chains
        self['cables'] = cables


class CDPRJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, collections.UserDict):
            return dict(o)
        elif isinstance(o, np.ndarray):
            return list(o)
        else: # Let the base class default method raise the TypeError
            return json.JSONEncoder.default(self, o)

# class CDPRJSONDecoder(json.JSONDecoder):
#     def default(self, o):
#         return json.JSONDecoder.defaul


class Thing(object):
    def __init__(self, name):
        self.name = name


def create_robot():
    r = Robot(
        frame=Frame(
            anchors=[
                FrameAnchor(
                    position=np.random.rand(3)
                    , orientation=np.eye(3)
                    , pulley=Pulley(
                        radius=0.10
                        , inertia=Inertia(
                            linear=np.random.random()
                            , angular=np.random.rand(3, 3)
                        )
                        , orientation=np.eye(3)
                    )
                    , drivetrain=Drivetrain(
                        winch=Winch(
                            radius=0.50
                            , inertia=Inertia(
                                linear=np.random.random()
                                , angular=np.random.rand(3, 3)
                            )
                        )
                        , gearbox=Gearbox(
                            ratio=5.00
                            , inertia=Inertia(
                            linear=np.random.random()
                            , angular=np.random.rand(3, 3)
                        )
                        )
                        , motor=Motor(
                            torques={'max': 12, 'nominal': 10, 'rated': 8}
                            , inertia=Inertia(
                            linear=np.random.random()
                            , angular=np.random.rand(3, 3)
                        )
                        )
                    )
                ) for idx_ in range(0, 8)
            ]
        )
        , platforms=[
            Platform(
                anchors=[
                    PlatformAnchor(
                        position=np.random.rand(3),
                        orientation=np.eye(3)
                    ) for idx_ in range(0, 8)
                ]
                , inertia=Inertia(
                    linear=np.random.random()
                    , angular=np.random.rand(3, 3)
                )
            ) for idx in range(0, 3)
        ]
        , cables=[
            Cable(
                diameter=6.0 / 1000
            ) for idx in range(0, 3 * 8)
        ]
        , chains=[
            Chain(
                frame=idx
                , platform=idx % 8
                , anchor=idx % 3
                , cable=idx
            ) for idx in range(0, 3 * 8)
        ]
    )

    return r

if __name__ == "__main__":
    r = create_robot()
    cpprint(dict(r))
    with open('cdpr.json', 'w') as fp:
        json.dump(dict(r), fp, cls=CDPRJSONEncoder, indent=2)
        # cpprint(j)
    # x = xmltodict.unparse(dict(r), full_document=False)
    # xmltodict.parse(x)
    # print(x)
    # with open('asd.xml', 'w') as f:
    #     f.write(x)
    # print(r['frame']['anchors'][0]['orientation'])

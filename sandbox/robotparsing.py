import xmltodict
from prettyprinter import cpprint

def sample_position(idx, scale=None):
    if scale is None:
        scale = 1.00

    return {
        'x': -scale if (idx - 1) % 4 in [0, 3] else scale,
        'y': -scale if (idx - 1) % 4 in [2, 3] else scale,
        'z': -scale if (idx - 1) >= 4 else scale,
    }


def sample_frame_anchor(idx, drivetrain):
    return {
        'position': sample_position(idx, scale=1.00)
        , 'orientation': sample_orientation()
        , 'pulley': {
            'orientation': sample_orientation(),
            'radius': 0.1,
            'inertia': sample_inertia(),
        }
        , 'drivetrain': sample_drivetrain()
    }


def sample_platform_anchor(idx):
    return {
        'position': sample_position(idx, scale=0.30),
        'orientation': sample_orientation(),
    }


def sample_linkage(idx):
    return {
        'position': sample_position(idx, scale=0.10)
        , 'type': 'revolute'
    }


def sample_platform(idx, parent):
    return {
        'dof_linear': 3,
        'dof_angular': 3,
        'anchors': [
            sample_platform_anchor(1)
            , sample_platform_anchor(2)
            , sample_platform_anchor(3)
            , sample_platform_anchor(4)
            , sample_platform_anchor(5)
            , sample_platform_anchor(6)
            , sample_platform_anchor(7)
            , sample_platform_anchor(8)
        ],
        'linkages': [
            sample_linkage(1)
        ],
        'connection': {
            'parent': parent,
            'offset': sample_position(parent, scale=0.75),
        },
    }


def sample_drivetrain():
    return {
        'winch': {
            'radius': 0.1
            , 'inertia': sample_inertia()
        }
        , 'gearbox': {
            'ratio': 12
            , 'inertia': sample_inertia()
        }
        , 'motor': {
            'torque': {
                'rated': 12
                , 'max': 15
            }
            , 'inertia': 10
        }
    }


def sample_cable():
    return {
        'type': 'default'
        , 'breaking_load': 10000.0
        , 'diameter': 0.006
        , 'color': 'red'
    }


def sample_chain(frame, platform, anchor, cable):
    return {
        'frame': frame,
        'platform': platform,
        'anchor': anchor,
        'cable': cable,
    }


def sample_orientation():
    return {
        'R11': 1.00,
        'R12': 0.00,
        'R13': 0.00,
        'R21': 0.00,
        'R22': 1.00,
        'R23': 0.00,
        'R31': 0.00,
        'R32': 0.00,
        'R33': 1.00,
    }


def sample_inertia():
    return {
        'linear': 0.50,
        'angular': {
            'J11': 1.00,
            'J12': 0.00,
            'J13': 0.00,
            'J21': 0.00,
            'J22': 1.00,
            'J23': 0.00,
            'J31': 0.00,
            'J32': 0.00,
            'J33': 1.00,
        }
    }


def sample_robot():
    r = {
        'name': 'default'
        , 'version': 1.0
        , 'anchors': [
            sample_frame_anchor(1, 1)
            , sample_frame_anchor(2, 2)
            , sample_frame_anchor(3, 3)
            , sample_frame_anchor(4, 4)
            , sample_frame_anchor(5, 5)
            , sample_frame_anchor(6, 6)
            , sample_frame_anchor(7, 7)
            , sample_frame_anchor(8, 8)
        ]
        , 'platforms': [
            sample_platform(1, parent=0)
            , sample_platform(2, parent=1)
            , sample_platform(3, parent=2)
        ]
        , 'cables': [
            sample_cable()
            , sample_cable()
            , sample_cable()
            , sample_cable()
            , sample_cable()
            , sample_cable()
            , sample_cable()
            , sample_cable()
        ]
        , 'chains': [
            sample_chain(frame=1, platform=1, anchor=1, cable=1)
            , sample_chain(frame=2, platform=1, anchor=2, cable=2)
            , sample_chain(frame=3, platform=1, anchor=3, cable=3)
            , sample_chain(frame=4, platform=1, anchor=4, cable=4)
            , sample_chain(frame=5, platform=2, anchor=1, cable=5)
            , sample_chain(frame=6, platform=2, anchor=2, cable=6)
            , sample_chain(frame=7, platform=2, anchor=3, cable=7)
            , sample_chain(frame=8, platform=2, anchor=4, cable=8)
            , sample_chain(frame=9, platform=3, anchor=1, cable=9)
            , sample_chain(frame=10, platform=3, anchor=2, cable=10)
            , sample_chain(frame=11, platform=3, anchor=3, cable=11)
            , sample_chain(frame=12, platform=3, anchor=4, cable=12)
        ]
    }

    return r


def robot2xml(r):
    return xmltodict.unparse({'robot': r}, pretty=True)


def xml2robot(x):
    return xmltodict.parse(x)


if __name__ == "__main__":
    r = sample_robot()
    cpprint(r)
    xml = robot2xml(r)
    print(xml)
    r = xml2robot(xml)

import numpy as np
import pytest
from scipy.spatial.transform import Rotation

import cdpyr

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"


@pytest.fixture
def robot_1t():
    return cdpyr.robot.Robot(
        name="Sample 1T robot",
        frame=cdpyr.robot.Frame(
            anchors=[
                cdpyr.robot.FrameAnchor(
                    position=[-1., 0., 0.],
                ),
                cdpyr.robot.FrameAnchor(
                    position=[1., 0., 0.],
                ),
            ]
        ),
        platforms=[
            cdpyr.robot.Platform(
                motion_pattern=cdpyr.motion.pattern.MP_1T,
                anchors=[
                    cdpyr.robot.PlatformAnchor(
                        position=[0., 0., 0.],
                    ),
                    cdpyr.robot.PlatformAnchor(
                        position=[0., 0., 0.],
                    )
                ]
            ),
        ],
        cables=[
            cdpyr.robot.Cable(
                name="Dyneema",
                material="Liros D-Pro SK78",
                diameter=6 / 1000,
                color="red"
            ),
            cdpyr.robot.Cable(
                name="Dyneema",
                material="Liros D-Pro SK78",
                diameter=6 / 1000,
                color="red"
            ),
        ],
        kinematic_chains=[
            {
                'frame_anchor':    0,
                'platform':        0,
                'platform_anchor': 0,
                'cable':           0
            },
            {
                'frame_anchor':    1,
                'platform':        0,
                'platform_anchor': 1,
                'cable':           1
            },
        ],
    )


@pytest.fixture
def robot_2t():
    return cdpyr.robot.Robot(
        name="Sample 2T robot",
        frame=cdpyr.robot.Frame(
            anchors=[
                cdpyr.robot.FrameAnchor(
                    position=[-1., 1., 0.],
                ),
                cdpyr.robot.FrameAnchor(
                    position=[1., 1., 0.],
                ),
                cdpyr.robot.FrameAnchor(
                    position=[0., -1., 0.],
                ),
            ]
        ),
        platforms=[
            cdpyr.robot.Platform(
                motion_pattern=cdpyr.motion.pattern.MP_2T,
                anchors=[
                    cdpyr.robot.PlatformAnchor(
                        position=[0., 0., 0.],
                    ),
                    cdpyr.robot.PlatformAnchor(
                        position=[0., 0., 0.],
                    ),
                    cdpyr.robot.PlatformAnchor(
                        position=[0., 0., 0.],
                    ),
                ]
            ),
        ],
        cables=[
            cdpyr.robot.Cable(
                name="Dyneema",
                material="Liros D-Pro SK78",
                diameter=6 / 1000,
                color="red"
            ),
            cdpyr.robot.Cable(
                name="Dyneema",
                material="Liros D-Pro SK78",
                diameter=6 / 1000,
                color="red"
            ),
            cdpyr.robot.Cable(
                name="Dyneema",
                material="Liros D-Pro SK78",
                diameter=6 / 1000,
                color="red"
            ),
        ],
        kinematic_chains=[
            {
                'frame_anchor':    0,
                'platform':        0,
                'platform_anchor': 0,
                'cable':           0
            },
            {
                'frame_anchor':    1,
                'platform':        0,
                'platform_anchor': 1,
                'cable':           1
            },
            {
                'frame_anchor':    2,
                'platform':        0,
                'platform_anchor': 2,
                'cable':           2
            },
        ],
    )


@pytest.fixture
def robot_3t():
    return cdpyr.robot.Robot(
        name="Sample 3T robot",
        frame=cdpyr.robot.Frame(
            anchors=[
                cdpyr.robot.FrameAnchor(
                    position=[-1., 1., 1.],
                ),
                cdpyr.robot.FrameAnchor(
                    position=[1., 1., 1.],
                ),
                cdpyr.robot.FrameAnchor(
                    position=[0., -1., 1.],
                ),
            ]
        ),
        platforms=[
            cdpyr.robot.Platform(
                motion_pattern=cdpyr.motion.pattern.MP_3T,
                anchors=[
                    cdpyr.robot.PlatformAnchor(
                        position=[0., 0., 0.],
                    ),
                    cdpyr.robot.PlatformAnchor(
                        position=[0., 0., 0.],
                    ),
                    cdpyr.robot.PlatformAnchor(
                        position=[0., 0., 0.],
                    ),
                ]
            ),
        ],
        cables=[
            cdpyr.robot.Cable(
                name="Dyneema",
                material="Liros D-Pro SK78",
                diameter=6 / 1000,
                color="red"
            ),
            cdpyr.robot.Cable(
                name="Dyneema",
                material="Liros D-Pro SK78",
                diameter=6 / 1000,
                color="red"
            ),
            cdpyr.robot.Cable(
                name="Dyneema",
                material="Liros D-Pro SK78",
                diameter=6 / 1000,
                color="red"
            ),
        ],
        kinematic_chains=[
            {
                'frame_anchor':    0,
                'platform':        0,
                'platform_anchor': 0,
                'cable':           0
            },
            {
                'frame_anchor':    1,
                'platform':        0,
                'platform_anchor': 1,
                'cable':           1
            },
            {
                'frame_anchor':    2,
                'platform':        0,
                'platform_anchor': 2,
                'cable':           2
            },
        ],
    )


@pytest.fixture
def robot_1r2t():
    return cdpyr.robot.Robot(
        name="Sample 1R2T robot",
        frame=cdpyr.robot.Frame(
            anchors=[
                cdpyr.robot.FrameAnchor(
                    position=[-1., 1., 0.],
                ),
                cdpyr.robot.FrameAnchor(
                    position=[1., 1., 0.],
                ),
                cdpyr.robot.FrameAnchor(
                    position=[1., -1., 0.],
                ),
                cdpyr.robot.FrameAnchor(
                    position=[-1., -1., 0.],
                ),
            ]
        ),
        platforms=[
            cdpyr.robot.Platform(
                motion_pattern=cdpyr.motion.pattern.MP_1R2T,
                anchors=[
                    cdpyr.robot.PlatformAnchor(
                        position=[-0.1, 0.1, 0.],
                    ),
                    cdpyr.robot.PlatformAnchor(
                        position=[0.1, 0.1, 0.],
                    ),
                    cdpyr.robot.PlatformAnchor(
                        position=[0.1, -0.1, 0.],
                    ),
                    cdpyr.robot.PlatformAnchor(
                        position=[-0.1, -0.1, 0.],
                    ),
                ],
            ),
        ],
        cables=[
            cdpyr.robot.Cable(
                name="Dyneema",
                material="Liros D-Pro SK78",
                diameter=6 / 1000,
                color="red"
            ),
            cdpyr.robot.Cable(
                name="Dyneema",
                material="Liros D-Pro SK78",
                diameter=6 / 1000,
                color="red"
            ),
            cdpyr.robot.Cable(
                name="Dyneema",
                material="Liros D-Pro SK78",
                diameter=6 / 1000,
                color="red"
            ),
            cdpyr.robot.Cable(
                name="Dyneema",
                material="Liros D-Pro SK78",
                diameter=6 / 1000,
                color="red"
            ),
        ],
        kinematic_chains=[
            {
                'frame_anchor':    0,
                'platform':        0,
                'platform_anchor': 0,
                'cable':           0
            },
            {
                'frame_anchor':    1,
                'platform':        0,
                'platform_anchor': 1,
                'cable':           1
            },
            {
                'frame_anchor':    2,
                'platform':        0,
                'platform_anchor': 2,
                'cable':           2
            },
            {
                'frame_anchor':    3,
                'platform':        0,
                'platform_anchor': 3,
                'cable':           3
            },
        ],
    )


@pytest.fixture
def robot_2r3t():
    return cdpyr.robot.Robot(
        name="Sample 2R3T robot",
        frame=cdpyr.robot.Frame(
            anchors=[
                cdpyr.robot.FrameAnchor(
                    position=[-1.0, 1.0, 1.0]
                ),
                cdpyr.robot.FrameAnchor(
                    position=[1.0, 1.0, 1.0]
                ),
                cdpyr.robot.FrameAnchor(
                    position=[1.0, -1.0, 1.0]
                ),
                cdpyr.robot.FrameAnchor(
                    position=[-1.0, -1.0, 1.0]
                ),
                cdpyr.robot.FrameAnchor(
                    position=[-1.0, 1.0, -1.0]
                ),
                cdpyr.robot.FrameAnchor(
                    position=[1.0, 1.0, -1.0]
                ),
                cdpyr.robot.FrameAnchor(
                    position=[1.0, -1.0, -1.0]
                ),
                cdpyr.robot.FrameAnchor(
                    position=[-1.0, -1.0, -1.0]
                ),
            ]
        ),
        platforms=[
            cdpyr.robot.Platform(
                motion_pattern=cdpyr.motion.pattern.MP_2R3T,
                anchors=[
                    cdpyr.robot.PlatformAnchor(
                        position=[-0.01, 0.01, 0.1],
                    ),
                    cdpyr.robot.PlatformAnchor(
                        position=[0.01, 0.01, 0.1],
                    ),
                    cdpyr.robot.PlatformAnchor(
                        position=[0.01, -0.01, 0.1],
                    ),
                    cdpyr.robot.PlatformAnchor(
                        position=[-0.01, -0.01, 0.1],
                    ),
                    cdpyr.robot.PlatformAnchor(
                        position=[-0.01, 0.01, -0.1],
                    ),
                    cdpyr.robot.PlatformAnchor(
                        position=[0.01, 0.01, -0.1],
                    ),
                    cdpyr.robot.PlatformAnchor(
                        position=[0.01, -0.01, -0.1],
                    ),
                    cdpyr.robot.PlatformAnchor(
                        position=[-0.01, -0.01, -0.1],
                    ),
                ]
            )
        ],
        cables=[
            cdpyr.robot.Cable(
                name="Dyneema",
                material="Liros D-Pro SK78",
                diameter=6 / 1000,
                color="red"
            ),
            cdpyr.robot.Cable(
                name="Dyneema",
                material="Liros D-Pro SK78",
                diameter=6 / 1000,
                color="red"
            ),
            cdpyr.robot.Cable(
                name="Dyneema",
                material="Liros D-Pro SK78",
                diameter=6 / 1000,
                color="red"
            ),
            cdpyr.robot.Cable(
                name="Dyneema",
                material="Liros D-Pro SK78",
                diameter=6 / 1000,
                color="red"
            ),
            cdpyr.robot.Cable(
                name="Dyneema",
                material="Liros D-Pro SK78",
                diameter=6 / 1000,
                color="red"
            ),
            cdpyr.robot.Cable(
                name="Dyneema",
                material="Liros D-Pro SK78",
                diameter=6 / 1000,
                color="red"
            ),
            cdpyr.robot.Cable(
                name="Dyneema",
                material="Liros D-Pro SK78",
                diameter=6 / 1000,
                color="red"
            ),
            cdpyr.robot.Cable(
                name="Dyneema",
                material="Liros D-Pro SK78",
                diameter=6 / 1000,
                color="red"
            ),
        ],
        kinematic_chains=[
            {
                'frame_anchor':    0,
                'platform':        0,
                'platform_anchor': 4,
                'cable':           0
            },
            {
                'frame_anchor':    1,
                'platform':        0,
                'platform_anchor': 5,
                'cable':           1
            },
            {
                'frame_anchor':    2,
                'platform':        0,
                'platform_anchor': 6,
                'cable':           2
            },
            {
                'frame_anchor':    3,
                'platform':        0,
                'platform_anchor': 7,
                'cable':           3
            },
            {
                'frame_anchor':    4,
                'platform':        0,
                'platform_anchor': 0,
                'cable':           4
            },
            {
                'frame_anchor':    5,
                'platform':        0,
                'platform_anchor': 1,
                'cable':           5
            },
            {
                'frame_anchor':    6,
                'platform':        0,
                'platform_anchor': 2,
                'cable':           6
            },
            {
                'frame_anchor':    7,
                'platform':        0,
                'platform_anchor': 3,
                'cable':           7
            },
        ],
    )


@pytest.fixture
def robot_3r3t():
    return cdpyr.robot.Robot(
        name="Sample 3R3T robot",
        frame=cdpyr.robot.Frame(
            anchors=[
                cdpyr.robot.FrameAnchor(
                    position=[-1.0, 1.0, 1.0]
                ),
                cdpyr.robot.FrameAnchor(
                    position=[1.0, 1.0, 1.0]
                ),
                cdpyr.robot.FrameAnchor(
                    position=[1.0, -1.0, 1.0]
                ),
                cdpyr.robot.FrameAnchor(
                    position=[-1.0, -1.0, 1.0]
                ),
                cdpyr.robot.FrameAnchor(
                    position=[-1.0, 1.0, -1.0]
                ),
                cdpyr.robot.FrameAnchor(
                    position=[1.0, 1.0, -1.0]
                ),
                cdpyr.robot.FrameAnchor(
                    position=[1.0, -1.0, -1.0]
                ),
                cdpyr.robot.FrameAnchor(
                    position=[-1.0, -1.0, -1.0]
                ),
            ]
        ),
        platforms=[
            cdpyr.robot.Platform(
                motion_pattern=cdpyr.motion.pattern.MP_3R3T,
                anchors=[
                    cdpyr.robot.PlatformAnchor(
                        position=[-0.1, 0.1, 0.1]
                    ),
                    cdpyr.robot.PlatformAnchor(
                        position=[0.1, 0.1, 0.1]
                    ),
                    cdpyr.robot.PlatformAnchor(
                        position=[0.1, -0.1, 0.1]
                    ),
                    cdpyr.robot.PlatformAnchor(
                        position=[-0.1, -0.1, 0.1]
                    ),
                    cdpyr.robot.PlatformAnchor(
                        position=[-0.1, 0.1, -0.1]
                    ),
                    cdpyr.robot.PlatformAnchor(
                        position=[0.1, 0.1, -0.1]
                    ),
                    cdpyr.robot.PlatformAnchor(
                        position=[0.1, -0.1, -0.1]
                    ),
                    cdpyr.robot.PlatformAnchor(
                        position=[-0.1, -0.1, -0.1]
                    ),
                ]
            )
        ],
        cables=[
            cdpyr.robot.Cable(
                name="Dyneema",
                material="Liros D-Pro SK78",
                diameter=6 / 1000,
                color="red"
            ),
            cdpyr.robot.Cable(
                name="Dyneema",
                material="Liros D-Pro SK78",
                diameter=6 / 1000,
                color="red"
            ),
            cdpyr.robot.Cable(
                name="Dyneema",
                material="Liros D-Pro SK78",
                diameter=6 / 1000,
                color="red"
            ),
            cdpyr.robot.Cable(
                name="Dyneema",
                material="Liros D-Pro SK78",
                diameter=6 / 1000,
                color="red"
            ),
            cdpyr.robot.Cable(
                name="Dyneema",
                material="Liros D-Pro SK78",
                diameter=6 / 1000,
                color="red"
            ),
            cdpyr.robot.Cable(
                name="Dyneema",
                material="Liros D-Pro SK78",
                diameter=6 / 1000,
                color="red"
            ),
            cdpyr.robot.Cable(
                name="Dyneema",
                material="Liros D-Pro SK78",
                diameter=6 / 1000,
                color="red"
            ),
            cdpyr.robot.Cable(
                name="Dyneema",
                material="Liros D-Pro SK78",
                diameter=6 / 1000,
                color="red"
            ),
        ],
        kinematic_chains=[
            {
                'frame_anchor':    0,
                'platform':        0,
                'platform_anchor': 0,
                'cable':           0
            },
            {
                'frame_anchor':    1,
                'platform':        0,
                'platform_anchor': 1,
                'cable':           1
            },
            {
                'frame_anchor':    2,
                'platform':        0,
                'platform_anchor': 2,
                'cable':           2
            },
            {
                'frame_anchor':    3,
                'platform':        0,
                'platform_anchor': 3,
                'cable':           3
            },
            {
                'frame_anchor':    4,
                'platform':        0,
                'platform_anchor': 4,
                'cable':           4
            },
            {
                'frame_anchor':    5,
                'platform':        0,
                'platform_anchor': 5,
                'cable':           5
            },
            {
                'frame_anchor':    6,
                'platform':        0,
                'platform_anchor': 6,
                'cable':           6
            },
            {
                'frame_anchor':    7,
                'platform':        0,
                'platform_anchor': 7,
                'cable':           7
            },
        ],
    )


@pytest.fixture
def rand_vector_3d():
    return np.random.random(3)


@pytest.fixture
def rand_pos_1t():
    return np.pad(2 * (np.random.random(1) - 0.5), (0, 2))


@pytest.fixture
def rand_pos_2t():
    return np.pad(2 * (np.random.random(2) - 0.5), (0, 1))


@pytest.fixture
def rand_pos_3t():
    return np.pad(2 * (np.random.random(3) - 0.5), (0, 0))


@pytest.fixture
def rand_rot_1r():
    return Rotation.from_euler('z',
                               (2 * np.pi * (np.random.rand() - 0.5))
                               ).as_dcm()


@pytest.fixture
def rand_rot_2r():
    return Rotation.from_euler('yx',
                               (2 * np.pi * (np.random.random(2) - 0.5))
                               ).as_dcm()


@pytest.fixture
def rand_rot_3r():
    return Rotation.random().as_dcm()


@pytest.fixture
def rand_rot():
    return Rotation.random().as_dcm()


@pytest.fixture
def unit_rot():
    return Rotation.from_quat([0., 0., 0., 1.]).as_dcm()


@pytest.fixture
def empty_pose():
    return cdpyr.motion.Pose()


@pytest.fixture
def rand_pose_1t(rand_pos_1t, unit_rot):
    return cdpyr.motion.Pose(
        position=(rand_pos_1t, unit_rot)
    )


@pytest.fixture
def rand_pose_2t(rand_pos_2t, unit_rot):
    return cdpyr.motion.Pose(
        position=(rand_pos_2t, unit_rot)
    )


@pytest.fixture
def rand_pose_3t(rand_pos_3t, unit_rot):
    return cdpyr.motion.Pose(
        position=(rand_pos_3t, unit_rot)
    )


@pytest.fixture
def rand_pose_1r2t(rand_pos_2t, rand_rot_1r):
    return cdpyr.motion.Pose(
        position=(rand_pos_2t, rand_rot_1r)
    )


@pytest.fixture
def rand_pose_2r3t(rand_pos_3t, rand_rot_2r):
    return cdpyr.motion.Pose(
        position=(rand_pos_3t, rand_rot_2r)
    )


@pytest.fixture
def rand_pose_3r3t(rand_pos_3t, rand_rot_3r):
    return cdpyr.motion.Pose(
        position=(rand_pos_3t, rand_rot_3r)
    )


@pytest.fixture
def rand_pose_3d(rand_pos_3t, rand_rot_3r):
    return cdpyr.motion.Pose(
        position=(rand_pos_3t, rand_rot_3r)
    )


@pytest.fixture
def ik_standard():
    return cdpyr.analysis.kinematics.STANDARD()

from __future__ import annotations

import numpy as np

import cdpyr

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"


def robot_1t():
    return cdpyr.robot.Robot(
            name="Sample 1T robot",
            gravity=-9.81,
            frame=cdpyr.robot.Frame(
                    anchors=[
                            cdpyr.robot.FrameAnchor(
                                    position=pos,
                                    angular=cdpyr.kinematics.transformation.Angular.rotation_z(
                                            np.arctan2(-pos[1], -pos[0])),
                                    pulley=cdpyr.robot.Pulley(
                                            radius=0.10,
                                    )
                            ) for pos in (
                                    (-1.00, 0.00, 0.00),
                                    (1.00, 0.00, 0.00),
                            )
                    ]
            ),
            platforms=[
                    cdpyr.robot.Platform(
                            motion_pattern=cdpyr.motion.pattern.MP_1T,
                            inertia=cdpyr.mechanics.Inertia(
                                    np.diag((1, 1, 1)) * 1),
                            anchors=[
                                    cdpyr.robot.PlatformAnchor(),
                                    cdpyr.robot.PlatformAnchor(),
                            ]
                    ),
            ],
            cables=(
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
            ),
            kinematic_chains=(
                    {
                            'frame_anchor':    0,
                            # 'platform':        0,  # implied
                            'platform_anchor': 0,
                            'cable':           0
                    },
                    {
                            'frame_anchor':    1,
                            # 'platform':        0,  # implied
                            'platform_anchor': 1,
                            'cable':           1
                    },
            ),
    )


def robot_2t():
    return cdpyr.robot.Robot(
            name="Sample 2T robot",
            gravity=(0, -9.81),
            frame=cdpyr.robot.Frame(
                    anchors=[
                            cdpyr.robot.FrameAnchor(
                                    position=pos,
                                    angular=cdpyr.kinematics.transformation.Angular.rotation_z(
                                            np.arctan2(-pos[1], -pos[0])),
                                    pulley=cdpyr.robot.Pulley(
                                            radius=0.10,
                                    )
                            ) for pos in (
                                    (-1.05, 1.00, 0.00),
                                    (1.00, 0.95, 0.00),
                                    (0.05, -1.00, 0.00),
                            )
                    ]
            ),
            platforms=[
                    cdpyr.robot.Platform(
                            motion_pattern=cdpyr.motion.pattern.MP_2T,
                            inertia=cdpyr.mechanics.Inertia(
                                    np.diag((1, 1, 1)) * 1),
                            anchors=[
                                    cdpyr.robot.PlatformAnchor(),
                                    cdpyr.robot.PlatformAnchor(),
                                    cdpyr.robot.PlatformAnchor(),
                            ]
                    ),
            ],
            cables=(
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
            ),
            kinematic_chains=(
                    {
                            'frame_anchor':    0,
                            # 'platform':        0,  # implied
                            'platform_anchor': 0,
                            'cable':           0
                    },
                    {
                            'frame_anchor':    1,
                            # 'platform':        0,  # implied
                            'platform_anchor': 1,
                            'cable':           1
                    },
                    {
                            'frame_anchor':    2,
                            # 'platform':        0,  # implied
                            'platform_anchor': 2,
                            'cable':           2
                    },
            ),
    )


def robot_3t():
    return cdpyr.robot.Robot(
            name="Sample 3T robot",
            gravity=(0, 0, -9.81),
            frame=cdpyr.robot.Frame(
                    anchors=[
                            cdpyr.robot.FrameAnchor(
                                    position=pos,
                                    angular=cdpyr.kinematics.transformation.Angular.rotation_z(
                                            np.arctan2(-pos[1], -pos[0])),
                                    pulley=cdpyr.robot.Pulley(
                                            radius=0.10,
                                    )
                            ) for pos in (
                                    (-0.95, 1.00, 1.05),
                                    (1.00, 0.95, 0.95),
                                    (0.05, -1.00, 1.00),
                            )
                    ]
            ),
            platforms=[
                    cdpyr.robot.Platform(
                            motion_pattern=cdpyr.motion.pattern.MP_3T,
                            inertia=cdpyr.mechanics.Inertia(
                                    np.diag((1, 1, 1)) * 1),
                            anchors=[
                                    cdpyr.robot.PlatformAnchor(),
                                    cdpyr.robot.PlatformAnchor(),
                                    cdpyr.robot.PlatformAnchor(),
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
                            # 'platform':        0,  # implied
                            'platform_anchor': 0,
                            'cable':           0
                    },
                    {
                            'frame_anchor':    1,
                            # 'platform':        0,  # implied
                            'platform_anchor': 1,
                            'cable':           1
                    },
                    {
                            'frame_anchor':    2,
                            # 'platform':        0,  # implied
                            'platform_anchor': 2,
                            'cable':           2
                    },
            ],
    )


def robot_1r2t():
    return cdpyr.robot.Robot(
            name="Sample 1R2T robot",
            gravity=(0, -9.81),
            frame=cdpyr.robot.Frame(
                    anchors=[
                            cdpyr.robot.FrameAnchor(
                                    position=pos,
                                    angular=cdpyr.kinematics.transformation.Angular.rotation_z(
                                            np.arctan2(-pos[1], -pos[0])),
                                    pulley=cdpyr.robot.Pulley(
                                            radius=0.10,
                                    )
                            ) for pos in (
                                    (-1.05, 1.00, 0.00),
                                    (0.95, 1.00, 0.00),
                                    (1.05, -0.95, 0.00),
                                    (-1.00, -0.95, 0.00),
                            )
                    ]
            ),
            platforms=[
                    cdpyr.robot.Platform(
                            motion_pattern=cdpyr.motion.pattern.MP_1R2T,
                            inertia=cdpyr.mechanics.Inertia(
                                    np.diag((1, 1, 1)) * 5),
                            anchors=[
                                    cdpyr.robot.PlatformAnchor(
                                            position=pos,
                                            angular=cdpyr.kinematics.transformation.Angular.rotation_z(
                                                    np.arctan2(-pos[1],
                                                               -pos[0])),
                                    ) for pos in (
                                            (-0.095, 0.105, 0.00),
                                            (0.105, 0.095, 0.00),
                                            (0.105, -0.100, 0.00),
                                            (-0.100, -0.095, 0.00),
                                    )
                            ],
                    ),
            ],
            cables=(
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
            ),
            kinematic_chains=(
                    {
                            'frame_anchor':    0,
                            # 'platform':        0,  # implied
                            'platform_anchor': 3,
                            'cable':           3
                    },
                    {
                            'frame_anchor':    1,
                            # 'platform':        0,  # implied
                            'platform_anchor': 2,
                            'cable':           2
                    },
                    {
                            'frame_anchor':    2,
                            # 'platform':        0,  # implied
                            'platform_anchor': 1,
                            'cable':           1
                    },
                    {
                            'frame_anchor':    3,
                            # 'platform':        0,  # implied
                            'platform_anchor': 0,
                            'cable':           0
                    },
            ),
    )


def robot_2r3t():
    return cdpyr.robot.Robot(
            name="Sample 2R3T robot",
            gravity=(0, 0, -9.81),
            frame=cdpyr.robot.Frame(
                    anchors=[
                            cdpyr.robot.FrameAnchor(
                                    position=pos,
                                    angular=cdpyr.kinematics.transformation.Angular.rotation_z(
                                            np.arctan2(-pos[1], -pos[0])),
                                    pulley=cdpyr.robot.Pulley(
                                            radius=0.10,
                                    )
                            ) for pos in (
                                    (-1.00, 0.95, 1.05),
                                    (1.05, 0.95, 1.00),
                                    (1.05, -1.00, 0.95),
                                    (-0.95, -1.05, 1.00),
                                    (-1.05, 1.00, -0.95),
                                    (0.95, 1.05, -1.00),
                                    (0.95, -1.00, -1.05),
                                    (-1.05, -1.00, -1.05),
                            )
                    ]
            ),
            platforms=[
                    cdpyr.robot.Platform(
                            motion_pattern=cdpyr.motion.pattern.MP_2R3T,
                            inertia=cdpyr.mechanics.Inertia(
                                    np.diag((1, 1, 1)) * 1),
                            anchors=[
                                    cdpyr.robot.PlatformAnchor(
                                            position=pos,
                                            angular=cdpyr.kinematics.transformation.Angular.rotation_z(
                                                    np.arctan2(-pos[1],
                                                               -pos[0])),
                                    ) for pos in (
                                            (-0.095, 0.105, 0.100),
                                            (0.105, 0.095, 0.100),
                                            (0.105, -0.100, 0.095),
                                            (-0.100, -0.095, 0.105),
                                            (-0.095, 0.100, -0.105),
                                            (0.105, 0.10, -0.095),
                                            (0.095, -0.105, -0.100),
                                            (-0.105, -0.100, -0.105),
                                    )
                            ]
                    )
            ],
            cables=(
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
            ),
            kinematic_chains=(
                    {
                            'frame_anchor':    0,
                            # 'platform':        0,  # implied
                            'platform_anchor': 4,
                            'cable':           0
                    },
                    {
                            'frame_anchor':    1,
                            # 'platform':        0,  # implied
                            'platform_anchor': 5,
                            'cable':           1
                    },
                    {
                            'frame_anchor':    2,
                            # 'platform':        0,  # implied
                            'platform_anchor': 6,
                            'cable':           2
                    },
                    {
                            'frame_anchor':    3,
                            # 'platform':        0,  # implied
                            'platform_anchor': 7,
                            'cable':           3
                    },
                    {
                            'frame_anchor':    4,
                            # 'platform':        0,  # implied
                            'platform_anchor': 0,
                            'cable':           4
                    },
                    {
                            'frame_anchor':    5,
                            # 'platform':        0,  # implied
                            'platform_anchor': 1,
                            'cable':           5
                    },
                    {
                            'frame_anchor':    6,
                            # 'platform':        0,  # implied
                            'platform_anchor': 2,
                            'cable':           6
                    },
                    {
                            'frame_anchor':    7,
                            # 'platform':        0,  # implied
                            'platform_anchor': 3,
                            'cable':           7
                    },
            ),
    )


def robot_3r3t():
    return cdpyr.robot.Robot(
            name="Sample 3R3T robot",
            gravity=(0, 0, -9.81),
            frame=cdpyr.robot.Frame(
                    anchors=[
                            cdpyr.robot.FrameAnchor(
                                    position=pos,
                                    angular=cdpyr.kinematics.transformation.Angular.rotation_z(
                                            np.arctan2(-pos[1], -pos[0])),
                                    pulley=cdpyr.robot.Pulley(
                                            radius=0.10,
                                    )
                            ) for pos in (
                                    (-1.00, 0.95, 1.05),
                                    (1.05, 0.95, 1.00),
                                    (1.05, -1.00, 0.95),
                                    (-0.95, -1.05, 1.00),
                                    (-1.05, 1.00, -0.95),
                                    (0.95, 1.05, -1.00),
                                    (0.95, -1.00, -1.05),
                                    (-1.05, -1.00, -1.05),
                            )
                    ]
            ),
            platforms=[
                    cdpyr.robot.Platform(
                            motion_pattern=cdpyr.motion.pattern.MP_3R3T,
                            inertia=cdpyr.mechanics.Inertia(
                                    np.diag((1, 1, 1)) * 1),
                            anchors=[
                                    cdpyr.robot.PlatformAnchor(
                                            position=pos,
                                            angular=cdpyr.kinematics.transformation.Angular.rotation_z(
                                                    np.arctan2(-pos[1],
                                                               -pos[0])),
                                    ) for pos in (
                                            (-0.095, 0.105, 0.100),
                                            (0.105, 0.095, 0.100),
                                            (0.105, -0.100, 0.095),
                                            (-0.100, -0.095, 0.105),
                                            (-0.095, 0.100, -0.105),
                                            (0.105, 0.10, -0.095),
                                            (0.095, -0.105, -0.100),
                                            (-0.105, -0.100, -0.105),
                                    )
                            ]
                    )
            ],
            cables=(
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
            ),
            kinematic_chains=(
                    {
                            'frame_anchor':    0,
                            # 'platform':        0,  # implied
                            'platform_anchor': 4,
                            'cable':           4
                    },
                    {
                            'frame_anchor':    1,
                            # 'platform':        0,  # implied
                            'platform_anchor': 5,
                            'cable':           5
                    },
                    {
                            'frame_anchor':    2,
                            # 'platform':        0,  # implied
                            'platform_anchor': 6,
                            'cable':           6
                    },
                    {
                            'frame_anchor':    3,
                            # 'platform':        0,  # implied
                            'platform_anchor': 7,
                            'cable':           7
                    },
                    {
                            'frame_anchor':    4,
                            # 'platform':        0,  # implied
                            'platform_anchor': 0,
                            'cable':           0
                    },
                    {
                            'frame_anchor':    5,
                            # 'platform':        0,  # implied
                            'platform_anchor': 1,
                            'cable':           1
                    },
                    {
                            'frame_anchor':    6,
                            # 'platform':        0,  # implied
                            'platform_anchor': 2,
                            'cable':           2
                    },
                    {
                            'frame_anchor':    7,
                            # 'platform':        0,  # implied
                            'platform_anchor': 3,
                            'cable':           3
                    },
            ),
    )


def segesta():
    return cdpyr.robot.Robot(
            name="SeGeSTA",
            gravity=(0, 0, -9.81),
            frame=cdpyr.robot.Frame(
                    anchors=[
                            cdpyr.robot.FrameAnchor(
                                    position=pos,
                                    angular=cdpyr.kinematics.transformation.Angular.rotation_z(
                                            np.arctan2(-pos[1], -pos[0])),
                                    pulley=cdpyr.robot.Pulley(
                                            radius=0.10,
                                    )
                            ) for pos in (
                                    (-0.415, -0.315, -0.5),
                                    (-0.415, -0.315, 0.5),
                                    (0.415, -0.315, 0.5),
                                    (0.415, -0.315, -0.5),
                                    (0.415, 0.315, -0.5),
                                    (-0.415, 0.315, 0.5),
                                    (-0.415, 0.315, -0.5),
                                    (0.415, 0.315, 0.5),
                            )
                    ]
            ),
            platforms=[
                    cdpyr.robot.Platform(
                            motion_pattern=cdpyr.motion.pattern.MP_3R3T,
                            inertia=cdpyr.mechanics.Inertia(
                                    np.diag((1, 1, 1)) * 1,
                                    cdpyr.mechanics.Inertia.cuboid(1, 0.0525,
                                                                   0.2, 0.02)),
                            anchors=[
                                    cdpyr.robot.PlatformAnchor(
                                            position=pos,
                                            angular=cdpyr.kinematics.transformation.Angular.rotation_z(
                                                    np.arctan2(-pos[1],
                                                               -pos[0])),
                                    ) for pos in (
                                            (-0.0525, -0.0760, 0.01),
                                            (-0.0525, -0.0760, 0.01),
                                            (0.0525, -0.0760, 0.01),
                                            (0.0525, -0.0760, 0.01),
                                            (0.0000, 0.1240, -0.01),
                                            (0.0000, 0.1240, -0.01),
                                            (0.0000, 0.1240, -0.01),
                                            (0.0000, 0.1240, -0.01),
                                    )
                            ]
                    )
            ],
            cables=(
                    cdpyr.robot.Cable(
                            name="Dyneema",
                            material="Liros D-Pro SK78",
                            diameter=1.5 / 1000,
                            color="red",
                            density=0.00073565,
                            modulus={
                                    'elasticities': (12.2 * 1e9,),
                                    'viscosities':  (0.46,),
                            }
                    ),
                    cdpyr.robot.Cable(
                            name="Dyneema",
                            material="Liros D-Pro SK78",
                            diameter=1.5 / 1000,
                            color="red",
                            density=0.00073565,
                            modulus={
                                    'elasticities': (12.2 * 1e9,),
                                    'viscosities':  (0.46,),
                            }
                    ),
                    cdpyr.robot.Cable(
                            name="Dyneema",
                            material="Liros D-Pro SK78",
                            diameter=1.5 / 1000,
                            color="red",
                            density=0.00073565,
                            modulus={
                                    'elasticities': (12.2 * 1e9,),
                                    'viscosities':  (0.46,),
                            }
                    ),
                    cdpyr.robot.Cable(
                            name="Dyneema",
                            material="Liros D-Pro SK78",
                            diameter=1.5 / 1000,
                            color="red",
                            density=0.00073565,
                            modulus={
                                    'elasticities': (12.2 * 1e9,),
                                    'viscosities':  (0.46,),
                            }
                    ),
                    cdpyr.robot.Cable(
                            name="Dyneema",
                            material="Liros D-Pro SK78",
                            diameter=1.5 / 1000,
                            color="red",
                            density=0.00073565,
                            modulus={
                                    'elasticities': (12.2 * 1e9,),
                                    'viscosities':  (0.46,),
                            }
                    ),
                    cdpyr.robot.Cable(
                            name="Dyneema",
                            material="Liros D-Pro SK78",
                            diameter=1.5 / 1000,
                            color="red",
                            density=0.00073565,
                            modulus={
                                    'elasticities': (12.2 * 1e9,),
                                    'viscosities':  (0.46,),
                            }
                    ),
                    cdpyr.robot.Cable(
                            name="Dyneema",
                            material="Liros D-Pro SK78",
                            diameter=1.5 / 1000,
                            color="red",
                            density=0.00073565,
                            modulus={
                                    'elasticities': (12.2 * 1e9,),
                                    'viscosities':  (0.46,),
                            }
                    ),
                    cdpyr.robot.Cable(
                            name="Dyneema",
                            material="Liros D-Pro SK78",
                            diameter=1.5 / 1000,
                            color="red",
                            density=0.00073565,
                            modulus={
                                    'elasticities': (12.2 * 1e9,),
                                    'viscosities':  (0.46,),
                            }
                    ),
            ),
            kinematic_chains=(
                    {
                            'frame_anchor':    0,
                            # 'platform':        0,  # implied
                            'platform_anchor': 0,
                            'cable':           0
                    },
                    {
                            'frame_anchor':    1,
                            # 'platform':        0,  # implied
                            'platform_anchor': 1,
                            'cable':           1
                    },
                    {
                            'frame_anchor':    2,
                            # 'platform':        0,  # implied
                            'platform_anchor': 2,
                            'cable':           2
                    },
                    {
                            'frame_anchor':    3,
                            # 'platform':        0,  # implied
                            'platform_anchor': 3,
                            'cable':           3
                    },
                    {
                            'frame_anchor':    4,
                            # 'platform':        0,  # implied
                            'platform_anchor': 4,
                            'cable':           4
                    },
                    {
                            'frame_anchor':    5,
                            # 'platform':        0,  # implied
                            'platform_anchor': 5,
                            'cable':           5
                    },
                    {
                            'frame_anchor':    6,
                            # 'platform':        0,  # implied
                            'platform_anchor': 6,
                            'cable':           6
                    },
                    {
                            'frame_anchor':    7,
                            # 'platform':        0,  # implied
                            'platform_anchor': 7,
                            'cable':           7
                    },
            ),
    )


def ipanema_3():
    return cdpyr.robot.Robot(
            name="Sample IPAnema 3",
            gravity=(0, 0, -9.81),
            frame=cdpyr.robot.Frame(
                    anchors=[
                            cdpyr.robot.FrameAnchor(
                                    position=pos,
                                    angular=cdpyr.kinematics.transformation.Angular.rotation_z(
                                            np.arctan2(-pos[1], -pos[0])),
                                    pulley=cdpyr.robot.Pulley(
                                            radius=0.10,
                                    )
                            ) for pos in (
                                    (-8.544, 5.463, 3.202),
                                    (8.184, 5.692, 3.236),
                                    (8.224, -5.492, 3.25),
                                    (-8.491, -5.322, 3.221),
                                    (-8.192, 5.648, -0.589),
                                    (7.208, 6.463, -0.548),
                                    (7.869, -5.557, -0.527),
                                    (-8.27, -5.545, -0.582),
                            )
                    ]
            ),
            platforms=[
                    cdpyr.robot.Platform(
                            motion_pattern=cdpyr.motion.pattern.MP_3R3T,
                            inertia=cdpyr.mechanics.Inertia(
                                    np.diag((1, 1, 1)) * 30,
                                    np.diag((5.226154,
                                             0.637352,
                                             4.723802))),
                            anchors=[
                                    cdpyr.robot.PlatformAnchor(
                                            position=pos,
                                            angular=cdpyr.kinematics.transformation.Angular.rotation_z(
                                                    np.arctan2(-pos[1],
                                                               -pos[0])),
                                    ) for pos in (
                                            (-0.085, 0.748, 0.261),
                                            (0.095, 0.749, 0.26),
                                            (0.095, -0.745, 0.26),
                                            (-0.085, -0.746, 0.261),
                                            (-0.07, 0.648, -0.26),
                                            (0.06, 0.648, -0.262),
                                            (0.06, -0.651, -0.262),
                                            (-0.07, -0.651, -0.26),
                                    )
                            ]
                    )
            ],
            cables=(
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
            ),
            kinematic_chains=(
                    {
                            'frame_anchor':    0,
                            # 'platform':        0,  # implied
                            'platform_anchor': 4,
                            'cable':           4
                    },
                    {
                            'frame_anchor':    1,
                            # 'platform':        0,  # implied
                            'platform_anchor': 5,
                            'cable':           5
                    },
                    {
                            'frame_anchor':    2,
                            # 'platform':        0,  # implied
                            'platform_anchor': 6,
                            'cable':           6
                    },
                    {
                            'frame_anchor':    3,
                            # 'platform':        0,  # implied
                            'platform_anchor': 7,
                            'cable':           7
                    },
                    {
                            'frame_anchor':    4,
                            # 'platform':        0,  # implied
                            'platform_anchor': 0,
                            'cable':           0
                    },
                    {
                            'frame_anchor':    5,
                            # 'platform':        0,  # implied
                            'platform_anchor': 1,
                            'cable':           1
                    },
                    {
                            'frame_anchor':    6,
                            # 'platform':        0,  # implied
                            'platform_anchor': 2,
                            'cable':           2
                    },
                    {
                            'frame_anchor':    7,
                            # 'platform':        0,  # implied
                            'platform_anchor': 3,
                            'cable':           3
                    },
            ),
    )


def cogiro():
    return cdpyr.robot.Robot(
            name="CoGiRo",
            gravity=(0, 0, -9.81),
            frame=cdpyr.robot.Frame(
                    anchors=[
                            cdpyr.robot.FrameAnchor(
                                    position=pos,
                                    angular=cdpyr.kinematics.transformation.Angular.rotation_z(
                                            np.arctan2(-pos[1], -pos[0])),
                                    pulley=cdpyr.robot.Pulley(
                                            radius=0.10,
                                    )
                            ) for pos in (
                                    (-7.11966, 5.47261, 5.41063),
                                    (7.50556, 5.07892, 5.41820),
                                    (7.14351, -5.54158, 5.39749),
                                    (-7.47855, -5.15440, 5.40093),
                                    (-7.40830, 5.19141, 5.39874),
                                    (7.22425, 5.36889, 5.40799),
                                    (7.42883, -5.26133, 5.38777),
                                    (-7.19673, -5.43978, 5.39277),
                            )
                    ]
            ),
            platforms=[
                    cdpyr.robot.Platform(
                            motion_pattern=cdpyr.motion.pattern.MP_3R3T,
                            inertia=cdpyr.mechanics.Inertia(
                                    np.diag((1, 1, 1)) * 91.058,
                                    np.asarray((
                                            (42.955, -0.414, 2.205),
                                            (-0.414, 42.427, -1.849),
                                            (2.205, -1.849, 25.557),
                                    ))),
                            anchors=[
                                    cdpyr.robot.PlatformAnchor(
                                            position=pos,
                                            angular=cdpyr.kinematics.transformation.Angular.rotation_z(
                                                    np.arctan2(-pos[1],
                                                               -pos[0])),
                                    ) for pos in (
                                            (-0.50968, 0.35080, 0.99759),
                                            (0.49605, 0.35613, 0.99961),
                                            (0.49983, -0.34038, 0.99913),
                                            (-0.50453, -0.34632, 0.99765),
                                            (-0.50316, 0.49282, 0),
                                            (0.50214, 0.27502, -0.00067),
                                            (0.50316, -0.49282, 0),
                                            (-0.50316, -0.26997, 0),
                                    )
                            ],
                            center_of_gravity=(-0.034, -0.013, 0.264),
                    )
            ],
            cables=(
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
            ),
            kinematic_chains=(
                    {
                            'frame_anchor':    0,
                            # 'platform':        0,  # implied
                            'platform_anchor': 1,
                            'cable':           1
                    },
                    {
                            'frame_anchor':    1,
                            # 'platform':        0,  # implied
                            'platform_anchor': 2,
                            'cable':           2
                    },
                    {
                            'frame_anchor':    2,
                            # 'platform':        0,  # implied
                            'platform_anchor': 3,
                            'cable':           3
                    },
                    {
                            'frame_anchor':    3,
                            # 'platform':        0,  # implied
                            'platform_anchor': 0,
                            'cable':           0
                    },
                    {
                            'frame_anchor':    4,
                            # 'platform':        0,  # implied
                            'platform_anchor': 7,
                            'cable':           7
                    },
                    {
                            'frame_anchor':    5,
                            # 'platform':        0,  # implied
                            'platform_anchor': 4,
                            'cable':           4
                    },
                    {
                            'frame_anchor':    6,
                            # 'platform':        0,  # implied
                            'platform_anchor': 5,
                            'cable':           5
                    },
                    {
                            'frame_anchor':    7,
                            # 'platform':        0,  # implied
                            'platform_anchor': 6,
                            'cable':           6
                    },
            ),
            home_pose=cdpyr.motion.pose.Pose(
                    linear=cdpyr.kinematics.transformation.Linear((0.0109,
                                                                   -0.0101,
                                                                   1.3176)),
                    angular=cdpyr.kinematics.transformation.Angular(
                            sequence='xyz', euler=(0.0201, 0.0012, -0.0151))
            )
    )


__all__ = [
        'robot_1t',
        'robot_2t',
        'robot_3t',
        'robot_1r2t',
        'robot_2r3t',
        'robot_3r3t',
        'ipanema_3',
        'cogiro',
        'segesta',
]

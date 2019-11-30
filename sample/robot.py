import numpy as np

import cdpyr


def mp_1t():
    return cdpyr.robot.Robot(
            name="Sample 1T robot",
            gravity=-9.81,
            frame=cdpyr.robot.Frame(
                    anchors=[
                        cdpyr.robot.FrameAnchor(
                                position=[-1., 0., 0.],
                                angular=cdpyr.kinematics.transformation.Angular.random(),
                        ),
                        cdpyr.robot.FrameAnchor(
                                position=[1., 0., 0.],
                                angular=cdpyr.kinematics.transformation.Angular.random(),
                        ),
                    ]
            ),
            platforms=[
                cdpyr.robot.Platform(
                        motion_pattern=cdpyr.motion.pattern.MP_1T,
                        inertia=cdpyr.mechanics.Inertia(np.diag((1, 1, 1)) * 1),
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
            ],
    )


def mp_2t():
    return cdpyr.robot.Robot(
            name="Sample 2T robot",
            gravity=[0, -9.81],
            frame=cdpyr.robot.Frame(
                    anchors=[
                        cdpyr.robot.FrameAnchor(
                                position=[-1., 1., 0.],
                                angular=cdpyr.kinematics.transformation.Angular.random(),
                        ),
                        cdpyr.robot.FrameAnchor(
                                position=[1., 1., 0.],
                                angular=cdpyr.kinematics.transformation.Angular.random(),
                        ),
                        cdpyr.robot.FrameAnchor(
                                position=[0., -1., 0.],
                                angular=cdpyr.kinematics.transformation.Angular.random(),
                        ),
                    ]
            ),
            platforms=[
                cdpyr.robot.Platform(
                        motion_pattern=cdpyr.motion.pattern.MP_2T,
                        inertia=cdpyr.mechanics.Inertia(np.diag((1, 1, 1)) * 1),
                        anchors=[
                            cdpyr.robot.PlatformAnchor(
                                    position=[0., 0., 0.],
                            ),
                            cdpyr.robot.PlatformAnchor(
                                    position=[0., 0., 0.],
                            ),
                            cdpyr.robot.PlatformAnchor(
                                    position=[0., -0., 0.],
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


def mp_3t():
    return cdpyr.robot.Robot(
            name="Sample 3T robot",
            gravity=[0, 0, -9.81],
            frame=cdpyr.robot.Frame(
                    anchors=[
                        cdpyr.robot.FrameAnchor(
                                position=[-1., 1., 1.],
                                angular=cdpyr.kinematics.transformation.Angular.random(),
                        ),
                        cdpyr.robot.FrameAnchor(
                                position=[1., 1., 1.],
                                angular=cdpyr.kinematics.transformation.Angular.random(),
                        ),
                        cdpyr.robot.FrameAnchor(
                                position=[0., -1., 1.],
                                angular=cdpyr.kinematics.transformation.Angular.random(),
                        ),
                        cdpyr.robot.FrameAnchor(
                                position=[0., 0., 0.],
                                angular=cdpyr.kinematics.transformation.Angular.random(),
                        ),
                    ]
            ),
            platforms=[
                cdpyr.robot.Platform(
                        motion_pattern=cdpyr.motion.pattern.MP_3T,
                        inertia=cdpyr.mechanics.Inertia(np.diag((1, 1, 1)) * 1),
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
                {
                    'frame_anchor':    3,
                    # 'platform':        0,  # implied
                    'platform_anchor': 3,
                    'cable':           3
                },
            ],
    )


def mp_1r2t():
    return cdpyr.robot.Robot(
            name="Sample 1R2T robot",
            gravity=[0, -9.81],
            frame=cdpyr.robot.Frame(
                    anchors=[
                        cdpyr.robot.FrameAnchor(
                                position=[-1., 1., 0.],
                                angular=cdpyr.kinematics.transformation.Angular.random(),
                        ),
                        cdpyr.robot.FrameAnchor(
                                position=[1., 1., 0.],
                                angular=cdpyr.kinematics.transformation.Angular.random(),
                        ),
                        cdpyr.robot.FrameAnchor(
                                position=[1., -1., 0.],
                                angular=cdpyr.kinematics.transformation.Angular.random(),
                        ),
                        cdpyr.robot.FrameAnchor(
                                position=[-1., -1., 0.],
                                angular=cdpyr.kinematics.transformation.Angular.random(),
                        ),
                    ]
            ),
            platforms=[
                cdpyr.robot.Platform(
                        motion_pattern=cdpyr.motion.pattern.MP_1R2T,
                        inertia=cdpyr.mechanics.Inertia(np.diag((1, 1, 1)) * 1),
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
                {
                    'frame_anchor':    3,
                    # 'platform':        0,  # implied
                    'platform_anchor': 3,
                    'cable':           3
                },
            ],
    )


def mp_2r3t():
    return cdpyr.robot.Robot(
            name="Sample 2R3T robot",
            gravity=[0, 0, -9.81],
            frame=cdpyr.robot.Frame(
                    anchors=[
                        cdpyr.robot.FrameAnchor(
                                position=[-1.0, 1.0, 1.0],
                                angular=cdpyr.kinematics.transformation.Angular.random(),
                        ),
                        cdpyr.robot.FrameAnchor(
                                position=[1.0, 1.0, 1.0],
                                angular=cdpyr.kinematics.transformation.Angular.random(),
                        ),
                        cdpyr.robot.FrameAnchor(
                                position=[1.0, -1.0, 1.0],
                                angular=cdpyr.kinematics.transformation.Angular.random(),
                        ),
                        cdpyr.robot.FrameAnchor(
                                position=[-1.0, -1.0, 1.0],
                                angular=cdpyr.kinematics.transformation.Angular.random(),
                        ),
                        cdpyr.robot.FrameAnchor(
                                position=[-1.0, 1.0, -1.0],
                                angular=cdpyr.kinematics.transformation.Angular.random(),
                        ),
                        cdpyr.robot.FrameAnchor(
                                position=[1.0, 1.0, -1.0],
                                angular=cdpyr.kinematics.transformation.Angular.random(),
                        ),
                        cdpyr.robot.FrameAnchor(
                                position=[1.0, -1.0, -1.0],
                                angular=cdpyr.kinematics.transformation.Angular.random(),
                        ),
                        cdpyr.robot.FrameAnchor(
                                position=[-1.0, -1.0, -1.0],
                                angular=cdpyr.kinematics.transformation.Angular.random(),
                        ),
                    ]
            ),
            platforms=[
                cdpyr.robot.Platform(
                        motion_pattern=cdpyr.motion.pattern.MP_2R3T,
                        inertia=cdpyr.mechanics.Inertia(np.diag((1, 1, 1)) * 1),
                        anchors=[
                            cdpyr.robot.PlatformAnchor(
                                    position=[0., 0., 0.1],
                            ),
                            cdpyr.robot.PlatformAnchor(
                                    position=[0., 0., 0.1],
                            ),
                            cdpyr.robot.PlatformAnchor(
                                    position=[0., 0., 0.1],
                            ),
                            cdpyr.robot.PlatformAnchor(
                                    position=[0., 0., 0.1],
                            ),
                            cdpyr.robot.PlatformAnchor(
                                    position=[0., 0., -0.1],
                            ),
                            cdpyr.robot.PlatformAnchor(
                                    position=[0., 0., -0.1],
                            ),
                            cdpyr.robot.PlatformAnchor(
                                    position=[0., 0., -0.1],
                            ),
                            cdpyr.robot.PlatformAnchor(
                                    position=[0., 0., -0.1],
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
            ],
    )


def mp_3r3t():
    return cdpyr.robot.Robot(
            name="Sample 3R3T robot",
            gravity=[0, 0, -9.81],
            frame=cdpyr.robot.Frame(
                    anchors=[
                        cdpyr.robot.FrameAnchor(
                                position=[-1.0, 1.0, 1.0],
                                angular=cdpyr.kinematics.transformation.Angular.random(),
                        ),
                        cdpyr.robot.FrameAnchor(
                                position=[1.0, 1.0, 1.0],
                                angular=cdpyr.kinematics.transformation.Angular.random(),
                        ),
                        cdpyr.robot.FrameAnchor(
                                position=[1.0, -1.0, 1.0],
                                angular=cdpyr.kinematics.transformation.Angular.random(),
                        ),
                        cdpyr.robot.FrameAnchor(
                                position=[-1.0, -1.0, 1.0],
                                angular=cdpyr.kinematics.transformation.Angular.random(),
                        ),
                        cdpyr.robot.FrameAnchor(
                                position=[-1.0, 1.0, -1.0],
                                angular=cdpyr.kinematics.transformation.Angular.random(),
                        ),
                        cdpyr.robot.FrameAnchor(
                                position=[1.0, 1.0, -1.0],
                                angular=cdpyr.kinematics.transformation.Angular.random(),
                        ),
                        cdpyr.robot.FrameAnchor(
                                position=[1.0, -1.0, -1.0],
                                angular=cdpyr.kinematics.transformation.Angular.random(),
                        ),
                        cdpyr.robot.FrameAnchor(
                                position=[-1.0, -1.0, -1.0],
                                angular=cdpyr.kinematics.transformation.Angular.random(),
                        ),
                    ]
            ),
            platforms=[
                cdpyr.robot.Platform(
                        motion_pattern=cdpyr.motion.pattern.MP_3R3T,
                        inertia=cdpyr.mechanics.Inertia(np.diag((1, 1, 1)) * 1),
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
            ],
    )


def ipanema_3():
    return cdpyr.robot.Robot(
            name="Sample IPAnema 3",
            gravity=[0, 0, -9.81],
            frame=cdpyr.robot.Frame(
                    anchors=[
                        cdpyr.robot.FrameAnchor(
                                position=[-8.544, 5.463, 3.202],
                                angular=cdpyr.kinematics.transformation.Angular.random(),
                        ),
                        cdpyr.robot.FrameAnchor(
                                position=[8.184, 5.692, 3.236],
                                angular=cdpyr.kinematics.transformation.Angular.random(),
                        ),
                        cdpyr.robot.FrameAnchor(
                                position=[8.224, -5.492, 3.25],
                                angular=cdpyr.kinematics.transformation.Angular.random(),
                        ),
                        cdpyr.robot.FrameAnchor(
                                position=[-8.491, -5.322, 3.221],
                                angular=cdpyr.kinematics.transformation.Angular.random(),
                        ),
                        cdpyr.robot.FrameAnchor(
                                position=[-8.192, 5.648, -0.589],
                                angular=cdpyr.kinematics.transformation.Angular.random(),
                        ),
                        cdpyr.robot.FrameAnchor(
                                position=[7.208, 6.463, -0.548],
                                angular=cdpyr.kinematics.transformation.Angular.random(),
                        ),
                        cdpyr.robot.FrameAnchor(
                                position=[7.869, -5.557, -0.527],
                                angular=cdpyr.kinematics.transformation.Angular.random(),
                        ),
                        cdpyr.robot.FrameAnchor(
                                position=[-8.27, -5.545, -0.582],
                                angular=cdpyr.kinematics.transformation.Angular.random(),
                        ),
                    ]
            ),
            platforms=[
                cdpyr.robot.Platform(
                        motion_pattern=cdpyr.motion.pattern.MP_3R3T,
                        inertia=cdpyr.mechanics.Inertia(np.diag((1, 1, 1)) * 25,
                                                        np.diag((5.226154,
                                                                 0.637352,
                                                                 4.723802))),
                        anchors=[
                            cdpyr.robot.PlatformAnchor(
                                    position=[-0.085, 0.748, 0.261],
                            ),
                            cdpyr.robot.PlatformAnchor(
                                    position=[0.095, 0.749, 0.26],
                            ),
                            cdpyr.robot.PlatformAnchor(
                                    position=[0.095, -0.745, 0.26],
                            ),
                            cdpyr.robot.PlatformAnchor(
                                    position=[-0.085, -0.746, 0.261],
                            ),
                            cdpyr.robot.PlatformAnchor(
                                    position=[-0.07, 0.648, -0.26],
                            ),
                            cdpyr.robot.PlatformAnchor(
                                    position=[0.06, 0.648, -0.262],
                            ),
                            cdpyr.robot.PlatformAnchor(
                                    position=[0.06, -0.651, -0.262],
                            ),
                            cdpyr.robot.PlatformAnchor(
                                    position=[-0.07, -0.651, -0.26],
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
                    'platform_anchor': 1,
                    'cable':           1
                },
                {
                    'frame_anchor':    5,
                    # 'platform':        0,  # implied
                    'platform_anchor': 2,
                    'cable':           2
                },
                {
                    'frame_anchor':    6,
                    # 'platform':        0,  # implied
                    'platform_anchor': 3,
                    'cable':           3
                },
                {
                    'frame_anchor':    7,
                    # 'platform':        0,  # implied
                    'platform_anchor': 4,
                    'cable':           4
                },
            ],
    )


def mp_3r3t_2platform():
    return cdpyr.robot.Robot(
            name="Sample 3R3T robot with 2 platforms",
            gravity=[0, 0, -9.81],
            frame=cdpyr.robot.Frame(
                    anchors=[
                        cdpyr.robot.FrameAnchor(
                                position=[-1.0, 1.0, 1.0],
                                angular=cdpyr.kinematics.transformation.Angular.random(),
                        ),
                        cdpyr.robot.FrameAnchor(
                                position=[1.0, 1.0, 1.0],
                                angular=cdpyr.kinematics.transformation.Angular.random(),
                        ),
                        cdpyr.robot.FrameAnchor(
                                position=[1.0, -1.0, 1.0],
                                angular=cdpyr.kinematics.transformation.Angular.random(),
                        ),
                        cdpyr.robot.FrameAnchor(
                                position=[-1.0, -1.0, 1.0],
                                angular=cdpyr.kinematics.transformation.Angular.random(),
                        ),
                        cdpyr.robot.FrameAnchor(
                                position=[-1.0, 1.0, 0.0],
                                angular=cdpyr.kinematics.transformation.Angular.random(),
                        ),
                        cdpyr.robot.FrameAnchor(
                                position=[1.0, 1.0, 0.0],
                                angular=cdpyr.kinematics.transformation.Angular.random(),
                        ),
                        cdpyr.robot.FrameAnchor(
                                position=[1.0, -1.0, 0.0],
                                angular=cdpyr.kinematics.transformation.Angular.random(),
                        ),
                        cdpyr.robot.FrameAnchor(
                                position=[-1.0, -1.0, 0.0],
                                angular=cdpyr.kinematics.transformation.Angular.random(),
                        ),
                        cdpyr.robot.FrameAnchor(
                                position=[-1.0, 1.0, 0.0],
                                angular=cdpyr.kinematics.transformation.Angular.random(),
                        ),
                        cdpyr.robot.FrameAnchor(
                                position=[1.0, 1.0, 0.0],
                                angular=cdpyr.kinematics.transformation.Angular.random(),
                        ),
                        cdpyr.robot.FrameAnchor(
                                position=[1.0, -1.0, 0.0],
                                angular=cdpyr.kinematics.transformation.Angular.random(),
                        ),
                        cdpyr.robot.FrameAnchor(
                                position=[-1.0, -1.0, 0.0],
                                angular=cdpyr.kinematics.transformation.Angular.random(),
                        ),
                        cdpyr.robot.FrameAnchor(
                                position=[-1.0, 1.0, -1.0],
                                angular=cdpyr.kinematics.transformation.Angular.random(),
                        ),
                        cdpyr.robot.FrameAnchor(
                                position=[1.0, 1.0, -1.0],
                                angular=cdpyr.kinematics.transformation.Angular.random(),
                        ),
                        cdpyr.robot.FrameAnchor(
                                position=[1.0, -1.0, -1.0],
                                angular=cdpyr.kinematics.transformation.Angular.random(),
                        ),
                        cdpyr.robot.FrameAnchor(
                                position=[-1.0, -1.0, -1.0],
                                angular=cdpyr.kinematics.transformation.Angular.random(),
                        ),
                    ]
            ),
            platforms=[
                cdpyr.robot.Platform(
                        motion_pattern=cdpyr.motion.pattern.MP_3R3T,
                        inertia=cdpyr.mechanics.Inertia(np.diag((1, 1, 1)) * 1),
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
                        ],
                        name="upper platform",
                ),
                cdpyr.robot.Platform(
                        motion_pattern=cdpyr.motion.pattern.MP_3R3T,
                        inertia=cdpyr.mechanics.Inertia(np.diag((1, 1, 1)) * 1),
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
                        ],
                        name="lower platform",
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
                {
                    'frame_anchor':    8,
                    'platform':        1,
                    'platform_anchor': 0,
                    'cable':           0
                },
                {
                    'frame_anchor':    9,
                    'platform':        1,
                    'platform_anchor': 1,
                    'cable':           1
                },
                {
                    'frame_anchor':    10,
                    'platform':        1,
                    'platform_anchor': 2,
                    'cable':           2
                },
                {
                    'frame_anchor':    11,
                    'platform':        1,
                    'platform_anchor': 3,
                    'cable':           3
                },
                {
                    'frame_anchor':    12,
                    'platform':        1,
                    'platform_anchor': 4,
                    'cable':           4
                },
                {
                    'frame_anchor':    13,
                    'platform':        1,
                    'platform_anchor': 5,
                    'cable':           5
                },
                {
                    'frame_anchor':    14,
                    'platform':        1,
                    'platform_anchor': 6,
                    'cable':           6
                },
                {
                    'frame_anchor':    15,
                    'platform':        1,
                    'platform_anchor': 7,
                    'cable':           7
                },
            ],
    )

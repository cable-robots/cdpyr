import cdpyr


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
                motionpattern=cdpyr.motion.Motionpattern.MP_1T,
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
            {'frame_anchor': 0, 'platform': 0, 'platform_anchor': 0, 'cable': 0},
            {'frame_anchor': 1, 'platform': 0, 'platform_anchor': 1, 'cable': 1},
        ],
    )


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
                motionpattern=cdpyr.motion.Motionpattern.MP_2T,
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
            {'frame_anchor': 0, 'platform': 0, 'platform_anchor': 0, 'cable': 0},
            {'frame_anchor': 1, 'platform': 0, 'platform_anchor': 1, 'cable': 1},
            {'frame_anchor': 2, 'platform': 0, 'platform_anchor': 2, 'cable': 2},
        ],
    )


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
                cdpyr.robot.FrameAnchor(
                    position=[0., 0., 0.],
                ),
            ]
        ),
        platforms=[
            cdpyr.robot.Platform(
                motionpattern=cdpyr.motion.Motionpattern.MP_3T,
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
            {'frame_anchor': 0, 'platform': 0, 'platform_anchor': 0, 'cable': 0},
            {'frame_anchor': 1, 'platform': 0, 'platform_anchor': 1, 'cable': 1},
            {'frame_anchor': 2, 'platform': 0, 'platform_anchor': 2, 'cable': 2},
            {'frame_anchor': 3, 'platform': 0, 'platform_anchor': 3, 'cable': 3},
        ],
    )


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
                motionpattern=cdpyr.motion.Motionpattern.MP_1R2T,
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
            {'frame_anchor': 0, 'platform': 0, 'platform_anchor': 0, 'cable': 0},
            {'frame_anchor': 1, 'platform': 0, 'platform_anchor': 1, 'cable': 1},
            {'frame_anchor': 2, 'platform': 0, 'platform_anchor': 2, 'cable': 2},
            {'frame_anchor': 3, 'platform': 0, 'platform_anchor': 3, 'cable': 3},
        ],
    )


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
                motionpattern=cdpyr.motion.Motionpattern.MP_2R3T,
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
            {'frame_anchor': 0, 'platform': 0, 'platform_anchor': 4, 'cable': 0},
            {'frame_anchor': 1, 'platform': 0, 'platform_anchor': 5, 'cable': 1},
            {'frame_anchor': 2, 'platform': 0, 'platform_anchor': 6, 'cable': 2},
            {'frame_anchor': 3, 'platform': 0, 'platform_anchor': 7, 'cable': 3},
            {'frame_anchor': 4, 'platform': 0, 'platform_anchor': 0, 'cable': 4},
            {'frame_anchor': 5, 'platform': 0, 'platform_anchor': 1, 'cable': 5},
            {'frame_anchor': 6, 'platform': 0, 'platform_anchor': 2, 'cable': 6},
            {'frame_anchor': 7, 'platform': 0, 'platform_anchor': 3, 'cable': 7},
        ],
    )



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
                motionpattern=cdpyr.motion.Motionpattern.MP_3R3T,
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
            {'frame_anchor': 0, 'platform': 0, 'platform_anchor': 4, 'cable': 0},
            {'frame_anchor': 1, 'platform': 0, 'platform_anchor': 5, 'cable': 1},
            {'frame_anchor': 2, 'platform': 0, 'platform_anchor': 6, 'cable': 2},
            {'frame_anchor': 3, 'platform': 0, 'platform_anchor': 7, 'cable': 3},
            {'frame_anchor': 4, 'platform': 0, 'platform_anchor': 0, 'cable': 4},
            {'frame_anchor': 5, 'platform': 0, 'platform_anchor': 1, 'cable': 5},
            {'frame_anchor': 6, 'platform': 0, 'platform_anchor': 2, 'cable': 6},
            {'frame_anchor': 7, 'platform': 0, 'platform_anchor': 3, 'cable': 7},
        ],
    )

import cdpyr


def ipanema_cuboid():
    r = cdpyr.robot.Robot(
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
                motionpattern=cdpyr.motion.Motionpattern._3R3T,
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
        kinematic_chains={
            (0, 0, 4, 0),
            (1, 0, 5, 1),
            (2, 0, 6, 2),
            (3, 0, 7, 3),
            (4, 0, 0, 4),
            (5, 0, 1, 5),
            (6, 0, 2, 6),
            (7, 0, 3, 7)
        }
    )

    return r

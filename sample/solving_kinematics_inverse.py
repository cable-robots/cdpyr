import cdpyr

# Load robot from file
copacabana = cdpyr.robot.load('/path/to/file.wcrfx')

# Set robot pose
copacabana.pose = cdpyr.motion.pose(position=[0, 0, 0],
                                    dcm=[[1, 0, 0], [0, 1, 0], [0, 0, 1]])

# Create algorithm solvers
iksolver = cdpyr.kinematics.inverse()

# Solve standard inverse kinematics for the currently active pose
iksol = iksolver.step(copacabana, iksolver.STANDARD)

# Define a list of poses to evaluate algorithms on
copacabana.pose = cdpyr.motion.poselist(
    cdpyr.motion.pose(position=[0, 0, 0],
                      dcm=[[1, 0, 0], [0, 1, 0], [0, 0, 1]]),
    cdpyr.motion.pose(position=[0, 0, 0],
                      dcm=[[1, 0, 0], [0, 1, 0], [0, 0, 1]])
)

# Solve pulley-based inverse kinematics for the currently active pose list
iksol = iksolver.step(copacabana, iksolver.PULLEY)

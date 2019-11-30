import copy
import numpy as _np
from magic_repr import make_repr
from matplotlib.testing.jpl_units import rad
from numpy import vectorize

from cdpyr.kinematics.transformation import  angular as _angular
from cdpyr.analysis import result as _result
from cdpyr.analysis.kinematics import algorithm as _kinematics
from cdpyr.motion.pose import pose as _pose
from cdpyr.robot import kinematicchain as _kinematicchain, robot as _robot, platform as _platform, cable as _cable
from cdpyr.robot.anchor import frame_anchor as _frame_anchor, platform_anchor as _platform_anchor
from cdpyr.typing import Matrix, Vector

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"


class KinematicsResult(_result.PoseResult):
    _algorithm: '_kinematics.Algorithm'
    _directions: Matrix
    _joints: Vector
    _swivel: Vector
    _wrap: Vector

    def __init__(self,
                 algorithm: '_kinematics.Algorithm',
                 pose: '_pose.Pose',
                 joints: Vector,
                 directions: Matrix,
                 swivel: Vector = None,
                 wrap: Vector = None,
                 **kwargs):
        super().__init__(pose)
        self._algorithm = copy.deepcopy(algorithm)
        self._joints = joints
        self._directions = directions
        self._swivel = swivel
        self._wrap = wrap

    @property
    def algorithm(self):
        return self._algorithm

    @property
    def cable_lengths(self):
        return self.joints

    @property
    def directions(self):
        return self._directions

    @property
    def joints(self):
        return self._joints

    @property
    def lengths(self):
        return self._joints

    def shape(self, robot: '_robot.Robot'):
        # discretization of points along the cable length
        num = 100

        # number of kinematic chains in this robot
        num_chains = robot.num_kinematic_chains

        # store results in an (chain, [X, Y, Z], point)-array
        shape = _np.zeros((num_chains, 3, num))

        # get position and orientation of the robot configuration used in
        # this kinematics result
        position, dcm = self.pose.position

        # get swivel and wrap angle of each anchor, or default to zero if there isn't any
        swivel = self.swivel if self.swivel is not None else _np.zeros((num_chains))
        wrap = self.wrap if self.wrap is not None else _np.zeros((num_chains))

        # loop over each kinematic chain
        chain: _kinematicchain.KinematicChain
        frame_anchor: _frame_anchor.FrameAnchor
        platform_anchor: _platform_anchor.PlatformAnchor
        cable: _cable.Cable
        for index_chain, chain in enumerate(robot.kinematic_chains):
            frame_anchor = robot.frame.anchors[chain.frame_anchor]
            platform = robot.platforms[chain.platform]
            platform_anchor = platform.anchors[chain.platform_anchor]
            cable = robot.cables[chain.cable]

            # get orientations of each anchor and pulley
            pos_frame_anchor = frame_anchor.linear.position
            dcm_frame_anchor = frame_anchor.angular.dcm
            try:
                dcm_pulley = frame_anchor.pulley.angular.dcm
            except AttributeError:
                dcm_pulley = _np.eye(3)
            dcm_cable = _angular.Angular.rotation_z(swivel[index_chain]).dcm

            # transformation matrix from pulley to world
            transform_pulley_2_world: Matrix
            transform_pulley_2_world = dcm_frame_anchor.dot(dcm_pulley.dot(dcm_cable))
            transform_world_2_pulley = transform_pulley_2_world.T

            # cable unit vector in local cable coordinate system
            direction_in_cable = transform_world_2_pulley.dot(self.directions[:,index_chain])
            # calculate position of cable leaving pulley
            dcm_wrap = _angular.Angular.rotation_y(wrap[index_chain]).dcm
            try:
                radius_vector = _np.asarray((frame_anchor.pulley.radius, 0, 0))
            except AttributeError:
                radius_vector = _np.zeros((3, ))

            # calculate point where cable leaves
            cable_leave_point_in_cable = dcm_wrap.dot(rad)

            # calculate length of cable on pulley
            try:
                cable_length_on_pulley = wrap[index_chain] * frame_anchor.pulley.radius
            except AttributeError:
                cable_length_on_pulley = 0

            # cable length in the workspace is the remainder from the total cable length
            cable_length_in_workspace = self.joints[index_chain] - cable_length_on_pulley

            # discretize the whole cable length into the desired amount of points
            linspace_cable_length = _np.linspace(0, self.joints[index_chain], num=num, endpoint=True)



            print('here')

            # # move the platform anchor at its global position
            # pos_platform_anchor = position + dcm.dot(platform_anchor.linear.position)
            #
            # # transform the platform anchor position into the pulley coordinate system
            # platform_anchor_in_pulley = dcm_cable.dot(dcm_pulley.T.dot(dcm_frame_anchor.T.dot(pos_frame_anchor - pos_platform_anchor)))


        # loop over each kinematic chain
        # # get the global frame anchor positions in the correct sorted order
        # frame_anchors = _np.vstack(
        #         [robot.frame.anchors[index].linear.position for index in
        #          robot.kinematic_chains.frame_anchor]).T
        # # get the platform anchors in the right order
        # index_platform = 0
        # platform_anchors = (robot.platforms[index_platform].anchors[index] for
        #                     index in robot.kinematic_chains.with_platform(
        #         index_platform).platform_anchor)
        #
        # # get platform position and orientation
        # pos, rot = self.pose.position
        #
        # # first, move the platform anchors to their global position given the
        # # pose
        # platform_anchors = _np.vstack(
        #         [pos + rot.dot(anchor.linear.position) for anchor in
        #          platform_anchors]).T
        #
        # # get swivel and wrap angle of each anchor, or default to zero if
        # there isn't anuy
        # swivel = self.swivel if self.swivel is not None else _np.zeros((
        # frame_anchors.shape[1]))
        # wrap = self.wrap if self.wrap is not None else _np.zeros((
        # frame_anchors.shape[1]))
        #
        # # calculate the cable shape in the local coordinate system of each

    @property
    def swivel(self):
        return self._swivel

    @property
    def wrap(self):
        return self._wrap

    __repr__ = make_repr(
            'algorithm',
            'pose',
            'joints',
            'swivel',
            'wrap',
    )


__all__ = [
    'KinematicsResult',
]

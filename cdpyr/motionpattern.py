from enum import Enum

__version__ = '1.0.0-dev'


class Spatiality(Enum):
    Point = 1
    Beam = 2
    Body = 3

    def __str__(self):
        return self.name.lower()

    def is_point(self):
        return self is Spatiality.Point

    def is_beam(self):
        return self is Spatiality.Beam

    def is_body(self):
        return self is Spatiality.Body


class Mobility(Enum):
    Linear = 1
    Planar = 2
    Spatial = 3

    def __str__(self):
        return self.name.lower()

    def moves_linear(self):
        return self is Mobility.Linear

    def moves_planar(self):
        return self is Mobility.Planar

    def moves_spatial(self):
        return self is Mobility.Spatial


class MotionPattern(Enum):
    _1T = '1T'
    _2T = '2T'
    _3T = '3T'
    _1R2T = '1R2T'
    _2R3T = '2R3T'
    _3R3T = '3R3T'

    @property
    def dof_linear(self):
        if self is MotionPattern._1T:
            return 1
        elif self is MotionPattern._2T:
            return 2
        elif self is MotionPattern._3T:
            return 3
        elif self is MotionPattern._1R2T:
            return 2
        elif self is MotionPattern._2R3T:
            return 3
        elif self is MotionPattern._3R3T:
            return 3

        raise AttributeError('\'MotionPattern\' object has no attribute '
                             '\'dof_linear\'')

    @property
    def dof_rotational(self):
        if self is MotionPattern._1T:
            return 0
        elif self is MotionPattern._2T:
            return 0
        elif self is MotionPattern._3T:
            return 0
        elif self is MotionPattern._1R2T:
            return 1
        elif self is MotionPattern._2R3T:
            return 3
        elif self is MotionPattern._3R3T:
            return 3

        raise AttributeError('\'MotionPattern\' object has no attribute '
                             '\'dof_rotational\'')

    @property
    def dof(self):
        try:
            return self.dof_rotational + self.dof_linear
        except AttributeError as exc:
            raise AttributeError from exc

    @property
    def spatiality(self):
        if self is MotionPattern._1T:
            return Spatiality.Point
        elif self is MotionPattern._2T:
            return Spatiality.Point
        elif self is MotionPattern._3T:
            return Spatiality.Point
        elif self is MotionPattern._1R2T:
            return Spatiality.Body
        elif self is MotionPattern._2R3T:
            return Spatiality.Beam
        elif self is MotionPattern._3R3T:
            return Spatiality.Body

    @property
    def mobility(self):
        if self is MotionPattern._1T:
            return Mobility.Linear
        elif self is MotionPattern._2T:
            return Mobility.Planar
        elif self is MotionPattern._3T:
            return Mobility.Spatial
        elif self is MotionPattern._1R2T:
            return Mobility.Planar
        elif self is MotionPattern._2R3T:
            return Mobility.Spatial
        elif self is MotionPattern._3R3T:
            return Mobility.Spatial

    def __str__(self):
        return self._value_

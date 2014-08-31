__author__ = 'michiel'

from gampy.engine.core.math3d import Vector3


class IntersectData:

    def __init__(self, does_intersect, direction):
        if not isinstance(direction, Vector3):
            direction = Vector3(direction)
        self._intersects = does_intersect
        self._direction = direction

    @property
    def does_intersect(self):
        return self._intersects

    @does_intersect.setter
    def does_intersect(self, value):
        self._intersects = value

    @property
    def distance(self):
        return self._direction.length

    @property
    def direction(self):
        return self._direction
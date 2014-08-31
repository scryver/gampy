__author__ = 'michiel'


class IntersectData:

    def __init__(self, does_intersect, distance):
        self._intersects = does_intersect
        self._distance = distance

    @property
    def does_intersect(self):
        return self._intersects

    @does_intersect.setter
    def does_intersect(self, value):
        self._intersects = value

    @property
    def distance(self):
        return self._distance

    @distance.setter
    def distance(self, value):
        self._distance = value
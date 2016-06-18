__author__ = 'michiel'

from gampy.engine.core.math3d import Vector3
from gampy.engine.core.util import ReferenceCounter


class Collider(ReferenceCounter):

    types = {
        'sphere': 0,
        'aabb': 1,
    }

    def __init__(self, type: str):
        super().__init__()
        self._type = Collider.types[type.lower()]

    @property
    def type(self):
        return self._type

    @property
    def center(self):
        return Vector3(0, 0, 0)

    def intersect(self, other):
        if self._type == other.type == Collider.types['sphere']:
            return self.intersect_sphere(other)
        elif self._type == other.type == Collider.types['aabb']:
            return self.intersect_AABB(other)

        raise NotImplementedError('Type {} and {} are not compatible for intersection'.format(type(self), type(other)))

    def transform(self, translation):
        pass

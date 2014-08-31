__author__ = 'michiel'

from gampy.engine.core.math3d import Vector3
from gampy.engine.physics.bounding import BoundingSphere, IntersectData


class PhysicsEngine:

    def __init__(self):
        self._objects = list()

    @property
    def num_objects(self):
        return len(self._objects)

    def get_object(self, index):
        return self._objects[index]

    def add_object(self, object):
        if isinstance(object, PhysicsObject):
            self._objects.append(object)

    def simulate(self, dt):
        for obj in self.all_gen():
            obj.integrate(dt)

    def handle_collisions(self):
        for obj1, obj2 in self.compare_gen():
            intersect = obj1.bounding_sphere().intersect(obj2.bounding_sphere())

            if intersect.does_intersect:
                obj1.velocity = -obj1.velocity
                obj2.velocity = -obj2.velocity


    def all_gen(self):
        for obj in self._objects:
            yield obj

    def compare_gen(self):
        num_objs = len(self._objects)
        for i in range(num_objs):
            for j in range(i + 1, num_objs):
                yield self._objects[i], self._objects[j]



class PhysicsObject:

    def __init__(self, position, velocity, radius):
        if not isinstance(position, Vector3):
            position = Vector3(position)
        if not isinstance(velocity, Vector3):
            velocity = Vector3(velocity)
        self._position = position
        self._velocity = velocity
        self._radius = radius

    @property
    def position(self):
        return self._position

    @property
    def velocity(self):
        return self._velocity

    @velocity.setter
    def velocity(self, value):
        self._velocity = value

    @property
    def radius(self):
        return self._radius

    def bounding_sphere(self):
        return BoundingSphere(self._position, self._radius)

    def integrate(self, dt):
        self._position += self._velocity * dt


def test():
    test1 = PhysicsObject([0, 1, 0], [1, 2, 3], 1.)
    test1.integrate(20.)

    test_pos = test1.position
    test_vel = test1.velocity

    assert test_pos.x == 20. and test_pos.y == 41. and test_pos.z == 60.
    assert test_vel.x == 1. and test_vel.y == 2. and test_vel.z == 3.


if __name__ == '__main__':
    test()
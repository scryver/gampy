__author__ = 'michiel'

from gampy.engine.core.math3d import Vector3
from gampy.engine.physics.bounding import BoundingSphere, IntersectData, Collider


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
            intersect = obj1.collider().intersect(obj2.collider())

            if intersect.does_intersect:
                direction = intersect.direction.normalized()
                other_direction = direction.reflect(obj1.velocity.normalized())
                obj1.velocity = obj1.velocity.reflect(other_direction)
                obj2.velocity = obj2.velocity.reflect(direction)


    def all_gen(self):
        for obj in self._objects:
            yield obj

    def compare_gen(self):
        num_objects = len(self._objects)
        for i in range(num_objects):
            for j in range(i + 1, num_objects):
                yield self._objects[i], self._objects[j]



class PhysicsObject:

    def __init__(self, collider, velocity=None):
        if isinstance(collider, PhysicsObject):
            self._collider = collider._collider
            self._position = collider.position
            self._old_position = collider.position
            self._velocity = collider.velocity
            self._collider.add_reference()
        else:
            if not isinstance(collider, Collider):
                raise TypeError('Collider argument is not a subtype of Collider, type is "{}"'.format(type(collider)))
            if not isinstance(velocity, Vector3):
                velocity = Vector3(velocity)
            self._position = collider.center
            self._old_position = self._position
            self._velocity = velocity
            self._collider = collider

    @property
    def position(self):
        return self._position

    @property
    def velocity(self):
        return self._velocity

    @velocity.setter
    def velocity(self, value):
        self._velocity = value

    def collider(self):
        difference = self._position - self._old_position
        self._old_position = self._position
        return self._collider.transform(difference)

    def integrate(self, dt):
        self._position += self._velocity * dt

    def __del__(self):
        if self._collider.remove_reference():
            del self._collider


def test():
    test1 = PhysicsObject(BoundingSphere([0, 1, 0], 1.), [1, 2, 3])
    test1.integrate(20.)

    test_pos = test1.position
    test_vel = test1.velocity

    assert test_pos.x == 20. and test_pos.y == 41. and test_pos.z == 60.
    assert test_vel.x == 1. and test_vel.y == 2. and test_vel.z == 3.


if __name__ == '__main__':
    test()
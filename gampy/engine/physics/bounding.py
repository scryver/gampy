__author__ = 'michiel'


from gampy.engine.core.math3d import Vector3
from gampy.engine.physics.intersections import IntersectData


class BoundingSphere:

    def __init__(self, center, radius):
        if not isinstance(center, Vector3):
            center = Vector3(center)
        self._center = center
        self._radius = radius

    @property
    def center(self):
        return self._center

    @property
    def radius(self):
        return self._radius

    def intersect(self, other):
        if isinstance(other, BoundingSphere):
            radius_distance = self._radius + other.radius
            center_distance = (other.center - self._center).length
            distance = center_distance - radius_distance

            return IntersectData(center_distance < radius_distance, distance)

        return NotImplemented


class AABB:
    """
    Axis Aligned Bounding Box
    """
    def __init__(self, extents):
        min_extents, max_extents = extents
        if not isinstance(min_extents, Vector3):
            min_extents = Vector3(min_extents)
        if not isinstance(min_extents, Vector3):
            max_extents = Vector3(max_extents)
        self._min_extents, self._max_extents = min_extents, max_extents

    @property
    def min_extents(self):
        return self._min_extents

    @property
    def max_extents(self):
        return self._max_extents

    def intersect(self, other):
        if isinstance(other, AABB):
            distances1 = other.min_extents - self._max_extents
            distances2 = self._min_extents - other.max_extents
            distances = Vector3.max(distances1, distances2)
            max_distance= distances.max_value()

            return IntersectData(max_distance < 0, max_distance)

        return NotImplemented


class Plane:

    def __init__(self, normal, distance):
        if not isinstance(normal, Vector3):
            normal = Vector3(normal)
        self._distance = distance
        self._normal = normal.normalized()

    @property
    def distance(self):
        return self._distance

    @property
    def normal(self):
        return self._normal

    def intersect(self, other):
        if isinstance(other, BoundingSphere):
            distance_from_sphere_center = abs(self._normal.dot(other.center) - self._distance)
            distance_from_sphere = distance_from_sphere_center - other.radius

            return IntersectData(distance_from_sphere < 0, distance_from_sphere)

        return NotImplemented


def test():
    sphere1 = BoundingSphere([0, 0, 0], 1.)
    sphere2 = BoundingSphere([0, 3, 0], 1.)
    sphere3 = BoundingSphere([0, 0, 2], 1.)
    sphere4 = BoundingSphere([1, 0, 0], 1.)

    sphere1_intersect_sphere2 = sphere1.intersect(sphere2)
    sphere1_intersect_sphere3 = sphere1.intersect(sphere3)
    sphere1_intersect_sphere4 = sphere1.intersect(sphere4)

    assert sphere1_intersect_sphere2.does_intersect == False and sphere1_intersect_sphere2.distance == 1.0
    assert sphere1_intersect_sphere3.does_intersect == False and sphere1_intersect_sphere3.distance == 0.0
    assert sphere1_intersect_sphere4.does_intersect == True and sphere1_intersect_sphere4.distance == -1.0

    aabb1 = AABB(([0, 0, 0], [1, 1, 1]))
    aabb2 = AABB(([1, 1, 1], [2, 2, 2]))
    aabb3 = AABB(([1, 0, 0], [2, 1, 1]))
    aabb4 = AABB(([0, 0, -2], [1, 1, -1]))
    aabb5 = AABB(([0, 0.5, 0], [1, 1.5, 1]))

    aabb1_intersect_aabb2 = aabb1.intersect(aabb2)
    aabb1_intersect_aabb3 = aabb1.intersect(aabb3)
    aabb1_intersect_aabb4 = aabb1.intersect(aabb4)
    aabb1_intersect_aabb5 = aabb1.intersect(aabb5)

    assert aabb1_intersect_aabb2.does_intersect == False and aabb1_intersect_aabb2.distance == 0.0
    assert aabb1_intersect_aabb3.does_intersect == False and aabb1_intersect_aabb3.distance == 0.0
    assert aabb1_intersect_aabb4.does_intersect == False and aabb1_intersect_aabb4.distance == 1.0
    assert aabb1_intersect_aabb5.does_intersect == True and aabb1_intersect_aabb5.distance == -0.5

    plane1 = Plane([0, 1, 0], 0)

    plane1_intersect_sphere1 = plane1.intersect(sphere1)
    plane1_intersect_sphere2 = plane1.intersect(sphere2)
    plane1_intersect_sphere3 = plane1.intersect(sphere3)
    plane1_intersect_sphere4 = plane1.intersect(sphere4)

    assert plane1_intersect_sphere1.does_intersect == True and plane1_intersect_sphere1.distance == -1.0
    assert plane1_intersect_sphere2.does_intersect == False and plane1_intersect_sphere2.distance == 2.0
    assert plane1_intersect_sphere3.does_intersect == True and plane1_intersect_sphere3.distance == -1.0
    assert plane1_intersect_sphere4.does_intersect == True and plane1_intersect_sphere4.distance == -1.0


if __name__ == '__main__':
    test()
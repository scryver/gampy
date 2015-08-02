__author__ = 'michiel'

# import numpy
from gampy.engine.objects.vectors import Matrix4
from gampy.core import Matrix4 as NewMatrix4
from gampy.engine.events.time import Timing

timings = Timing()


@timings
def cast_object_vertexes(vertices):
    size = len(vertices)
    num_array = []

    for i in range(size):
        num_array.append([vertices[i].pos.x,
                          vertices[i].pos.y,
                          vertices[i].pos.z])

    # num_array = [[vertices[i].pos.x, vertices[i].pos.y, vertices[i].pos.z] for i in range(size)]
    return [map(float, num_array[i]) for i in num_array]
    # return numpy.array(num_array, dtype=numpy.float32)


@timings
def cast_object_indices(indices):
    size = len(indices)
    num_array = []

    for i in range(size):
        num_array.append(indices[i])

    return [map(int, num_array[i]) for i in num_array]
    # return numpy.array(num_array, dtype=numpy.uint32)


@timings
def cast_matrix(matrix):
    try:
        return [[float(matrix.get(i, j)) for j in range(4)] for i in range(4)]
    except:
        return False

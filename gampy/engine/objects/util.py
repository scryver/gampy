__author__ = 'michiel'

# import numpy
from gampy.engine.objects.vectors import Matrix4


def cast_object_vertexes(vertices):
    size = len(vertices)
    num_array = []

    for i in range(size):
        num_array.append([vertices[i].pos.x,
                          vertices[i].pos.y,
                          vertices[i].pos.z])

    return [map(float, num_array[i]) for i in num_array]
    # return numpy.array(num_array, dtype=numpy.float32)


def cast_object_indices(indices):
    size = len(indices)
    num_array = []

    for i in range(size):
        num_array.append(indices[i])

    return [map(int, num_array[i]) for i in num_array]
    # return numpy.array(num_array, dtype=numpy.uint32)


def cast_matrix(matrix):
    if isinstance(matrix, Matrix4):
        # new_matrix = numpy.identity(4, dtype=numpy.float32)
        new_matrix = Matrix4()

        for i, j in Matrix4.item_loop():
            item = matrix.m[i][j]
            # new_matrix[i, j] = item
            new_matrix.m[i][j] = float(item)

        # return new_matrix
        return new_matrix.m

    return False

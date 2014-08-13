__author__ = 'michiel'

import numpy
from gampy.engine.objects.vectors import Matrix4

def cast_object_array(vertices):
    size = len(vertices)
    num_array = []

    for i in range(size):
        num_array.append([vertices[i].pos.x,
                          vertices[i].pos.y,
                          vertices[i].pos.z])

    return numpy.array(num_array, dtype=numpy.float32)

def cast_matrix(matrix):
    if isinstance(matrix, Matrix4):
        new_matrix = numpy.identity(4, dtype=numpy.float32)

        for i, j in Matrix4.item_loop():
            item = matrix.m[i][j]
            new_matrix[i, j] = item

        return new_matrix

    return False
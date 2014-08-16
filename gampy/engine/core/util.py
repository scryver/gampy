__author__ = 'michiel'

import numpy

from gampy.engine.core.vectors import Matrix4


def cast_object_vertexes(vertices):
    size = len(vertices)
    num_array = [[vertices[i].pos.x,
                  vertices[i].pos.y,
                  vertices[i].pos.z,
                  vertices[i].tex_coord.x,
                  vertices[i].tex_coord.y,
                  vertices[i].normal.x,
                  vertices[i].normal.y,
                  vertices[i].normal.z,
                 ] for i in range(size)]

    return numpy.array(num_array, dtype=numpy.float32)


def cast_object_indices(indices):
    return numpy.array(indices, dtype=numpy.uint32)


def cast_matrix(matrix):
    if isinstance(matrix, Matrix4):
        new_matrix = numpy.identity(4, dtype=numpy.float32)

        for i, j in Matrix4.item_loop():
            item = matrix.m[i][j]
            new_matrix[i, j] = item

        return new_matrix

    return False


def remove_empty_strings(data):
    result = []

    for i in range(len(data)):
        if data[i] != '':
            result.append(data[i])

    return result
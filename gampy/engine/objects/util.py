__author__ = 'michiel'

import numpy

def cast_object_array(vertices):
    size = len(vertices)
    num_array = []

    for i in range(size):
        num_array.append([vertices[i].pos.x,
                          vertices[i].pos.y,
                          vertices[i].pos.z])

    return numpy.array(num_array, dtype=numpy.float32)

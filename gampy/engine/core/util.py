__author__ = 'michiel'

import numpy
import numbers

def cast_object_vertexes(vertices):
    # size = len(vertices)
    # num_array = [vertices[i].get() for i in range(size)]

    return numpy.array(vertices, dtype=numpy.float32)

def cast_object_indices(indices):
    return numpy.array(indices, dtype=numpy.uint32)

def remove_empty_strings(data):
    return [data[i] for i in range(len(data)) if data[i] != '']

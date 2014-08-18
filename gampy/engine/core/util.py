__author__ = 'michiel'

import numpy
import numbers


def cast_object_vertexes(vertices):
    size = len(vertices)
    num_array = [[vertices[i].position.x,
                  vertices[i].position.y,
                  vertices[i].position.z,
                  vertices[i].tex_coord.x,
                  vertices[i].tex_coord.y,
                  vertices[i].normal.x,
                  vertices[i].normal.y,
                  vertices[i].normal.z,
                 ] for i in range(size)]

    return numpy.array(num_array, dtype=numpy.float32)

def cast_object_indices(indices):
    return numpy.array(indices, dtype=numpy.uint32)

def remove_empty_strings(data):
    result = []

    for i in range(len(data)):
        if data[i] != '':
            result.append(data[i])

    return result

def is_float(value, field_name, default=0):
    """Checks if value is a number and cast it to a float, field_name is used for error description"""
    if value is None and default is not None:
        res = float(default)
    elif isinstance(value, (numbers.Number, numpy.float32)):
        res = float(value)
    else:
        raise AttributeError('{} "{}" is not a number'.format(field_name, value))

    return res

def is_instance(value, field_name, type, default=None):
    """Checks if value is an instance of type, field_name is used for error description"""
    if value is None and default is not None:
        res = default
    elif isinstance(value, type):
        res = value
    else:
        raise AttributeError('{field} "{value}" is not a {type}'.format(field=field_name, value=value, type=type))

    return res
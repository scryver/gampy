__author__ = 'michiel'

import timeit

setup = '''
import numba
import numpy

@numba.jit('f4[:,:](f4[:,:], f4[:,:])')
def matrix44_mult(a, b):
    result = numpy.ndarray((4, 4), dtype=numpy.float32)
    for i in range(4):
        for j in range(4):
            result[i, j] = a[i, 0] * b[0, j] + a[i, 1] * b[1, j] + a[i, 2] * b[2, j] + a[i, 3] * b[3, j]

    return result
'''

setup2 = '''
import numpy

def matrix44_mult(a, b):
    return numpy.dot(a, b)
'''

setup3 = '''
import numpy

def matrix44_mult(a, b):
    return a @ b
'''

data = '''
A = numpy.random.random((4, 4))
B = numpy.random.random((4, 4))

C = numpy.array(matrix44_mult(A, B)).view(numpy.matrix)
# print(C)
'''

print(min(timeit.Timer(data, setup=setup3).repeat(7, 1000)))
print(min(timeit.Timer(data, setup=setup2).repeat(7, 1000)))

import numpy as np

def matrix44_mult_numpy(a, b):
    return np.dot(a, b)

def matrix44_mult_python(a, b):
    result = np.ndarray((4, 4), dtype=np.float32)
    for i in range(4):
        for j in range(4):
            result[i, j] = a[i, 0] * b[0, j] + a[i, 1] * b[1, j] + a[i, 2] * b[2, j] + a[i, 3] * b[3, j]

    return result

# from numba.decorators import jit

# @jit('f4[:,:](f4[:,:], f4[:,:])')
# def matrix44_mult_numba(a, b):
#     result = np.ndarray((4, 4), dtype=np.float32)
#     for i in range(4):
#         for j in range(4):
#             result[i, j] = a[i, 0] * b[0, j] + a[i, 1] * b[1, j] + a[i, 2] * b[2, j] + a[i, 3] * b[3, j]

#     return result

import linecache

def traceit(frame, event, arg):
    if event == "line":
        lineno = frame.f_lineno
        filename = frame.f_globals["__file__"]
        if (filename.endswith(".pyc") or
            filename.endswith(".pyo")):
            filename = filename[:-1]
        name = frame.f_globals["__name__"]
        line = linecache.getline(filename, lineno)
        print("{name:20}:{linenr:4}: {line}".format(name=name, linenr=lineno, line=line.rstrip()))
    return traceit

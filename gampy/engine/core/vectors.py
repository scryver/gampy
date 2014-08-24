__author__ = 'michiel'

from math import radians, tan, sin, cos
from numbers import Number
import numpy
from numpy import NaN

class Vector(numpy.ndarray):

    def __new__(subtype, shape, data, dtype=numpy.float32, buffer=None, offset=0,
                strides=None, order=None):
        obj = numpy.ndarray.__new__(subtype, shape, dtype, buffer, offset, strides,
                                    order)
        obj[:] = data
        return obj

    def __array_finalize__(self, obj):
        if obj is None: return

    @property
    def length(self):
        return numpy.sqrt(numpy.dot(self, self))

    def normalized(self):
        try:
            return numpy.nan_to_num(self / self.length).view(self.__class__)
        except ZeroDivisionError:
            return self.__class__()

    def dot(self, other):
        return numpy.dot(self, other)

    def cross(self, other):
        return numpy.cross(self, other)

    def __truediv__(self, other):
        if other == 0:
            result = None
        else:
            result = numpy.nan_to_num(super().__truediv__(other))
        return self.__class__(result)

    def __eq__(self, other):
        if other is None:
            return False
        elif isinstance(other, Vector):
            return numpy.array_equal(self, other)
        else:
            super().__eq__(other)

    def __ne__(self, other):
        return ~(self == other)


class Vector2(Vector):

    def __new__(cls, x_or_data=0., y=0.):
        if isinstance(x_or_data, Number):
            return super().__new__(cls, 2, [x_or_data, y])
        else:
            return super().__new__(cls, 2, x_or_data)

    def set(self, x, y=None):
        if isinstance(x, Vector2):
            self[:] = [x.x, x.y]
        else:
            self[:] = [x, y]

        return self

    @property
    def x(self):
        return self[0]

    @x.setter
    def x(self, value):
        self[0] = value

    @property
    def y(self):
        return self[1]
    @y.setter
    def y(self, value):
        self[1] = value

    def rotate(self, angle):
        rad = radians(angle)
        cosine = cos(rad)
        sinus = sin(rad)

        return Vector2(self.x * cosine - self.y * sinus, self.x * sinus + self.y * cosine)

    def lerp(self, destination, lerp_factor):
        return (destination - self) * lerp_factor + self # .normalized()


class Vector3(Vector):

    def __new__(cls, x_or_data=0., y=0., z=0.):
        if isinstance(x_or_data, Number):
            return super().__new__(cls, 3, [x_or_data, y, z])
        else:
            return super().__new__(cls, 3, x_or_data)

    @property
    def x(self):
        return self[0]
    @x.setter
    def x(self, value):
        self[0] = value

    @property
    def y(self):
        return self[1]
    @y.setter
    def y(self, value):
        self[1] = value

    @property
    def z(self):
        return self[2]
    @z.setter
    def z(self, value):
        self[2] = value

    def set(self, x, y=None, z=None):
        if isinstance(x, Vector3):
            self[:] = [x.x, x.y, x.z]
        else:
            self[:] = [x, y, z]

        return self

    @property
    def xy(self):
        return Vector2(self[0], self[1])
    @property
    def xz(self):
        return Vector2(self[0], self[2])
    @property
    def yx(self):
        return Vector2(self[1], self[0])
    @property
    def yz(self):
        return Vector2(self[1], self[2])
    @property
    def zx(self):
        return Vector2(self[2], self[0])
    @property
    def zy(self):
        return Vector2(self[2], self[1])

    def rotate(self, quat_or_axis, angle=None):
        if isinstance(quat_or_axis, Quaternion):
            w = quat_or_axis * self * quat_or_axis.conjugate()
            return w[:3].view(Vector3)
        elif isinstance(quat_or_axis, Vector3):
            rotate_vector_on_axis(self.view(numpy.ndarray), quat_or_axis, angle)
            return self.view(Vector3)
        else:
            return NotImplemented

    def lerp(self, destination, lerp_factor):
        return (destination - self) * lerp_factor + self #.normalized()


class Matrix4(numpy.matrix):

    def __new__(subtype, data=None, dtype=numpy.float32):
        obj = numpy.zeros((4, 4), dtype=numpy.float32).view(Matrix4)
        if data is not None:
            obj[:,:] = data
        return obj

    @property
    def m(self):
        return self.copy().view(Matrix4)

    def init_identity(self):
        self[:,:] = numpy.eye(4, 4, dtype=numpy.float32)
        return self.view(Matrix4)

    def init_translation(self, x, y, z):
        matrix_translation(self.view(numpy.ndarray), x, y, z)
        return self.view(Matrix4)

    def init_rotation(self, x, y, z=None):
        if isinstance(x, Vector3):
            if z is None:
                f = x.normalized()
                r = y.view(Vector3).normalized()
                r = r.cross(f)
                u = f.cross(r)
            else:
                f = x
                u = y
                r = z
            matrix_rotation_3ax(self.view(numpy.ndarray), f.view(numpy.ndarray), u.view(numpy.ndarray), r.view(numpy.ndarray))
        else:
            rx = Matrix4().init_identity()
            ry = Matrix4().init_identity()
            rz = Matrix4().init_identity()

            x = radians(x)
            y = radians(y)
            z = radians(z)

            rz._m[0, 0] = numpy.cos(z)
            rz._m[1, 0] = numpy.sin(z)
            rz._m[0, 1] = -numpy.sin(z)
            rz._m[1, 1] = numpy.cos(z)

            rx._m[1, 1] = numpy.cos(x)
            rx._m[2, 1] = numpy.sin(x)
            rx._m[1, 2] = -numpy.sin(x)
            rx._m[2, 2] = numpy.cos(x)

            ry._m[0, 0] = numpy.cos(y)
            ry._m[2, 0] = -numpy.sin(y)
            ry._m[0, 2] = numpy.sin(y)
            ry._m[2, 2] = numpy.cos(y)

            tmp = rz * ry * rx
            self[:,:] = tmp

        return self.view(Matrix4)

    def init_scale(self, x, y, z):
        self[0, 0] = x
        self[1, 1] = y
        self[2, 2] = z
        self[3, 3] = 1.

        return self.view(Matrix4)

    def init_perspective(self, fov, aspect_ratio, z_near, z_far):
        matrix_perspective(self, fov, aspect_ratio, z_near, z_far)
        return self.view(Matrix4)

    def init_orthographic(self, left, right, bottom, top, near, far):
        width = right - left
        height = top - bottom
        depth = far - near

        self[0, 0] = 2 / width
        self[1, 1] = 2 / height
        self[2, 2] = -2 / depth
        self[0, 3] = -(right + left) / width
        self[1, 3] = -(top + bottom) / height
        self[2, 3] = -(far + near) / depth
        self[3, 3] = 1.

        return self.view(Matrix4)

    def transform(self, other, w_offset=1.):
        result =  numpy.empty(3, dtype=numpy.float32)
        matrix_transform(self.view(numpy.ndarray), other.view(numpy.ndarray), w_offset, result)
        return Vector3(result)

    def __mul__(self, other):
        if isinstance(other, Matrix4):
            result =  numpy.empty((4, 4), dtype=numpy.float32)
            matrix_mul(self.view(numpy.ndarray), other.view(numpy.ndarray), result)
            return Matrix4(result)

        return NotImplemented

    def get(self, x, y):
        return self[x, y]

    def set(self, x, y, value):
        self[x, y] = value


class Quaternion(Vector):

    EPSILON = 1e3

    def __new__(cls, x=None, y=None, z=None, w=None):
        """
        all depends on x, if x is None then a default Quaternion will be created
        if x is a Vector3 it is assumed to be the axis and y the rotation angle

        :param x: None, Number or Vector3 'axis'
        :param y: None, Number or number 'angle'
        :param z:
        :param w:
        :return:
        """
        data = [0, 0, 0, 1]
        if x is not None:
            if isinstance(x, Matrix4):
                data =  numpy.empty(4, dtype=numpy.float32)
                quat_from_matrix(x.view(numpy.ndarray), data)
            elif isinstance(x, Vector3):
                sin_half_angle = sin(y / 2)
                cos_half_angle = cos(y / 2)

                data = [x.x * sin_half_angle, x.y * sin_half_angle, x.z * sin_half_angle, cos_half_angle]
            elif isinstance(x, Quaternion):
                data = x.copy()
            elif isinstance(x, numpy.ndarray):
                data[:x.size] = x
            else:
                data = [x, y, z, w]

        return super().__new__(cls, 4, data)

    def conjugate(self):
        return Quaternion(-self.x, -self.y, -self.z, self.w)

    def to_rotation_matrix(self):
        forward =  numpy.empty(3, dtype=numpy.float32)
        up =  numpy.empty(3, dtype=numpy.float32)
        right =  numpy.empty(3, dtype=numpy.float32)
        quat_to_matrix(self.view(numpy.ndarray), forward, up, right)
        return Matrix4().init_rotation(forward.view(Vector3), up.view(Vector3), right.view(Vector3))

    def set(self, x, y=None, z=None, w=None):
        if isinstance(x, Quaternion):
            self[:] = x.copy()
        else:
            self[:] = [x, y, z, w]

        return self

    @property
    def x(self):
        return self[0]
    @x.setter
    def x(self, value):
        self[0] = value

    @property
    def y(self):
        return self[1]
    @y.setter
    def y(self, value):
        self[1] = value

    @property
    def z(self):
        return self[2]
    @z.setter
    def z(self, value):
        self[2] = value

    @property
    def w(self):
        return self[3]
    @w.setter
    def w(self, value):
        self[3] = value

    @property
    def forward(self):
        return Vector3(0, 0, 1).rotate(self)

    @property
    def back(self):
        return Vector3(0, 0, -1).rotate(self)

    @property
    def up(self):
        return Vector3(0, 1, 0).rotate(self)

    @property
    def down(self):
        return Vector3(0, -1, 0).rotate(self)

    @property
    def right(self):
        return Vector3(1, 0, 0).rotate(self)

    @property
    def left(self):
        return Vector3(-1, 0, 0).rotate(self)

    def __mul__(self, other):
        if isinstance(other, Quaternion):
            result =  numpy.empty(4, dtype=numpy.float32)
            quaternion_mult(self.view(numpy.ndarray), other.view(numpy.ndarray), result)
            return Quaternion(result)
        elif isinstance(other, Vector3):
            result =  numpy.empty(4, dtype=numpy.float32)
            quat_vec3_mult(self.view(numpy.ndarray), other.view(numpy.ndarray), result)
            return Quaternion(result)
        elif isinstance(other, Number):
            return Quaternion(super().__mul__(other))
        else:
            super().__mul__(other)

    # Normalized Linear Interpelation
    def nlerp(self, destination, lerp_factor, shortest=True):
        result = numpy.ndarray(4, dtype=numpy.float32)
        quat_nlerp(self.view(numpy.ndarray), destination.view(numpy.ndarray), lerp_factor, result, shortest)
        return result.view(Quaternion).normalized()

    def slerp(self, destination, lerp_factor, shortest=True):
        return quat_slerp(self.view(numpy.ndarray), destination.view(numpy.ndarray), lerp_factor, Quaternion.EPSILON, shortest).view(Quaternion)

from numba import jit, float32

@jit('void(f4[:,:], f4[:,:], f4[:,:])', nopython=True)
def matrix_mul(A, B, result):
    for i in range(4):
        for j in range(4):
            result[i, j] = 0.
            for k in range(4):
                result[i, j] += A[i, k] * B[k, j]

@jit('void(f4[:,:], f4[:], f4, f4[:])', nopython=True)
def matrix_transform(A, B, offset, result):
    for i in range(3):
        result[i] = A[i, 0] * B[0] + A[i, 1] * B[1] + A[i, 2] * B[2] + A[i, 3] * offset

@jit('void(f4[:], f4[:], f4[:])', nopython=True)
def quaternion_mult(a, b, result):
    result[0] = a[0] * b[3] + a[3] * b[0] + a[1] * b[2] - a[2] * b[1]
    result[1] = a[1] * b[3] + a[3] * b[1] + a[2] * b[0] - a[0] * b[2]
    result[2] = a[2] * b[3] + a[3] * b[2] + a[0] * b[1] - a[1] * b[0]
    result[3] = a[3] * b[3] - a[0] * b[0] - a[1] * b[1] - a[2] * b[2]

@jit('void(f4[:], f4[:], f4[:])', nopython=True)
def quat_vec3_mult(a, b, result):
    result[0] =  a[3] * b[0] + a[1] * b[2] - a[2] * b[1]
    result[1] =  a[3] * b[1] + a[2] * b[0] - a[0] * b[2]
    result[2] =  a[3] * b[2] + a[0] * b[1] - a[1] * b[0]
    result[3] = -a[0] * b[0] - a[1] * b[1] - a[2] * b[2]

@jit('void(f4[:,:], f4[:])', nopython=True)
def quat_from_matrix(M, result):
    trace = M[0, 0]  + M[1, 1] + M[2, 2]
    s = 0.
    if trace > 0:
        s = 0.5 / numpy.sqrt(trace + 1)
        result[0] = (M[1, 2] - M[2, 1]) * s
        result[1] = (M[2, 0] - M[0, 2]) * s
        result[2] = (M[0, 1] - M[1, 0]) * s
        result[3] = 0.25 / s
    else:
        s = 2 * numpy.sqrt(1 + M[0, 0] - M[1, 1] - M[2, 2])
        if M[0, 0] > M[1, 1] and M[0, 0] > M[2, 2]:
            result[0] = 0.25 * s
            result[1] = (M[1, 0] + M[0, 1]) / s
            result[2] = (M[2, 0] + M[0, 2]) / s
            result[3] = (M[1, 2] - M[2, 1]) / s
        elif M[1, 1] > M[2, 2]:
            result[0] = (M[1, 0] + M[0, 1]) / s
            result[1] = 0.25 * s
            result[2] = (M[2, 1] + M[1, 2]) / s
            result[3] = (M[2, 0] - M[0, 2]) / s
        else:
            result[0] = (M[2, 0] + M[0, 2]) / s
            result[1] = (M[1, 2] + M[2, 1]) / s
            result[2] = 0.25 * s
            result[3] = (M[0, 1] - M[1, 0]) / s

    summed = 0.
    for i in range(4):
        summed += result[i] * result[i]
    length = numpy.sqrt(summed)

    result[0] = result[0] / length
    result[1] = result[1] / length
    result[2] = result[2] / length
    result[3] = result[3] / length
    
@jit('void(f4[:], f4[:], f4[:], f4[:])', nopython=True)
def quat_to_matrix(quat, forward, up, right):
    forward[0] = 2 * (quat[0] * quat[2] - quat[3] * quat[1])
    forward[1] = 2 * (quat[1] * quat[2] + quat[3] * quat[0])
    forward[2] = 1 - 2 * (quat[0] * quat[0] + quat[1] * quat[1])
    up[0] = 2 * (quat[0] * quat[1] + quat[3] * quat[2])
    up[1] = 1 - 2 * (quat[0] * quat[0] + quat[2] * quat[2])
    up[2] = 2 * (quat[1] * quat[2] - quat[3] * quat[0])
    right[0] = 1 - 2 * (quat[1] * quat[1] + quat[2] * quat[2])
    right[1] = 2 * (quat[0] * quat[1] - quat[3] * quat[2])
    right[2] = 2 * (quat[0] * quat[2] + quat[3] * quat[1])

@jit('void(f4[:,:], f4, f4, f4)', nopython=True)
def matrix_translation(M, x, y, z):
    M[0, 0] = 1.
    M[0, 1] = 0.
    M[0, 2] = 0.
    M[0, 3] = x
    M[1, 0] = 0.
    M[1, 1] = 1.
    M[1, 2] = 0.
    M[1, 3] = y
    M[2, 0] = 0.
    M[2, 1] = 0.
    M[2, 2] = 1.
    M[2, 3] = z
    M[3, 0] = 0.
    M[3, 1] = 0.
    M[3, 2] = 0.
    M[3, 3] = 1.

@jit('void(f4[:,:], f4, f4, f4, f4)', nopython=True)
def matrix_perspective(M, fov, aspect_ratio, z_near, z_far):
    tan_half_fov = tan(fov / 2)
    z_range = z_near - z_far

    x = 1 / (tan_half_fov * aspect_ratio)
    y = 1 / tan_half_fov
    z = (-z_near - z_far) / z_range
    zw = 2 * z_far * z_near / z_range

    M[0, 0] = x
    M[0, 1] = 0.
    M[0, 2] = 0.
    M[0, 3] = 0.
    M[1, 0] = 0.
    M[1, 1] = y
    M[1, 2] = 0.
    M[1, 3] = 0.
    M[2, 0] = 0.
    M[2, 1] = 0.
    M[2, 2] = z
    M[2, 3] = zw
    M[3, 0] = 0.
    M[3, 1] = 0.
    M[3, 2] = 1.
    M[3, 3] = 0.

@jit('void(f4[:,:], f4[:], f4[:], f4[:])', nopython=True)
def matrix_rotation_3ax(M, forward, up, right):
    M[0, 0] = right[0]
    M[0, 1] = right[1]
    M[0, 2] = right[2]
    M[0, 3] = 0.
    M[1, 0] = up[0]
    M[1, 1] = up[1]
    M[1, 2] = up[2]
    M[1, 3] = 0.
    M[2, 0] = forward[0]
    M[2, 1] = forward[1]
    M[2, 2] = forward[2]
    M[2, 3] = 0.
    M[3, 0] = 0.
    M[3, 1] = 0.
    M[3, 2] = 0.
    M[3, 3] = 1

@jit('void(f4[:], f4[:], f4[:])', nopython=True)
def vec3_cross(a, b, result):
    result[0] = a[1] * b[2] - a[2] * b[1]
    result[1] = a[2] * b[0] - a[0] * b[2]
    result[2] = a[0] * b[1] - a[1] * b[0]

@jit('void(f4[:], f4[:], f4[:])', nopython=True)
def vec3_mul(a, b, result):
    for i in range(3):
        result[i] = a[i] * b[i]

@jit('void(f4[:], f4[:], f4[:])', nopython=True)
def vec4_mul(a, b, result):
    for i in range(4):
        result[i] = a[i] * b[i]

@jit('void(f4[:], f4, f4[:])', nopython=True)
def vec3_mul_scalar(a, b, result):
    for i in range(3):
        result[i] = a[i] * b

@jit('void(f4[:], f4, f4[:])', nopython=True)
def vec4_mul_scalar(a, b, result):
    for i in range(4):
        result[i] = a[i] * b

@jit('f4(f4[:], f4[:])', nopython=True, locals=dict(result=float32))
def vec3_dot(a, b):
    result = 0.
    for i in range(3):
        result += a[i] * b[i]
    return result

@jit('f4(f4[:], f4[:])', nopython=True, locals=dict(result=float32))
def vec4_dot(a, b):
    result = 0.
    for i in range(4):
        result += a[i] * b[i]
    return result

@jit('void(f4[:], f4[:], f4[:])', nopython=True)
def vec4_add(a, b, result):
    for i in range(4):
        result[i] = a[i] + b[i]

@jit('void(f4[:], f4, f4[:])', nopython=True)
def vec4_add_scalar(a, b, result):
    for i in range(4):
        result[i] = a[i] + b

@jit('void(f4[:], f4[:], f4[:])', nopython=True)
def vec4_sub(a, b, result):
    for i in range(4):
        result[i] = a[i] - b[i]

@jit('void(f4[:], f4[:], f4)', nopython=True)
def rotate_vector_on_axis(vec, axis, angle):
    a = vec
    b = a
    c = a
    d = a
    e = a
    vec3_mul_scalar(axis, -numpy.sin(angle), b)
    vec3_mul_scalar(a, numpy.cos(angle), c)
    vec3_mul_scalar(axis, 1 - numpy.cos(angle), d)
    vec3_mul_scalar(axis, vec3_dot(a, d), e)
    # b = axis * -numpy.sin(angle) + a * numpy.cos(angle) + axis * numpy.dot(a, axis * (1 - numpy.cos(angle)))
    # rotate on local x + rotate on local z + rotate on local y
    vec3_cross(a, e, vec)

@jit('void(f4[:], f4[:], f4, f4[:], b1)', nopython=True, locals=dict(a=float32[:], b=float32[:]))
def quat_nlerp(quat, destination, lerp_factor, result, shortest=True):
    corrected_dest = destination

    if shortest and (vec4_dot(quat, destination) < 0):
        for i in range(4):
            corrected_dest[i] = -destination[i]

    a = destination
    b = destination
    vec4_sub(corrected_dest, quat, a)
    vec4_mul_scalar(a, lerp_factor, b)

    vec4_add(b, quat, result)

@jit('f4[:](f4[:], f4[:], f4, f4, b1)')
def quat_slerp(quat, destination, lerp_factor, epsilon, shortest=True):
    cosine = vec4_dot(quat, destination)
    corrected_dest = destination

    if shortest and cosine < 0:
        cosine = -cosine
        corrected_dest[0] = -destination[0]
        corrected_dest[1] = -destination[1]
        corrected_dest[2] = -destination[2]
        corrected_dest[3] = -destination[3]

    if abs(cosine) >= 1 - epsilon:
        quat_nlerp(quat, corrected_dest, lerp_factor, destination, False)
        return destination

    sine = numpy.sqrt(1 - cosine * cosine)
    angle = numpy.arctan2(sine, cosine)
    inv_sine = 1 / sine

    src_factor = numpy.sin((1 - lerp_factor) * angle) * inv_sine
    dest_factor = numpy.sin(lerp_factor * angle) * inv_sine

    return quat * src_factor + corrected_dest * dest_factor

@jit('b1(f4[:], f4[:], i4)', nopython=True)
def vec_equal(a, b, size):
    for i in range(size):
        if a[i] != b[i]:
            return False
    return True

@jit('b1(f4[:,:], f4[:,:])', nopython=True)
def matrix44_equal(a, b):
    for i in range(4):
        for j in range(4):
            if a[i, j] != b[i, j]:
                return False
    return True

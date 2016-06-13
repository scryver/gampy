#!/usr/bin/env python

from math import radians, tan, sin, cos
from numbers import Number
import numpy


__author__ = 'michiel'


class Vector(numpy.ndarray):

    def __new__(subtype, shape, data, dtype=numpy.float32, buffer=None,
                offset=0, strides=None, order=None):
        # print("New {}({})".format(subtype, data))
        obj = numpy.ndarray.__new__(subtype, shape, dtype, buffer, offset,
                                    strides, order)
        try:
            obj[:] = data
        except TypeError:
            obj[:] = list(data)
        return obj

    def __array_finalize__(self, obj):
        if obj is None:
            return

    @property
    def length(self):
        return numpy.sqrt(numpy.dot(self, self))

    def normalized(self):
        if self.length == 0:
            return self.__class__()
        else:
            return (self / self.length).view(self.__class__)

    def dot(self, other):
        return numpy.dot(self, other)

    def cross(self, other):
        return numpy.cross(self, other)

    def reflect(self, normal):
        return (self - (normal * (numpy.dot(self, normal) * 2))).view(
            self.__class__)

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

    def max_value(self):
        max = self[0]
        for i in range(1, self.size):
            if self[i] > max:
                max = self[i]

        return max

    @classmethod
    def max(cls, self, other):
        result = cls()
        for i in range(self.size):
            result[i] = self[i] if self[i] >= other[i] else other[i]
        return result


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

        return Vector2(self.x * cosine - self.y * sinus,
                       self.x * sinus + self.y * cosine)

    def lerp(self, destination, lerp_factor):
        return (destination - self) * lerp_factor + self  # .normalized()


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
            a = self
            # b = a
            # c = a
            d = a
            e = a
            # b = [quat_or_axis[i] * -numpy.sin(angle) for i in range(3)]
            # c = [a[i] * numpy.cos(angle) for i in range(3)]
            d = [quat_or_axis[i] * 1 - numpy.cos(angle) for i in range(3)]
            e = [quat_or_axis[i] * a.dot(d) for i in range(3)]
            # b = quat_or_axis * -numpy.sin(angle) + a * numpy.cos(angle) \
            #     + quat_or_axis * numpy.dot(a, quat_or_axis * (1 - numpy.cos(angle)))
            # rotate on local x + rotate on local z + rotate on local y

            # vec3_cross(a, e, self)
            self = a.cross(e)
            # self[0] = a[1] * e[2] - a[2] * e[1]
            # self[1] = a[2] * e[0] - a[0] * e[2]
            # self[2] = a[0] * e[1] - a[1] * e[0]
            return self.view(Vector3)
        else:
            return NotImplemented

    def lerp(self, destination, lerp_factor):
        return (destination - self) * lerp_factor + self  # .normalized()


class Matrix4(numpy.matrix):

    def __new__(subtype, data=None, dtype=numpy.float32):
        obj = numpy.zeros((4, 4), dtype=numpy.float32).view(Matrix4)
        if data is not None:
            if isinstance(data, (list, tuple)):
                for i, row in enumerate(data):
                    obj[i, :] = row
            else:
                obj[:, :] = data
        return obj

    @property
    def m(self):
        return self.copy().view(Matrix4)

    def init_identity(self):
        self[:, :] = numpy.eye(4, 4, dtype=numpy.float32)
        return self.view(Matrix4)

    def init_translation(self, x, y, z):
        self[:, :] = numpy.eye(4, 4, dtype=numpy.float32)
        self[0, 3] = x
        self[1, 3] = y
        self[2, 3] = z
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
            self[0, 0] = r[0]
            self[0, 1] = r[1]
            self[0, 2] = r[2]
            self[1, 0] = u[0]
            self[1, 1] = u[1]
            self[1, 2] = u[2]
            self[2, 0] = f[0]
            self[2, 1] = f[1]
            self[2, 2] = f[2]
            self[3, 3] = 1
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
            self[:, :] = tmp

        return self.view(Matrix4)

    def init_scale(self, x, y, z):
        self[0, 0] = x
        self[1, 1] = y
        self[2, 2] = z
        self[3, 3] = 1.

        return self.view(Matrix4)

    def init_perspective(self, fov, aspect_ratio, z_near, z_far):
        tan_half_fov = tan(fov / 2)
        z_range = z_near - z_far

        x = 1 / (tan_half_fov * aspect_ratio)
        y = 1 / tan_half_fov
        z = (-z_near - z_far) / z_range
        zw = 2 * z_far * z_near / z_range

        self[0, 0] = x
        self[1, 1] = y
        self[2, 2] = z
        self[2, 3] = zw
        self[3, 2] = 1.
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
        return Vector3(self[i, 0] * other[0]
                       + self[i, 1] * other[1]
                       + self[i, 2] * other[2]
                       + self[i, 3] * w_offset for i in range(3))

    def __mul__(self, other):
        if isinstance(other, Matrix4):
            return Matrix4(
                [
                    [
                        sum(self[i, k] * other[k, j] for k in range(4))
                        for j in range(4)
                    ] for i in range(4)
                ])

        raise NotImplementedError()

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
                data = cls._from_matrix(x)
            elif isinstance(x, Vector3):
                sin_half_angle = sin(y / 2)
                cos_half_angle = cos(y / 2)

                data = [x.x * sin_half_angle, x.y * sin_half_angle,
                        x.z * sin_half_angle, cos_half_angle]
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
        forward = Vector3()
        up = Vector3()
        right = Vector3()
        forward[0] = 2 * (self[0] * self[2] - self[3] * self[1])
        forward[1] = 2 * (self[1] * self[2] + self[3] * self[0])
        forward[2] = 1 - 2 * (self[0] * self[0] + self[1] * self[1])
        up[0] = 2 * (self[0] * self[1] + self[3] * self[2])
        up[1] = 1 - 2 * (self[0] * self[0] + self[2] * self[2])
        up[2] = 2 * (self[1] * self[2] - self[3] * self[0])
        right[0] = 1 - 2 * (self[1] * self[1] + self[2] * self[2])
        right[1] = 2 * (self[0] * self[1] - self[3] * self[2])
        right[2] = 2 * (self[0] * self[2] + self[3] * self[1])
        return Matrix4().init_rotation(forward, up, right)

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
            result = numpy.empty(4, dtype=numpy.float32)
            result[0] = self[0] * other[3] + self[3] * other[0] \
                + self[1] * other[2] - self[2] * other[1]
            result[1] = self[1] * other[3] + self[3] * other[1] \
                + self[2] * other[0] - self[0] * other[2]
            result[2] = self[2] * other[3] + self[3] * other[2] \
                + self[0] * other[1] - self[1] * other[0]
            result[3] = self[3] * other[3] - self[0] * other[0] \
                - self[1] * other[1] - self[2] * other[2]
            return Quaternion(result)
        elif isinstance(other, Vector3):
            result = numpy.empty(4, dtype=numpy.float32)
            result[0] = self[3] * other[0] + self[1] * other[2] \
                - self[2] * other[1]
            result[1] = self[3] * other[1] + self[2] * other[0] \
                - self[0] * other[2]
            result[2] = self[3] * other[2] + self[0] * other[1] \
                - self[1] * other[0]
            result[3] = -self[0] * other[0] - self[1] * other[1] \
                - self[2] * other[2]
            return Quaternion(result)
        elif isinstance(other, Number):
            return Quaternion(super().__mul__(other))
        else:
            super().__mul__(other)

    # Normalized Linear Interpelation
    def nlerp(self, destination, lerp_factor, shortest=True):
        corrected_dest = destination

        if shortest and (self.dot(destination) < 0):
            corrected_dest = [-destination[i] for i in range(4)]

        a = corrected_dest - self

        return Quaternion([a[i] * lerp_factor for i in range(4)] + self).normalized()

    def slerp(self, destination, lerp_factor, shortest=True):
        cosine = self.dot(destination)
        corrected_dest = destination

        if shortest and cosine < 0:
            cosine = -cosine
            corrected_dest[0] = -destination[0]
            corrected_dest[1] = -destination[1]
            corrected_dest[2] = -destination[2]
            corrected_dest[3] = -destination[3]

        if abs(cosine) >= 1 - Quaternion.epsilon:
            return self.nlerp(corrected_dest, lerp_factor, False)

        sine = numpy.sqrt(1 - cosine * cosine)
        angle = numpy.arctan2(sine, cosine)
        inv_sine = 1 / sine

        src_factor = numpy.sin((1 - lerp_factor) * angle) * inv_sine
        dest_factor = numpy.sin(lerp_factor * angle) * inv_sine

        return (self * src_factor
                + corrected_dest * dest_factor).view(Quaternion)

    @classmethod
    def _from_matrix(self, matrix):
        result = [0.] * 4
        trace = matrix[0, 0] + matrix[1, 1] + matrix[2, 2]
        s = 0.

        if trace <= 0:
            s = 2 * numpy.sqrt(1 + matrix[0, 0] - matrix[1, 1] - matrix[2, 2])
            if matrix[0, 0] > matrix[1, 1] and matrix[0, 0] > matrix[2, 2]:
                result[0] = 0.25 * s
                result[1] = (matrix[1, 0] + matrix[0, 1]) / s
                result[2] = (matrix[2, 0] + matrix[0, 2]) / s
                result[3] = (matrix[1, 2] - matrix[2, 1]) / s
            elif matrix[1, 1] > matrix[2, 2]:
                result[0] = (matrix[1, 0] + matrix[0, 1]) / s
                result[1] = 0.25 * s
                result[2] = (matrix[2, 1] + matrix[1, 2]) / s
                result[3] = (matrix[2, 0] - matrix[0, 2]) / s
            else:
                result[0] = (matrix[2, 0] + matrix[0, 2]) / s
                result[1] = (matrix[1, 2] + matrix[2, 1]) / s
                result[2] = 0.25 * s
                result[3] = (matrix[0, 1] - matrix[1, 0]) / s
        else:
            s = 0.5 / numpy.sqrt(trace + 1)
            result[0] = (matrix[1, 2] - matrix[2, 1]) * s
            result[1] = (matrix[2, 0] - matrix[0, 2]) * s
            result[2] = (matrix[0, 1] - matrix[1, 0]) * s
            result[3] = 0.25 / s

        summed = 0.
        for i in range(4):
            summed += result[i] * result[i]
        length = numpy.sqrt(summed)

        result[0] = result[0] / length
        result[1] = result[1] / length
        result[2] = result[2] / length
        result[3] = result[3] / length

        return result

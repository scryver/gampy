__author__ = 'michiel'

from math import radians, tan, sin, cos
from numbers import Number, Integral
import numpy
from numpy import sqrt
import gampy.engine.core.util as core_util


class Vector:

    def __init__(self, data):
        if isinstance(data, Integral):
            """data is a number so we use it to set the size of the vector"""
            data = [0. for i in range(data)]
        self._array = numpy.array(data, dtype=numpy.float32)

    @property
    def length(self):
        return numpy.sqrt(self._array.dot(self._array))

    def normalized(self):
        try:
            return self / self.length
        except ZeroDivisionError:
            return self.__class__()

    def dot(self, other):
        return numpy.dot(self._array, other._array)

    def cross(self, other):
        result = numpy.cross(self._array, other._array)
        if isinstance(result, (Number, numpy.float32)):
            return result
        else:
            return self.__class__(result)

    def __add__(self, other):
        if isinstance(other, Vector):
            result = self._array + other._array
        else:
            result = self._array + other
        return self.__class__(result)

    def __sub__(self, other):
        if isinstance(other, Vector):
            result = self._array - other._array
        else:
            result = self._array - other
        return self.__class__(result)

    def __mul__(self, other):
        if isinstance(other, Vector):
            result = self._array * other._array
        else:
            result = self._array * other
        return self.__class__(result)

    def __truediv__(self, other):
        if other == 0:
            result = None
        elif isinstance(other, Vector):
            result = self._array / other._array
        else:
            result = self._array / other
        return self.__class__(result)

    def __eq__(self, other):
        if isinstance(other, Vector):
            return numpy.array_equal(self._array, other._array)
        else:
            return numpy.all(self._array == other)

    def __ne__(self, other):
        if isinstance(other, Vector):
            return numpy.any(self._array != other._array)
        else:
            return numpy.any(self._array != other)

    def __abs__(self):
        result = abs(self._array)
        return self.__class__(result)

    def max(self):
        return max(self._array)

    def min(self):
        return min(self._array)

    def __str__(self):
        return str(self._array)

    def copy(self):
        return self.__class__(self._array)


class Vector2(Vector):

    def __init__(self, x_or_data=0., y=0.):
        super().__init__(2)
        try:
            self._array[:] = [x_or_data, y]
        except ValueError:
            self._array[:] = x_or_data

    def set(self, x, y=None):
        if isinstance(x, Vector2):
            self._array[:] = [x.x, x.y]
        else:
            self._array[:] = [x, y]

        return self

    @property
    def x(self):
        return self._array[0]
    @x.setter
    def x(self, value):
        self._array[0] = value

    @property
    def y(self):
        return self._array[1]
    @y.setter
    def y(self, value):
        self._array[1] = value

    def rotate(self, angle):
        rad = radians(angle)
        cosine = cos(rad)
        sinus = sin(rad)

        return Vector2(self.x * cosine - self.y * sinus, self.x * sinus + self.y * cosine)

    def lerp(self, destination, lerp_factor):
        lerp_factor = core_util.is_float(lerp_factor, 'Lerp Factor')
        destination = core_util.is_instance(destination, 'Destination', Vector2)

        return (destination - self) * lerp_factor + self



class Vector3(Vector):

    def __init__(self, x_or_data=0., y=0., z=0.):
        super().__init__(3)
        try:
            self._array[:] = [x_or_data, y, z]
        except ValueError:
            self._array[:] = x_or_data

    @property
    def x(self):
        return self._array[0]
    @x.setter
    def x(self, value):
        self._array[0] = value

    @property
    def y(self):
        return self._array[1]
    @y.setter
    def y(self, value):
        self._array[1] = value

    @property
    def z(self):
        return self._array[2]
    @z.setter
    def z(self, value):
        self._array[2] = value

    def set(self, x, y=None, z=None):
        if isinstance(x, Vector3):
            self._array[:] = [x.x, x.y, x.z]
        else:
            self._array[:] = [x, y, z]

        return self

    @property
    def xy(self):
        return Vector2(self._array[0], self._array[1])
    @property
    def xz(self):
        return Vector2(self._array[0], self._array[2])
    @property
    def yx(self):
        return Vector2(self._array[1], self._array[0])
    @property
    def yz(self):
        return Vector2(self._array[1], self._array[2])
    @property
    def zx(self):
        return Vector2(self._array[2], self._array[0])
    @property
    def zy(self):
        return Vector2(self._array[2], self._array[1])

    def rotate(self, quat_or_axis, angle=None):
        if isinstance(quat_or_axis, Quaternion):
            w = quat_or_axis * self * quat_or_axis.conjugate()

            return Vector3(w.x, w.y, w.z)
        elif isinstance(quat_or_axis, Vector3):
            # rotate on local x + rotate on local z + rotate on local y
            return self.cross(quat_or_axis * -sin(angle)) + \
                   self * cos(angle) + \
                   quat_or_axis * self.dot(quat_or_axis * (1 - cos(angle)))
        else:
            return NotImplemented

    def lerp(self, destination, lerp_factor):
        return (destination - self) * lerp_factor + self


class Matrix4:

    def __init__(self):
        self._m = numpy.zeros((4, 4), dtype=numpy.float32).view(numpy.matrix)

    @property
    def m(self):
        return self._m

    def init_identity(self):
        self._m = numpy.eye(4, 4, dtype=numpy.float32).view(numpy.matrix)

        return self

    def init_translation(self, x, y, z):
        self.init_identity()
        self._m[0:3, 3] = [[x], [y], [z]]

        return self

    def init_rotation(self, x, y, z=None):
        if isinstance(x, Vector3):
            if z is None:
            # DONT KNOW IF THIS IS NECESSARY
                f = x.normalized()
                r = y.normalized()
                r = r.cross(f)
                u = f.cross(r)
            # END OF DONT KNOW
            else:
                f = x # forward
                u = y # up
                r = z # right

            self._m[0, 0:3] = [r.x, r.y, r.z]
            self._m[1, 0:3] = [u.x, u.y, u.z]
            self._m[2, 0:3] = [f.x, f.y, f.z]
            self._m[3, 3] = 1.
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
            self._m = tmp._m

        return self

    def init_scale(self, x, y, z):
        self._m[0, 0] = x
        self._m[1, 1] = y
        self._m[2, 2] = z
        self._m[3, 3] = 1.

        return self

    def init_perspective(self, fov, aspect_ratio, z_near, z_far):
        tan_half_fov = tan(fov / 2)
        z_range = z_near - z_far

        x = 1 / (tan_half_fov * aspect_ratio)
        y = 1 / tan_half_fov
        z = (-z_near - z_far) / z_range
        zw = 2 * z_far * z_near / z_range

        self._m[0, 0] = x
        self._m[1, 1] = y
        self._m[2, 2] = z
        self._m[2, 3] = zw
        self._m[3, 2] = 1.
        return self

    def init_orthographic(self, left, right, bottom, top, near, far):
        left = core_util.is_float(left, 'Left')
        right = core_util.is_float(right, 'Right')
        bottom = core_util.is_float(bottom, 'Bottom')
        top = core_util.is_float(top, 'Top')
        near = core_util.is_float(near, 'Near')
        far = core_util.is_float(far, 'Far')

        width = right - left
        height = top - bottom
        depth = far - near

        self._m[0, 0] = 2 / width
        self._m[1, 1] = 2 / height
        self._m[2, 2] = -2 / depth
        self._m[0, 3] = -(right + left) / width
        self._m[1, 3] = -(top + bottom) / height
        self._m[2, 3] = -(far + near) / depth
        self._m[3, 3] = 1.

        return self

    def transform(self, other, w_offset=1.):
        return Vector3(self._m[0, 0] * other.x + self._m[0, 1] * other.y + self._m[0, 2] * other.z + self._m[0, 3] * w_offset,
                       self._m[1, 0] * other.x + self._m[1, 1] * other.y + self._m[1, 2] * other.z + self._m[1, 3] * w_offset,
                       self._m[2, 0] * other.x + self._m[2, 1] * other.y + self._m[2, 2] * other.z + self._m[2, 3] * w_offset)

    def __mul__(self, other):
        if isinstance(other, Matrix4):
            res = Matrix4()
            res._m = self._m * other._m
            return res

        return NotImplemented

    def get(self, x, y):
        return self._m[x, y]

    def set(self, x, y, value):
        self._m[x, y] = value

    def __str__(self):
        return str(self._m)


class Quaternion(Vector):

    def __init__(self, x=None, y=None, z=None, w=None):
        """
        all depends on x, if x is None then a default Quaternion will be created
        if x is a Vector3 it is assumed to be the axis and y the rotation angle

        :param x: None, Number or Vector3 'axis'
        :param y: None, Number or number 'angle'
        :param z:
        :param w:
        :return:
        """
        super().__init__(4)
        if x is None:
            self._array[3] = 1.
        elif isinstance(x, Vector3):
            sin_half_angle = sin(y / 2)
            cos_half_angle = cos(y / 2)

            w = cos_half_angle
            z = x.z * sin_half_angle
            y = x.y * sin_half_angle
            x = x.x * sin_half_angle
            self._array[:] = [x, y, z, w]
        elif isinstance(x, Quaternion):
            self._array = x._array.copy()
        elif isinstance(x, numpy.ndarray):
            self._array[:x.size] = x
        else:
            self._array[:] = [x, y, z, w]


    def conjugate(self):
        return Quaternion(-self.x, -self.y, -self.z, self.w)

    def to_rotation_matrix(self):
        forward = Vector3(2 * (self.x * self.z - self.w * self.y),
                       2 * (self.y * self.z + self.w * self.x),
                       1 - 2 * (self.x * self.x + self.y * self.y))
        up = Vector3(2 * (self.x * self.y + self.w * self.z),
                       1 - 2 * (self.x * self.x + self.z * self.z),
                       2 * (self.y * self.z - self.w * self.x))
        right = Vector3(1 - 2 * (self.y * self.y + self.z * self.z),
                       2 * (self.x * self.y - self.w * self.z),
                       2 * (self.x * self.z + self.w * self.y))
        return Matrix4().init_rotation(forward, up, right)

    def set(self, x, y=None, z=None, w=None):
        if isinstance(x, Quaternion):
            self._array = x._array.copy()
        else:
            self._array[:] = [x, y, z, w]

        return self

    @property
    def x(self):
        return self._array[0]
    @x.setter
    def x(self, value):
        self._array[0] = value

    @property
    def y(self):
        return self._array[1]
    @y.setter
    def y(self, value):
        self._array[1] = value

    @property
    def z(self):
        return self._array[2]
    @z.setter
    def z(self, value):
        self._array[2] = value

    @property
    def w(self):
        return self._array[3]
    @w.setter
    def w(self, value):
        self._array[3] = value

    @property
    def forward(self):
        return Vector3(0, 0, 1).rotate(self)
        # return Vector3(2 * (self.x * self.z - self.w * self.y),
        #                2 * (self.y * self.z + self.w * self.x),
        #                1 - 2 * (self.x * self.x + self.y * self.y))

    @property
    def back(self):
        return Vector3(0, 0, -1).rotate(self)
        # return Vector3(-2 * (self.x * self.z - self.w * self.y),
        #                -2 * (self.y * self.z + self.w * self.x),
        #                -(1 - 2 * (self.x * self.x + self.y * self.y)))

    @property
    def up(self):
        return Vector3(0, 1, 0).rotate(self)
        # return Vector3(2 * (self.x * self.y + self.w * self.z),
        #                1 - 2 * (self.x * self.x + self.z * self.z),
        #                2 * (self.y * self.z - self.w * self.x))

    @property
    def down(self):
        return Vector3(0, -1, 0).rotate(self)
        # return Vector3(-2 * (self.x * self.y + self.w * self.z),
        #                -(1 - 2 * (self.x * self.x + self.z * self.z)),
        #                -2 * (self.y * self.z - self.w * self.x))

    @property
    def right(self):
        return Vector3(1, 0, 0).rotate(self)
        # return Vector3(1 - 2 * (self.y * self.y + self.z * self.z),
        #                2 * (self.x * self.y - self.w * self.z),
        #                2 * (self.x * self.z + self.w * self.y))

    @property
    def left(self):
        return Vector3(-1, 0, 0).rotate(self)
        # return Vector3(-(1 - 2 * (self.y * self.y + self.z * self.z)),
        #                -2 * (self.x * self.y - self.w * self.z),
        #                -2 * (self.x * self.z + self.w * self.y))

    def __mul__(self, other):
        if isinstance(other, Quaternion):
            own_x, own_y, own_z, own_w = tuple(self._array)
            other_x, other_y, other_z, other_w = tuple(other._array)
            x = own_x * other_w + own_w * other_x + own_y * other_z - own_z * other_y
            y = own_y * other_w + own_w * other_y + own_z * other_x - own_x * other_z
            z = own_z * other_w + own_w * other_z + own_x * other_y - own_y * other_x
            w = own_w * other_w - own_x * other_x - own_y * other_y - own_z * other_z

            return Quaternion(x, y, z, w)
        elif isinstance(other, Vector3):
            own_x, own_y, own_z, own_w = tuple(self._array)
            other_x, other_y, other_z = tuple(other._array)
            w = -own_x * other_x - own_y * other_y - own_z * other_z
            x =  own_w * other_x + own_y * other_z - own_z * other_y
            y =  own_w * other_y + own_z * other_x - own_x * other_z
            z =  own_w * other_z + own_x * other_y - own_y * other_x

            return Quaternion(x, y, z, w)
        else:
            super().__mul__(other)

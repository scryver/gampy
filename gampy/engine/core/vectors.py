__author__ = 'michiel'

from math import radians, tan, sin, cos
from numbers import Number
import numpy

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
            return self / self.length
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
            result = super().__truediv__(other)
        return self.__class__(result)

    def __eq__(self, other):
        if isinstance(other, Vector):
            return numpy.array_equal(self, other)
        else:
            return numpy.all(self == other)

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
        return (destination - self) * lerp_factor + self


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
            # rotate on local x + rotate on local z + rotate on local y
            return self.cross(quat_or_axis * -sin(angle)) + \
                   self * cos(angle) + \
                   quat_or_axis * self.dot(quat_or_axis * (1 - cos(angle)))
        else:
            return NotImplemented

    def lerp(self, destination, lerp_factor):
        return (destination - self) * lerp_factor + self


class Matrix4(numpy.matrix):

    def __new__(subtype, dtype=numpy.float32):

        obj = numpy.zeros((4, 4), dtype=numpy.float32).view(Matrix4)
        return obj

    @property
    def m(self):
        return self.copy().view(Matrix4)

    def init_identity(self):
        self[:,:] = numpy.eye(4, 4, dtype=numpy.float32).view(numpy.matrix)

        return self.view(Matrix4)

    def init_translation(self, x, y, z):
        self.init_identity()
        self[0:3, 3] = [[x], [y], [z]]

        return self.view(Matrix4)

    def init_rotation(self, x, y, z=None):
        if isinstance(x, Vector3):
            if z is None:
            # DONT KNOW IF THIS IS NECESSARY
                f = x.normalized()
                r = y.view(Vector3).normalized()
                r = r.cross(f)
                u = f.cross(r)
            # END OF DONT KNOW
            else:
                f = x # forward
                u = y # up
                r = z # right

            self[0, 0:3] = [r.x, r.y, r.z]
            self[1, 0:3] = [u.x, u.y, u.z]
            self[2, 0:3] = [f.x, f.y, f.z]
            self[3, 3] = 1.
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
        return Vector3(self[0, 0] * other.x + self[0, 1] * other.y + self[0, 2] * other.z + self[0, 3] * w_offset,
                       self[1, 0] * other.x + self[1, 1] * other.y + self[1, 2] * other.z + self[1, 3] * w_offset,
                       self[2, 0] * other.x + self[2, 1] * other.y + self[2, 2] * other.z + self[2, 3] * w_offset)

    def __mul__(self, other):
        if isinstance(other, Matrix4):
            return numpy.dot(self, other).view(Matrix4)

        return NotImplemented

    def get(self, x, y):
        return self[x, y]

    def set(self, x, y, value):
        self[x, y] = value


class Quaternion(Vector):

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
            if isinstance(x, Vector3):
                sin_half_angle = sin(y / 2)
                cos_half_angle = cos(y / 2)

                w = cos_half_angle
                z = x.z * sin_half_angle
                y = x.y * sin_half_angle
                x = x.x * sin_half_angle
                data = [x, y, z, w]
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
            own_x, own_y, own_z, own_w = tuple(self)
            other_x, other_y, other_z, other_w = tuple(other)
            x = own_x * other_w + own_w * other_x + own_y * other_z - own_z * other_y
            y = own_y * other_w + own_w * other_y + own_z * other_x - own_x * other_z
            z = own_z * other_w + own_w * other_z + own_x * other_y - own_y * other_x
            w = own_w * other_w - own_x * other_x - own_y * other_y - own_z * other_z

            return Quaternion(x, y, z, w)
        elif isinstance(other, Vector3):
            own_x, own_y, own_z, own_w = tuple(self)
            other_x, other_y, other_z = tuple(other)
            w = -own_x * other_x - own_y * other_y - own_z * other_z
            x =  own_w * other_x + own_y * other_z - own_z * other_y
            y =  own_w * other_y + own_z * other_x - own_x * other_z
            z =  own_w * other_z + own_x * other_y - own_y * other_x

            return Quaternion(x, y, z, w)
        else:
            super().__mul__(other)
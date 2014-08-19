__author__ = 'michiel'

from math import radians, tan, sin, cos
from numbers import Number
import numpy
from numpy import sqrt
import gampy.engine.core.util as core_util


class Vector2:

    def __init__(self, x=None, y=None):
        self.x = core_util.is_float(x, 'X')
        self.y = core_util.is_float(y, 'Y')

    @property
    def length(self):
        return sqrt(self.x * self.x + self.y * self.y)

    def max(self):
        return max(self.x, self.y)

    def normalized(self):
        length = self.length

        if length > 0:
            return self / length
        else:
            return Vector2(0, 0, 0)

    def rotate(self, angle):
        rad = radians(angle)
        cosine = cos(rad)
        sinus = sin(rad)

        return Vector2(self.x * cosine - self.y * sinus,
                       self.x * sinus + self.y * cosine)

    def lerp(self, destination, lerp_factor):
        lerp_factor = core_util.is_float(lerp_factor, 'Lerp Factor')
        destination = core_util.is_instance(destination, 'Destination', Vector2)

        return (destination - self) * lerp_factor + self

    def dot(self, other):
        if isinstance(other, Vector2):
            return self.x * other.x + self.y * other.y
        return NotImplemented

    def cross(self, other):
        if isinstance(other, Vector2):
            return self.x * other.y - self.y * other.x
        return NotImplemented

    def __add__(self, other):
        if isinstance(other, Vector2):
            return Vector2(self.x + other.x, self.y + other.y)
        elif isinstance(other, Number):
            return Vector2(self.x + other, self.y + other)

        return NotImplemented

    def __sub__(self, other):
        if isinstance(other, Vector2):
            return Vector2(self.x - other.x, self.y - other.y)
        elif isinstance(other, Number):
            return Vector2(self.x - other, self.y - other)

        return NotImplemented

    def __mul__(self, other):
        if isinstance(other, Vector2):
            return Vector2(self.x * other.x, self.y * other.y)
        elif isinstance(other, Number):
            return Vector2(self.x * other, self.y * other)

        return NotImplemented

    def __truediv__(self, other):
        if isinstance(other, Vector2):
            return Vector2(self.x / other.x, self.y / other.y)
        elif isinstance(other, Number):
            return Vector2(self.x / other, self.y / other)

        return NotImplemented

    def __eq__(self, other):
        if isinstance(other, Vector2):
            return self.x == other.x and self.y == other.y
        elif isinstance(other, Number):
            return self.x == other and self.y == other

        return NotImplemented

    def __ne__(self, other):
        if isinstance(other, Vector2):
            return self.x != other.x and self.y != other.y
        elif isinstance(other, Number):
            return self.x != other and self.y != other

        return NotImplemented

    def __str__(self):
        return '({} {})'.format(self.x, self.y)


class Vector3:

    def __init__(self, x=0., y=0., z=0.):
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)

    def set(self, x, y, z):
        self.x, self.y, self.z = x, y, z

    @property
    def length(self):
        return sqrt(self.dot(self))

    def max(self):
        return max(self.x, self.y, self.z)

    @property
    def xy(self):
        return Vector2(self.x, self.y)
    @property
    def xz(self):
        return Vector2(self.x, self.z)
    @property
    def yx(self):
        return Vector2(self.y, self.x)
    @property
    def yz(self):
        return Vector2(self.y, self.z)
    @property
    def zx(self):
        return Vector2(self.z, self.x)
    @property
    def zy(self):
        return Vector2(self.z, self.y)

    def normalized(self):
        try:
            return self / self.length
        except ZeroDivisionError:
            return Vector3(0, 0, 0)

    def rotate(self, quat_or_axis, angle=None):
        if isinstance(quat_or_axis, Quaternion):
            w = quat_or_axis * self * quat_or_axis.conjugate()

            return Vector3(w.x, w.y, w.z)
        elif isinstance(quat_or_axis, Vector3):
            # rotate on local x + rotate on local z + rotate on local y
            return self.cross(quat_or_axis * -sin(angle)) + \
                   self * cos(angle) + \
                   quat_or_axis * self.dot(quat_or_axis * (1 - cos(angle)))
            # rotation = Quaternion(quat_or_axis, angle)
            # w = (rotation * self) * rotation.conjugate()
            #
            # self.x = w.x
            # self.y = w.y
            # self.z = w.z
            #
            # return self
        else:
            return NotImplemented

    def lerp(self, destination, lerp_factor):
        lerp_factor = core_util.is_float(lerp_factor, 'Lerp Factor')
        destination = core_util.is_instance(destination, 'Destination', Vector3)

        return (destination - self) * lerp_factor + self

    def dot(self, other):
        if isinstance(other, Vector3):
            return self.x * other.x + self.y * other.y + self.z * other.z
        return NotImplemented

    def cross(self, other):
        if isinstance(other, Vector3):
            x = self.y * other.z - self.z * other.y
            y = self.z * other.x - self.x * other.z
            z = self.x * other.y - self.y * other.x
            return Vector3(x, y, z)
        return NotImplemented

    def __add__(self, other):
        if isinstance(other, Vector3):
            return Vector3(self.x + other.x, self.y + other.y, self.z + other.z)
        elif isinstance(other, Number):
            return Vector3(self.x + other, self.y + other, self.z + other)

        return NotImplemented

    def __sub__(self, other):
        if isinstance(other, Vector3):
            return Vector3(self.x - other.x, self.y - other.y, self.z - other.z)
        elif isinstance(other, Number):
            return Vector3(self.x - other, self.y - other, self.z - other)

        return NotImplemented

    def __mul__(self, other):
        if isinstance(other, Vector3):
            return Vector3(self.x * other.x, self.y * other.y, self.z * other.z)
        elif isinstance(other, Number):
            return Vector3(self.x * other, self.y * other, self.z * other)

        return NotImplemented

    def __truediv__(self, other):
        if isinstance(other, Vector3):
            return Vector3(self.x / other.x, self.y / other.y, self.z / other.y)
        elif isinstance(other, Number):
            return Vector3(self.x / other, self.y / other, self.z / other)

        return NotImplemented

    def __eq__(self, other):
        if isinstance(other, Vector3):
            return self.x == other.x and self.y == other.y and self.z == other.z
        elif isinstance(other, Number):
            return self.x == other and self.y == other and self.z == other

        return NotImplemented

    def __ne__(self, other):
        if isinstance(other, Vector3):
            return self.x != other.x and self.y != other.y and self.z != other.z
        elif isinstance(other, Number):
            return self.x != other and self.y != other and self.z != other

        return NotImplemented

    def __str__(self):
        return '({} {} {})'.format(self.x, self.y, self.z)

    def __abs__(self):
        return Vector3(abs(self.x), abs(self.y), abs(self.z))


class Matrix4:

    def __init__(self):
        self.m = []

        for i in range(4):
            self.m.append([])
            for j in range(4):
                self.m[i].append(0.)

    def get_m(self):
        res = Matrix4()
        res.m = [[self.m[i][j] for j in range(4)] for i in range(4)]

        return res

    def init_identity(self):
        for i, j in self.item_loop():
            if i == j:
                self.m[i][j] = 1.

        return self

    def init_translation(self, x, y, z):
        for i, j in self.item_loop():
            if i == j:
                self.m[i][j] = 1.
            if j == 3:
                if i == 0:
                    self.set(i, j, x)
                elif i == 1:
                    self.m[i][j] = y
                elif i == 2:
                    self.m[i][j] = z

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

            for i, j in self.item_loop():
                if i == j == 3:
                    self.set(i, j, 1.)
                elif i == 0:
                    v = r
                elif i == 1:
                    v = u
                elif i == 2:
                    v = f
                else:
                    continue

                if j == 0:
                    self.set(i, j, v.x)
                elif j == 1:
                    self.set(i, j, v.y)
                elif j == 2:
                    self.set(i, j, v.z)

        else:
            rx = Matrix4()
            ry = Matrix4()
            rz = Matrix4()

            x = radians(core_util.is_float(x, 'x'))
            y = radians(core_util.is_float(y, 'Y'))
            z = radians(core_util.is_float(z, 'Z'))

            rz.set(0, 0, cos(z));   rz.set(0, 1, -sin(z));      rz.set(0, 2, 0.);       rz.set(0, 3, 0.)
            rz.set(1, 0, sin(z));   rz.set(1, 1, cos(z));       rz.set(1, 2, 0.);       rz.set(1, 3, 0.)
            rz.set(2, 0, 0.);       rz.set(2, 1, 0.);           rz.set(2, 2, 1.);       rz.set(2, 3, 0.)
            rz.set(3, 0, 0.);       rz.set(3, 1, 0.);           rz.set(3, 2, 0.);       rz.set(3, 3, 1.)

            rx.set(0, 0, 1.);       rx.set(0, 1, 0.);           rx.set(0, 2, 0.);       rx.set(0, 3, 0.)
            rx.set(1, 0, 0.);       rx.set(1, 1, cos(x));       rx.set(1, 2, -sin(x));  rx.set(1, 3, 0.)
            rx.set(2, 0, 0.);       rx.set(2, 1, sin(x));       rx.set(2, 2, cos(x));   rx.set(2, 3, 0.)
            rx.set(3, 0, 0.);       rx.set(3, 1, 0.);           rx.set(3, 2, 0.);       rx.set(3, 3, 1.)

            ry.set(0, 0, cos(y));   ry.set(0, 1, 0.);           ry.set(0, 2, sin(y));   ry.set(0, 3, 0.)
            ry.set(1, 0, 0.);       ry.set(1, 1, 1.);           ry.set(1, 2, 0.);       ry.set(1, 3, 0.)
            ry.set(2, 0, -sin(y));  ry.set(2, 1, 0.);           ry.set(2, 2, cos(y));   ry.set(2, 3, 0.)
            ry.set(3, 0, 0.);       ry.set(3, 1, 0.);           ry.set(3, 2, 0.);       ry.set(3, 3, 1.)

            tmp = rz * ry * rx
            self.m = tmp.m

        return self

    def init_scale(self, x, y, z):
        for i, j in self.item_loop():
            if i == j:
                if i == 0:
                    self.m[i][j] = x
                elif i == 1:
                    self.m[i][j] = y
                elif i == 2:
                    self.m[i][j] = z
                elif i == 3:
                    self.m[i][j] = 1.

        return self

    def init_perspective(self, fov, aspect_ratio, z_near, z_far):
        tan_half_fov = tan(fov / 2)
        z_range = z_near - z_far

        x = 1 / (tan_half_fov * aspect_ratio)
        y = 1 / tan_half_fov
        z = (-z_near - z_far) / z_range
        zw = 2 * z_far * z_near / z_range

        self.set(0, 0, x);          self.set(0, 1, 0.);     self.set(0, 2, 0.);       self.set(0, 3, 0.)
        self.set(1, 0, 0.);         self.set(1, 1, y);      self.set(1, 2, 0.);       self.set(1, 3, 0.)
        self.set(2, 0, 0.);         self.set(2, 1, 0.);     self.set(2, 2, z);        self.set(2, 3, zw)
        self.set(3, 0, 0.);         self.set(3, 1, 0.);     self.set(3, 2, 1.);       self.set(3, 3, 0.)

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

        self.set(0, 0, 2/width);    self.set(0, 1, 0.);         self.set(0, 2, 0.);       self.set(0, 3, -(right + left)/width)
        self.set(1, 0, 0.);         self.set(1, 1, 2/height);   self.set(1, 2, 0.);       self.set(1, 3, -(top + bottom)/height)
        self.set(2, 0, 0.);         self.set(2, 1, 0.);         self.set(2, 2, -2/depth); self.set(2, 3, -(far + near)/depth)
        self.set(3, 0, 0.);         self.set(3, 1, 0.);         self.set(3, 2, 0.);       self.set(3, 3, 1.)

        return self

    def __mul__(self, other):
        if isinstance(other, Matrix4):
            res = Matrix4()

            for i, j in self.item_loop():
                res.set(i, j, self.m[i][0] * other.get(0, j) +
                              self.m[i][1] * other.get(1, j) +
                              self.m[i][2] * other.get(2, j) +
                              self.m[i][3] * other.get(3, j))

            return res

        return NotImplemented

    def get(self, x, y):
        return self.m[x][y]

    def set(self, x, y, value):
        self.m[x][y] = value

    @staticmethod
    def item_loop():
        for i in range(4):
            for j in range(4):
                yield i, j

    def __str__(self):
        data = []
        [[data.append(self.m[i][j]) for j in range(4)] for i in range(4)]

        string =  '\n[{:{width}} {:{width}} {:{width}} {:{width}}]' \
                  '\n[{:{width}} {:{width}} {:{width}} {:{width}}]' \
                  '\n[{:{width}} {:{width}} {:{width}} {:{width}}]' \
                  '\n[{:{width}} {:{width}} {:{width}} {:{width}}]' \
                  '\n'

        return string.format(*tuple(data), width=10)

    @classmethod
    def cast_matrix(cls, matrix):
        if isinstance(matrix, Matrix4):
            new_matrix = numpy.identity(4, dtype=numpy.float32)

            for i, j in Matrix4.item_loop():
                item = matrix.m[i][j]
                new_matrix[i, j] = item

            return new_matrix

        return False


class Quaternion:

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
        if x is None:
            x = 0
            y = 0
            z = 0
            w = 1
        elif isinstance(x, Vector3):
            sin_half_angle = sin(y / 2)
            cos_half_angle = cos(y / 2)

            w = cos_half_angle
            z = x.z * sin_half_angle
            y = x.y * sin_half_angle
            x = x.x * sin_half_angle

        self.x = x
        self.y = y
        self.z = z
        self.w = w

    @property
    def length(self):
        return sqrt(self.x * self.x + self.y * self.y + self.z * self.z + self.w * self.w)

    def normalized(self):
        length = self.length

        if length > 0:
            norm = self / length
        else:
            norm = Quaternion(0, 0, 0, 0)
        return norm

    def conjugate(self):
        return Quaternion(-self.x, -self.y, -self.z, self.w)

    def to_rotation_matrix(self):
        forward = Vector3(2.0 * (self.x*self.z - self.w*self.y), 2.0 * (self.y*self.z + self.w*self.x), 1.0 - 2.0 * (self.x*self.x + self.y*self.y))
        up = Vector3(2.0 * (self.x*self.y + self.w*self.z), 1.0 - 2.0 * (self.x*self.x + self.z*self.z), 2.0 * (self.y*self.z - self.w*self.x))
        right = Vector3(1.0 - 2.0 * (self.y*self.y + self.z*self.z), 2.0 * (self.x*self.y - self.w*self.z), 2.0 * (self.x*self.z + self.w*self.y))
        return Matrix4().init_rotation(forward, up, right)

    @property
    def forward(self):
        # return Vector3(0, 0, 1).rotate(self)
        return Vector3(2 * (self.x * self.z - self.w * self.y),
                       2 * (self.y * self.z + self.w * self.x),
                       1 - 2 * (self.x * self.x + self.y * self.y))

    @property
    def back(self):
        # return Vector3(0, 0, -1).rotate(self)
        return Vector3(-2 * (self.x * self.z - self.w * self.y),
                       -2 * (self.y * self.z + self.w * self.x),
                       -(1 - 2 * (self.x * self.x + self.y * self.y)))

    @property
    def up(self):
        # return Vector3(0, 1, 0).rotate(self)
        return Vector3(2 * (self.x * self.y + self.w * self.z),
                       1 - 2 * (self.x * self.x + self.z * self.z),
                       2 * (self.y * self.z - self.w * self.x))

    @property
    def down(self):
        # return Vector3(0, -1, 0).rotate(self)
        return Vector3(-2 * (self.x * self.y + self.w * self.z),
                       -(1 - 2 * (self.x * self.x + self.z * self.z)),
                       -2 * (self.y * self.z - self.w * self.x))

    @property
    def right(self):
        # return Vector3(1, 0, 0).rotate(self)
        return Vector3(1 - 2 * (self.y * self.y + self.z * self.z),
                       2 * (self.x * self.y - self.w * self.z),
                       2 * (self.x * self.z + self.w * self.y))

    @property
    def left(self):
        # return Vector3(-1, 0, 0).rotate(self)
        return Vector3(-(1 - 2 * (self.y * self.y + self.z * self.z)),
                       -2 * (self.x * self.y - self.w * self.z),
                       -2 * (self.x * self.z + self.w * self.y))

    def __mul__(self, other):
        if isinstance(other, Quaternion):
            x = self.x * other.w + self.w * other.x + self.y * other.z - self.z * other.y
            y = self.y * other.w + self.w * other.y + self.z * other.x - self.x * other.z
            z = self.z * other.w + self.w * other.z + self.x * other.y - self.y * other.x
            w = self.w * other.w - self.x * other.x - self.y * other.y - self.z * other.z

            return Quaternion(x, y, z, w)
        if isinstance(other, Vector3):
            w = -self.x * other.x - self.y * other.y - self.z * other.z
            x =  self.w * other.x + self.y * other.z - self.z * other.y
            y =  self.w * other.y + self.z * other.x - self.x * other.z
            z =  self.w * other.z + self.x * other.y - self.y * other.x

            return Quaternion(x, y, z, w)
        if isinstance(other, Number):
            return Quaternion(self.x * other, self.y * other, self.z * other, self.w * other)

        return NotImplemented

    def __truediv__(self, other):
        if isinstance(other, Number):
            return Quaternion(self.x / other, self.y / other, self.z / other, self.w / other)

        return NotImplemented

    def __str__(self):
        return '({} {} {} {})'.format(self.x, self.y, self.z, self.w)

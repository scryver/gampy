__author__ = 'michiel'
__author__ = 'michiel'

from math import sqrt, radians, sin, cos, tan
from numbers import Number, Integral
import numpy
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
            return self._array == other._array
        else:
            return self._array == other

    def __ne__(self, other):
        if isinstance(other, Vector):
            return self._array != other._array
        else:
            return self._array != other

    def __abs__(self):
        result = abs(self._array)
        return self.__class__(result)

    def max(self):
        return max(self._array)

    def min(self):
        return min(self._array)

    def __str__(self):
        return str(self._array)


class Vector2(Vector):

    def __init__(self, x=0, y=0):
        super().__init__(2)
        try:
            self.x = x
            self.y = y
        except ValueError:
            self.x = x[0]
            self.y = x[1]

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

    def __init__(self, x=0, y=0, z=0):
        super().__init__(3)
        try:
            self.x = x
            self.y = y
            self.z = z
        except ValueError:
            self.x = x[0]
            self.y = x[1]
            self.y = x[2]

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

    def rotate(self, angle, axis):
        if isinstance(axis, Vector3):
            half_angle = radians(angle / 2)
            sin_half_angle = sin(half_angle)
            cos_half_angle = cos(half_angle)

            rx = axis.x * sin_half_angle
            ry = axis.y * sin_half_angle
            rz = axis.z * sin_half_angle
            rw = cos_half_angle

            rotation = Quaternion(rx, ry, rz, rw)
            w = (rotation * self) * rotation.conjugate()

            self.x = w.x
            self.y = w.y
            self.z = w.z

            return self

        return NotImplemented

    def lerp(self, destination, lerp_factor):
        lerp_factor = core_util.is_float(lerp_factor, 'Lerp Factor')
        destination = core_util.is_instance(destination, 'Destination', Vector3)

        return (destination - self) * lerp_factor + self


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
        if z is None:
            forward = core_util.is_instance(x, 'Forward', Vector3)
            up = core_util.is_instance(y, 'Up', Vector3)

            # DONT KNOW IF THIS IS NECESSARY
            f = forward.normalized()

            r = up.normalized()
            r = r.cross(f)

            u = f.cross(r)
            # END OF DONT KNOW

            for i, j in self.item_loop():
                if i == 0:
                    v = r
                elif i == 1:
                    v = u
                elif i == 2:
                    v = f

                if j == 0:
                    self.set(i, j, v.x)
                elif j == 1:
                    self.set(i, j, v.y)
                elif j == 2:
                    self.set(i, j, v.z)

                if i == j == 3:
                    self.set(i, j, 1.)
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
        fov = core_util.is_float(fov, 'Field of View')
        aspect_ratio = core_util.is_float(aspect_ratio, 'Aspect Ratio')
        z_near = core_util.is_float(z_near, 'Z Near')
        z_far = core_util.is_float(z_far, 'Z Far')

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
        self.x = core_util.is_float(x, 'X')
        self.y = core_util.is_float(y, 'Y')
        self.z = core_util.is_float(z, 'Z')
        self.w = core_util.is_float(w, 'W')

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

        return NotImplemented

    def __truediv__(self, other):
        if isinstance(other, Number):
            return Quaternion(self.x / other, self.y / other, self.z / other, self.w / other)

        return NotImplemented

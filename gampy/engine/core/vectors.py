__author__ = 'michiel'

from math import sqrt, radians, sin, cos, tan
from numbers import Number
import numpy as np


class Vector2:

    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    @property
    def length(self):
        return sqrt(self.x * self.x + self.y * self.y)

    def dot(self, other):
        if isinstance(other, Vector2):
            return self.x * other.x + self.y * other.y

        return NotImplemented

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

    def __str__(self):
        return '({} {})'.format(self.x, self.y)


class Vector3:

    def __init__(self, x=0, y=0, z=0):
        self.x = x
        self.y = y
        self.z = z

    @property
    def length(self):
        return sqrt(self.x * self.x + self.y * self.y + self.z * self.z)

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

    def normalized(self):
        length = self.length

        if length > 0:
            return self / length
        else:
            return Vector3(0, 0, 0)

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

    def __str__(self):
        return '({} {} {})'.format(self.x, self.y, self.z)

    def __abs__(self):
        return Vector3(abs(self.x), abs(self.y), abs(self.z))

    def copy(self):
        return Vector3(self.x, self.y, self.z)


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

    def initIdentity(self):
        for i, j in self.item_loop():
            if i == j:
                self.m[i][j] = 1.

        return self

    def initTranslation(self, x, y, z):
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

    def initRotation(self, x, y, z):
        rx = Matrix4()
        ry = Matrix4()
        rz = Matrix4()

        x = radians(x)
        y = radians(y)
        z = radians(z)

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
        if isinstance(fov, Number):
            fov = float(fov)
        else:
            raise AttributeError('Field of View is not a number')
        if isinstance(aspect_ratio, Number):
            aspect_ratio = float(aspect_ratio)
        else:
            raise AttributeError('Aspect Ratio is not a number')
        if isinstance(z_near, Number):
            z_near = float(z_near)
        else:
            raise AttributeError('Z Near is not a number')
        if isinstance(z_far, Number):
            z_far = float(z_far)
        else:
            raise AttributeError('Z Far is not a number')

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

    def init_rotation(self, forward, up):
        if not isinstance(up, Vector3):
            raise AttributeError('Up direction of the camera is not a vector')
        if not isinstance(forward, Vector3):
            raise AttributeError('Forward direction of the camera is not a vector')

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


class Quaternion:

    def __init__(self, x=0., y=0., z=0., w=0.):
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
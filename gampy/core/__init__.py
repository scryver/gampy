from math import radians
from gampy.core.core import lib
from numbers import Number

__all__ = ['Matrix4', 'Vector3']


class Matrix4(object):
    """C++ Matrix4"""
    def __init__(self):
        super(Matrix4, self).__init__()
        self.m = lib.NewMatrix4d()

    def initIdentity(self):
        self.m = lib.Matrix4d_InitIdentity(self.m)
        return self

    def initTranslation(self, x, y, z):
        self.m = lib.Matrix4d_InitTranslation(self.m, float(x), float(y),
                                              float(z))
        return self

    def initRotation(self, x, y, z):
        x = radians(float(x))
        y = radians(float(y))
        z = radians(float(z))
        self.m = lib.Matrix4d_InitRotation(self.m, x, y, z)
        return self

    def init_scale(self, x, y, z):
        self.m = lib.Matrix4d_InitScale(self.m, float(x), float(y), float(z))
        return self

    def init_projection(self, fov, width, height, z_near, z_far):
        fov = radians(float(fov))
        self.m = lib.Matrix4d_InitProjection(self.m, fov, int(width),
                                             int(height), float(z_near),
                                             float(z_far))
        return self

    def get(self, x, y):
        return lib.Matrix4d_Get(self.m, x, y)

    def set(self, x, y, value):
        lib.Matrix4d_Set(self.m, x, y, value)

    def __mul__(self, other):
        if isinstance(other, Matrix4):
            res = Matrix4()
            res.m = lib.Matrix4d_Add(res.m, self.m)
            res.m = lib.Matrix4d_Mul(res.m, other.m)
        elif isinstance(other, (int, float)):
            res = Matrix4()
            res.m = lib.Matrix4d_Add(res.m, self.m)
            res.m = lib.Matrix4d_Mul_Scalar(res.m, float(other))
        else:
            return NotImplemented
        return res

    def __del__(self):
        if self.m is not None:
            lib.DeleteMatrix4d(self.m)
            self.m = None

    def __str__(self):
        data = []
        [[data.append(self.get(i, j)) for j in range(4)] for i in range(4)]

        string = '\n[{:{width}} {:{width}} {:{width}} {:{width}}]' \
                 '\n[{:{width}} {:{width}} {:{width}} {:{width}}]' \
                 '\n[{:{width}} {:{width}} {:{width}} {:{width}}]' \
                 '\n[{:{width}} {:{width}} {:{width}} {:{width}}]' \
                 '\n'

        return string.format(*tuple(data), width=20)


class Vector3(object):
    def __init__(self, x=0, y=0, z=0):
        super(Vector3, self).__init__()
        self.v = lib.NewVector3dInit(x, y, z)

    @property
    def x(self):
        return lib.Vector3d_GetX(self.v)

    @x.setter
    def x(self, value):
        lib.Vector3d_SetX(self.v, value)

    @property
    def y(self):
        return lib.Vector3d_GetY(self.v)

    @y.setter
    def y(self, value):
        lib.Vector3d_SetY(self.v, value)

    @property
    def z(self):
        return lib.Vector3d_GetZ(self.v)

    @z.setter
    def z(self, value):
        lib.Vector3d_SetZ(self.v, value)

    @property
    def length(self):
        return lib.Vector3d_GetLength(self.v)

    def dot(self, other):
        if isinstance(other, Vector3):
            return lib.Vector3d_Dot(self.v, other.v)

        return NotImplemented

    def cross(self, other):
        if isinstance(other, Vector3):
            res = Vector3()
            res.v = lib.Vector3d_Add(self.v)
            res.v = lib.Vector3d_Cross(other.v)
            return res

        return NotImplemented

    def normalize(self):
        lib.Vector3d_Normalize(self.v)

    def rotate(self, angle):
        pass

    def __add__(self, other):
        if isinstance(other, Vector3):
            res = Vector3()
            res.v = lib.Vector3d_Add(self.v)
            res.v = lib.Vector3d_Add(other.v)
            return res
        elif isinstance(other, Number):
            res = Vector3()
            res.v = lib.Vector3d_Add(self.v)
            res.v = lib.Vector3d_Add_Scalar(other)
            return res

        return NotImplemented

    def __sub__(self, other):
        if isinstance(other, Vector3):
            res = Vector3()
            res.v = lib.Vector3d_Add(self.v)
            res.v = lib.Vector3d_Sub(other.v)
            return res
        elif isinstance(other, Number):
            res = Vector3()
            res.v = lib.Vector3d_Add(self.v)
            res.v = lib.Vector3d_Sub_Scalar(other)
            return res

        return NotImplemented

    def __mul__(self, other):
        if isinstance(other, Vector3):
            res = Vector3()
            res.v = lib.Vector3d_Add(self.v)
            res.v = lib.Vector3d_Mul(other.v)
            return res
        elif isinstance(other, Number):
            res = Vector3()
            res.v = lib.Vector3d_Add(self.v)
            res.v = lib.Vector3d_Mul_Scalar(other)
            return res

        return NotImplemented

    def __truediv__(self, other):
        if isinstance(other, Vector3):
            res = Vector3()
            res.v = lib.Vector3d_Add(self.v)
            res.v = lib.Vector3d_Div(other.v)
            return res
        elif isinstance(other, Number):
            res = Vector3()
            res.v = lib.Vector3d_Add(self.v)
            res.v = lib.Vector3d_Div_Scalar(other)
            return res

        return NotImplemented

    def __str__(self):
        return '({} {} {})'.format(self.x, self.y, self.z)

    def __del__(self):
        if self.v is not None:
            lib.DeleteVector3d(self.v)
            self.v = None

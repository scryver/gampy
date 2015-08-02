from math import radians
from gampy.core.core import lib

__all__ = ['Matrix4']


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

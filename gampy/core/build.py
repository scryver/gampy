#!/usr/bin/env python

import os
from cffi import FFI

COMPILE = True
CORE_DIR = os.path.abspath(os.path.dirname(__file__))

ffi = FFI()

if COMPILE:
    ffi.set_source(
        "core", """
            // Nothing
            #include "wrapper.h"
        """,
        libraries=['game_core'],
        library_dirs=[os.path.join(CORE_DIR, 'build')],
        include_dirs=[os.path.join(CORE_DIR, 'include')]
    )

ffi.cdef("""
    typedef struct Matrix4d Matrix4d;

    Matrix4d* NewMatrix4d(void);

    Matrix4d* Matrix4d_InitIdentity(Matrix4d* m);
    Matrix4d* Matrix4d_InitTranslation(Matrix4d* m, double x, double y, double z);
    Matrix4d* Matrix4d_InitRotation(Matrix4d* m, double x, double y, double z);
    Matrix4d* Matrix4d_InitScale(Matrix4d* m, double x, double y, double z);
    Matrix4d* Matrix4d_InitProjection(Matrix4d* m, double fov, int width, int height, double zNear, double zFar);

    const double** Matrix4d_GetData(Matrix4d* m);
    const double Matrix4d_Get(Matrix4d* m, int row, int col);
    void Matrix4d_Set(Matrix4d* m, int row, int col, double value);

    Matrix4d* Matrix4d_Copy(Matrix4d* m, const Matrix4d* other);
    Matrix4d* Matrix4d_Add(Matrix4d* m, const Matrix4d* other);
    Matrix4d* Matrix4d_Sub(Matrix4d* m, const Matrix4d* other);
    Matrix4d* Matrix4d_Mul(Matrix4d* m, const Matrix4d* other);
    Matrix4d* Matrix4d_Add_Scalar(Matrix4d* m, double scalar);
    Matrix4d* Matrix4d_Sub_Scalar(Matrix4d* m, double scalar);
    Matrix4d* Matrix4d_Mul_Scalar(Matrix4d* m, double scalar);
    Matrix4d* Matrix4d_Div_Scalar(Matrix4d* m, double scalar);

    bool Matrix4d_Equals(Matrix4d* m, const Matrix4d* other);

    void DeleteMatrix4d(Matrix4d* m);
""")

if not COMPILE:
    lib = ffi.dlopen(os.path.join(CORE_DIR, 'build', 'libgame_core.so'))


if __name__ == '__main__':
    if COMPILE:
        ffi.compile()

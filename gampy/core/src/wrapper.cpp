#include "wrapper.h"

#include <stdio.h>
#include "./math/matrix4.hpp"

extern "C" {
    Matrix4d* NewMatrix4d(void) {
        return new Matrix4d();
    }

    Matrix4d* Matrix4d_InitIdentity(Matrix4d* m) {
        return &(m->InitIdentity());
    }

    Matrix4d* Matrix4d_InitTranslation(Matrix4d* m, double x, double y, double z) {
        return &(m->InitTranslation(x, y, z));
    }

    Matrix4d* Matrix4d_InitRotation(Matrix4d* m, double x, double y, double z) {
        return &(m->InitRotation(x, y, z));
    }

    Matrix4d* Matrix4d_InitScale(Matrix4d* m, double x, double y, double z) {
        return &(m->InitScale(x, y, z));
    }

    Matrix4d* Matrix4d_InitProjection(Matrix4d* m, double fov, int width, int height, double zNear, double zFar) {
        return &(m->InitProjection(fov, width, height, zNear, zFar));
    }

    const double Matrix4d_Get(Matrix4d* m, int row, int col) {
        return m->Get(row, col);
    }

    void Matrix4d_Set(Matrix4d* m, int row, int col, double value) {
        m->Set(row, col, value);
    }

    Matrix4d* Matrix4d_Copy(Matrix4d* m, const Matrix4d* other) {
        return &(*m = *other);
    }

    Matrix4d* Matrix4d_Add(Matrix4d* m, const Matrix4d* other) {
        return &(*m += *other);
    }

    Matrix4d* Matrix4d_Sub(Matrix4d* m, const Matrix4d* other) {
        return &(*m -= *other);
    }

    Matrix4d* Matrix4d_Mul(Matrix4d* m, const Matrix4d* other) {
        return &(*m *= *other);
    }

    Matrix4d* Matrix4d_Add_Scalar(Matrix4d* m, double scalar) {
        return &(*m += scalar);
    }

    Matrix4d* Matrix4d_Sub_Scalar(Matrix4d* m, double scalar) {
        return &(*m -= scalar);
    }

    Matrix4d* Matrix4d_Mul_Scalar(Matrix4d* m, double scalar) {
        return &(*m *= scalar);
    }

    Matrix4d* Matrix4d_Div_Scalar(Matrix4d* m, double scalar) {
        return &(*m /= scalar);
    }

    bool Matrix4d_Equals(Matrix4d* m, const Matrix4d* other) {
        return *m == *other;
    }

    void DeleteMatrix4d(Matrix4d* m) {
        delete m;
    }

}

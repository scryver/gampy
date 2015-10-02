#include "wrapper.h"

#include <stdio.h>
#include "./math/vector3.hpp"

extern "C" {
    Vector3d* NewVector3d(void) {
        return new Vector3d();
    }

    Vector3d* NewVector3dInit(double x, double y, double z) {
        return new Vector3d(x, y, z);
    }


    double Vector3d_Length(Vector3d* v) {
        return v->GetLength();
    }

    double Vector3d_Dot(Vector3d* v, const Vector3d* other) {
        return v->Dot(*other);
    }

    Vector3d* Vector3d_Cross(Vector3d* v, const Vector3d* other) {
        return v->Cross(*other);
    }

    Vector3d* Vector3d_Normalize(Vector3d* v) {
        return &(v->Normalize());
    }

    Vector3d* Vector3d_Normalized(Vector3d* v) {
        return v->Normalized();
    }

    const double Vector3d_GetX(Vector3d* v) {
        return v->GetX();
    }

    const double Vector3d_GetY(Vector3d* v) {
        return v->GetY();
    }

    const double Vector3d_GetZ(Vector3d* v) {
        return v->GetZ();
    }

    void Vector3d_SetX(Vector3d* v, double x) {
        v->SetX(x);
    }

    void Vector3d_SetY(Vector3d* v, double y) {
        v->SetY(y);
    }

    void Vector3d_SetZ(Vector3d* v, double z) {
        v->SetZ(z);
    }

    Vector3d* Vector3d_Copy(Vector3d* v, const Vector3d* other) {
        return &(*v = *other);
    }

    Vector3d* Vector3d_Add(Vector3d* v, const Vector3d* other) {
        return &(*v += *other);
    }

    Vector3d* Vector3d_Sub(Vector3d* v, const Vector3d* other) {
        return &(*v -= *other);
    }

    Vector3d* Vector3d_Mul(Vector3d* v, const Vector3d* other) {
        return &(*v *= *other);
    }

    Vector3d* Vector3d_Div(Vector3d* v, const Vector3d* other) {
        return &(*v /= *other);
    }

    Vector3d* Vector3d_Add_Scalar(Vector3d* v, double scalar) {
        return &(*v += scalar);
    }

    Vector3d* Vector3d_Sub_Scalar(Vector3d* v, double scalar) {
        return &(*v -= scalar);
    }

    Vector3d* Vector3d_Mul_Scalar(Vector3d* v, double scalar) {
        return &(*v *= scalar);
    }

    Vector3d* Vector3d_Div_Scalar(Vector3d* v, double scalar) {
        return &(*v /= scalar);
    }

    bool Vector3d_Equals(Vector3d* v, const Vector3d* other) {
        return (*v == *other);
    }

    void DeleteVector3d(Vector3d* v) {
        delete v;
    }
}

#ifndef __VECTOR_H__
#define __VECTOR_H__

#ifdef __cplusplus
extern "C" {
#endif

#include <stdbool.h>

typedef struct Vector3d Vector3d;

Vector3d* NewVector3d(void);
Vector3d* NewVector3dInit(double x, double y, double z);

double Vector3d_Length(Vector3d* v);
double Vector3d_Dot(Vector3d* v, const Vector3d* other);
Vector3d* Vector3d_Cross(Vector3d* v, const Vector3d* other);
Vector3d* Vector3d_Normalize(Vector3d* v);
Vector3d* Vector3d_Normalized(Vector3d* v);

const double Vector3d_GetX(Vector3d* v);
const double Vector3d_GetY(Vector3d* v);
const double Vector3d_GetZ(Vector3d* v);
void Vector3d_SetX(Vector3d* v, double x);
void Vector3d_SetY(Vector3d* v, double y);
void Vector3d_SetZ(Vector3d* v, double z);

Vector3d* Vector3d_Copy(Vector3d* v, const Vector3d* other);
Vector3d* Vector3d_Add(Vector3d* v, const Vector3d* other);
Vector3d* Vector3d_Sub(Vector3d* v, const Vector3d* other);
Vector3d* Vector3d_Mul(Vector3d* v, const Vector3d* other);
Vector3d* Vector3d_Div(Vector3d* v, const Vector3d* other);
Vector3d* Vector3d_Add_Scalar(Vector3d* v, double scalar);
Vector3d* Vector3d_Sub_Scalar(Vector3d* v, double scalar);
Vector3d* Vector3d_Mul_Scalar(Vector3d* v, double scalar);
Vector3d* Vector3d_Div_Scalar(Vector3d* v, double scalar);

bool Vector3d_Equals(Vector3d* v, const Vector3d* other);

void DeleteVector3d(Vector3d* v);

#ifdef __cplusplus
}
#endif

#endif // __VECTOR_H__

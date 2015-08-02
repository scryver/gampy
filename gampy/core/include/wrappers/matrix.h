#ifndef __MATRIX_H__
#define __MATRIX_H__

#ifdef __cplusplus
extern "C" {
#endif

#include <stdbool.h>

typedef struct Matrix4d Matrix4d;

Matrix4d* NewMatrix4d(void);

Matrix4d* Matrix4d_InitIdentity(Matrix4d* m);
Matrix4d* Matrix4d_InitTranslation(Matrix4d* m, double x, double y, double z);
Matrix4d* Matrix4d_InitRotation(Matrix4d* m, double x, double y, double z);
Matrix4d* Matrix4d_InitScale(Matrix4d* m, double x, double y, double z);
Matrix4d* Matrix4d_InitProjection(Matrix4d* m, double fov, int width, int height, double zNear, double zFar);

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

#ifdef __cplusplus
}
#endif

#endif // __MATRIX_H__

#include <stdio.h>
#include <math.h>

#include "../include/wrapper.h"

void print_matrix(Matrix4d *m) {
    int i, j;
    for (i = 0; i < 4; i++) {
        for (j = 0; j < 4; j++) {
            printf("%d %d %6.3f |", i, j, Matrix4d_Get(m, i, j));
        }
        printf("\n");
    }
    printf("------------------------------------\n");
}

int main() {
    Matrix4d *m = NewMatrix4d();
    print_matrix(m);

    Matrix4d_InitIdentity(m);
    print_matrix(m);

    DeleteMatrix4d(m);

    m = NewMatrix4d();
    Matrix4d *t = NewMatrix4d();
    Matrix4d *r = NewMatrix4d();
    Matrix4d *s = NewMatrix4d();

    Matrix4d_InitTranslation(t, 4.0, 2.0, 3.0);
    print_matrix(t);

    Matrix4d_InitRotation(r, 3.3, 4.4, 5.5);
    print_matrix(r);

    Matrix4d_InitScale(s, 2.0, 3.0, 4.0);
    print_matrix(s);

    Matrix4d_Add(m, t);
    Matrix4d_Mul(m, r);
    Matrix4d_Mul(m, s);
    print_matrix(m);

    DeleteMatrix4d(m);
    DeleteMatrix4d(t);
    DeleteMatrix4d(r);
    DeleteMatrix4d(s);

    m = NewMatrix4d();
    Matrix4d_InitProjection(m, 70.0 / 360.0 * 2.0 * M_PI, 640, 480, 0.1, 1000.0);
    print_matrix(m);

    DeleteMatrix4d(m);
}

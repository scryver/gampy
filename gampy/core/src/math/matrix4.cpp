#include "matrix4.hpp"

#include <stdio.h>
#include <math.h>

Matrix4d::Matrix4d() {
    for (unsigned int i = 0; i < 4; i++) {
        for (unsigned int j = 0; j < 4; j++) {
            m_data[i][j] = 0.0;
        }
    }
}

Matrix4d::~Matrix4d() {

}

Matrix4d& Matrix4d::InitIdentity() {
    for (int i = 4 - 1; i >= 0; i--) {
        m_data[i][i] = 1.0;
    }
    return *this;
}

Matrix4d& Matrix4d::InitTranslation(double x, double y, double z) {
    for (int i = 4 - 1; i >= 0; i--) {
        m_data[i][i] = 1.0;
    }
    m_data[0][3] = x;
    m_data[1][3] = y;
    m_data[2][3] = z;

    return *this;
}

Matrix4d& Matrix4d::InitRotation(double x, double y, double z) {
    Matrix4d rx;
    Matrix4d ry;
    Matrix4d rz;

    rz.Set(0, 0, cos(z));   rz.Set(0, 1, -sin(z));  rz.Set(0, 2, 0.0);      rz.Set(0, 3, 0.0);
    rz.Set(1, 0, sin(z));   rz.Set(1, 1, cos(z));   rz.Set(1, 2, 0.0);      rz.Set(1, 3, 0.0);
    rz.Set(2, 0, 0.0);      rz.Set(2, 1, 0.0);      rz.Set(2, 2, 1.0);      rz.Set(2, 3, 0.0);
    rz.Set(3, 0, 0.0);      rz.Set(3, 1, 0.0);      rz.Set(3, 2, 0.0);      rz.Set(3, 3, 1.0);

    rx.Set(0, 0, 1.0);      rx.Set(0, 1, 0.0);      rx.Set(0, 2, 0.0);      rx.Set(0, 3, 0.0);
    rx.Set(1, 0, 0.0);      rx.Set(1, 1, cos(x));   rx.Set(1, 2, -sin(x));  rx.Set(1, 3, 0.0);
    rx.Set(2, 0, 0.0);      rx.Set(2, 1, sin(x));   rx.Set(2, 2, cos(x));   rx.Set(2, 3, 0.0);
    rx.Set(3, 0, 0.0);      rx.Set(3, 1, 0.0);      rx.Set(3, 2, 0.0);      rx.Set(3, 3, 1.0);

    ry.Set(0, 0, cos(y));   ry.Set(0, 1, 0.0);      ry.Set(0, 2, sin(y));   ry.Set(0, 3, 0.0);
    ry.Set(1, 0, 0.0);      ry.Set(1, 1, 1.0);      ry.Set(1, 2, 0.0);      ry.Set(1, 3, 0.0);
    ry.Set(2, 0, -sin(y));  ry.Set(2, 1, 0.0);      ry.Set(2, 2, cos(y));   ry.Set(2, 3, 0.0);
    ry.Set(3, 0, 0.0);      ry.Set(3, 1, 0.0);      ry.Set(3, 2, 0.0);      ry.Set(3, 3, 1.0);

    *this = rz * ry * rx;
    return *this;
}

Matrix4d& Matrix4d::InitScale(double x, double y, double z) {
    m_data[0][0] = x;
    m_data[1][1] = y;
    m_data[2][2] = z;
    m_data[3][3] = 1.0;
    return *this;
}

Matrix4d& Matrix4d::InitProjection(double fov, int width, int height, double zNear, double zFar) {
    double aspectRatio = (double)width / height;
    double tanHalfFOV = tan(fov / 2);
    double zRange = zNear - zFar;

    double x, y, z, zw;
    x = 1 / (tanHalfFOV * aspectRatio);
    y = 1 / tanHalfFOV;
    z = (-zNear - zFar) / zRange;
    zw = 2 * zFar * zNear / zRange;

    m_data[0][0] = x;
    m_data[1][1] = y;
    m_data[2][2] = z;
    m_data[2][3] = zw;
    m_data[3][2] = 1.0;

    return *this;
}

Matrix4d& Matrix4d::operator=(const Matrix4d& other) {
    double value;
    if (this != &other) {
        for (int i = 4 - 1; i >= 0; i--) {
            for (int j = 4 - 1; j >= 0; j--) {
                value = other.Get(i, j);
                m_data[i][j] = value;
            }
        }
    }

    return *this;
}

Matrix4d& Matrix4d::operator+=(const Matrix4d& other) {
    for (unsigned int i = 0; i < 4; i++) {
        for (unsigned int j = 0; j < 4; j++) {
            m_data[i][j] += other.Get(i, j);
        }
    }

    return *this;
}

Matrix4d& Matrix4d::operator-=(const Matrix4d& other) {
    for (unsigned int i = 0; i < 4; i++) {
        for (unsigned int j = 0; j < 4; j++) {
            m_data[i][j] -= other.Get(i, j);
        }
    }

    return *this;
}

Matrix4d& Matrix4d::operator*=(const Matrix4d& other) {
    unsigned int i, j;
    Matrix4d res;
    double value;

    for (i = 0; i < 4; i++) {
        for (j = 0; j < 4; j++) {
            res.Set(i, j, m_data[i][0] * other.Get(0, j) +
                    m_data[i][1] * other.Get(1, j) +
                    m_data[i][2] * other.Get(2, j) +
                    m_data[i][3] * other.Get(3, j));
        }
    }

    for (i = 0; i < 4; i++) {
        for (j = 0; j < 4; j++) {
            m_data[i][j] = res.Get(i, j);
        }
    }

    return *this;
}


Matrix4d& Matrix4d::operator+=(double scalar) {
    for (unsigned int i = 0; i < 4; i++) {
        for (unsigned int j = 0; j < 4; j++) {
            m_data[i][j] += scalar;
        }
    }

    return *this;
}

Matrix4d& Matrix4d::operator-=(double scalar) {
    for (unsigned int i = 0; i < 4; i++) {
        for (unsigned int j = 0; j < 4; j++) {
            m_data[i][j] -= scalar;
        }
    }

    return *this;
}

Matrix4d& Matrix4d::operator*=(double scalar) {
    for (unsigned int i = 0; i < 4; i++) {
        for (unsigned int j = 0; j < 4; j++) {
            m_data[i][j] *= scalar;
        }
    }

    return *this;
}

Matrix4d& Matrix4d::operator/=(double scalar) {
    for (unsigned int i = 0; i < 4; i++) {
        for (unsigned int j = 0; j < 4; j++) {
            m_data[i][j] /= scalar;
        }
    }

    return *this;
}

bool Matrix4d::operator==(const Matrix4d& other) const {
    bool same = true, loop = true;

    for (int i = 4 - 1; i >= 0 && loop; i--) {
        for (int j = 4 - 1; j >= 0 && loop; j--) {
            if (m_data[i][j] != other.Get(i, j)) {
                same = false;
                loop = false;
            }
        }
    }

    return same;
}


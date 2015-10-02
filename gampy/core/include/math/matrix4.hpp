#ifndef __MATRIX_4_HPP__
#define __MATRIX_4_HPP__

class Matrix4d
{
public:
    Matrix4d();
    virtual ~Matrix4d();

    Matrix4d& InitIdentity();
    Matrix4d& InitTranslation(double x, double y, double z);
    Matrix4d& InitRotation(double x, double y, double z);
    Matrix4d& InitScale(double x, double y, double z);
    Matrix4d& InitProjection(double fov, int width, int height, double zNear, double zFar);

    const double Get(int row, int col) const { return m_data[row][col]; };
    void Set(int row, int col, double value) { m_data[row][col] = value; };

    Matrix4d(const Matrix4d& other);
    Matrix4d& operator=(const Matrix4d& other);
    Matrix4d& operator+=(const Matrix4d& other);
    Matrix4d& operator-=(const Matrix4d& other);
    Matrix4d& operator*=(const Matrix4d& other);
    Matrix4d& operator+=(double scalar);
    Matrix4d& operator-=(double scalar);
    Matrix4d& operator*=(double scalar);
    Matrix4d& operator/=(double scalar);

    const Matrix4d operator+(const Matrix4d& other) const {
        return Matrix4d(*this) += other;
    };
    const Matrix4d operator-(const Matrix4d& other) const {
        return Matrix4d(*this) -= other;
    };
    const Matrix4d operator*(const Matrix4d& other) const {
        return Matrix4d(*this) *= other;
    };

    const Matrix4d operator+(double scalar) const {
        return Matrix4d(*this) += scalar;
    };
    const Matrix4d operator-(double scalar) const {
        return Matrix4d(*this) -= scalar;
    };
    const Matrix4d operator*(double scalar) const {
        return Matrix4d(*this) *= scalar;
    };
    const Matrix4d operator/(double scalar) const {
        return Matrix4d(*this) /= scalar;
    };

    bool operator==(const Matrix4d& other) const;
    bool operator!=(const Matrix4d& other) const { return !(*this == other); };
private:
    double      m_data[4][4];
};

#endif // __MATRIX_4_HPP__

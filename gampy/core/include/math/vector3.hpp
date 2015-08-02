#ifndef __VECTOR_3_HPP__
#define __VECTOR_3_HPP__

class Vector3d
{
public:
    Vector3d();
    Vector3d(double x, double y, double z);
    virtual ~Vector3d();

    double GetLength();
    double Dot(const Vector3d& other);
    Vector3d Cross(const Vector3d& other);
    void Normalize();
    Vector3d Normalized();

    double GetX() { return m_x; };
    double GetY() { return m_y; };
    double GetZ() { return m_z; };
    double SetX(double x) { m_x = x; };
    double SetY(double y) { m_y = y; };
    double SetZ(double z) { m_z = z; };

    Vector3d& operator=(const Vector3d& other);
    Vector3d& operator+=(const Vector3d& other);
    Vector3d& operator-=(const Vector3d& other);
    Vector3d& operator*=(const Vector3d& other);
    Vector3d& operator/=(const Vector3d& other);
    Vector3d& operator+=(double scalar);
    Vector3d& operator-=(double scalar);
    Vector3d& operator*=(double scalar);
    Vector3d& operator/=(double scalar);

    const Vector3d operator+(const Vector3d& other) const {
        return Vector3d(*this) += other;
    };
    const Vector3d operator-(const Vector3d& other) const {
        return Vector3d(*this) -= other;
    };
    const Vector3d operator*(const Vector3d& other) const {
        return Vector3d(*this) *= other;
    };
    const Vector3d operator/(const Vector3d& other) const {
        return Vector3d(*this) /= other;
    };

    const Vector3d operator+(double scalar) const {
        return Vector3d(*this) += scalar;
    };
    const Vector3d operator-(double scalar) const {
        return Vector3d(*this) -= scalar;
    };
    const Vector3d operator*(double scalar) const {
        return Vector3d(*this) *= scalar;
    };
    const Vector3d operator/(double scalar) const {
        return Vector3d(*this) /= scalar;
    };

    bool operator==(const Vector3d& other) const;
    bool operator!=(const Vector3d& other) const { return !(*this == other); };
private:
    double      m_x;
    double      m_y;
    double      m_z;
};)

#endif // __VECTOR_3_HPP__

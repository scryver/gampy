#include "vector3.hpp"

#include <math.h>

Vector3d::Vector3d() {
    Vector3d(0.0, 0.0, 0.0);
}

Vector3d::Vector3d(double x, double y, double z) :
    m_x(x),
    m_y(y),
    m_z(z) {}

Vector3d::~Vector3d() {

}

double Vector3d::GetLength() {
    return sqrt(m_x * m_x + m_y * m_y + m_z * m_z);
}

double Vector3d::Dot(const Vector3d& other) {
    return m_x * other.GetX() + m_y * other.GetY() + m_z * other.GetZ();
}

Vector3d* Vector3d::Cross(const Vector3d& other) {
    double x, y, z;
    x = m_y * other.GetZ() - m_z * other.GetY();
    y = m_z * other.GetX() - m_x * other.GetZ();
    z = m_x * other.GetY() - m_y * other.GetX();

    return new Vector3d(x, y, z);
}

Vector3d& Vector3d::Normalize() {
    double length = GetLength();
    *this /= length;
    return *this;
}

Vector3d* Vector3d::Normalized() {
    return &((new Vector3d(*this))->Normalize());
}

Vector3d::Vector3d(const Vector3d& other) {
    m_x = other.m_x;
    m_y = other.m_y;
    m_z = other.m_z;
}

Vector3d& Vector3d::operator=(const Vector3d& other) {
    if (this != &other) {
        m_x = other.GetX();
        m_y = other.GetY();
        m_z = other.GetZ();
    }

    return *this;
}

Vector3d& Vector3d::operator+=(const Vector3d& other) {
    m_x += other.GetX();
    m_y += other.GetY();
    m_z += other.GetZ();

    return *this;
}

Vector3d& Vector3d::operator-=(const Vector3d& other) {
    m_x -= other.GetX();
    m_y -= other.GetY();
    m_z -= other.GetZ();

    return *this;
}

Vector3d& Vector3d::operator*=(const Vector3d& other) {
    m_x *= other.GetX();
    m_y *= other.GetY();
    m_z *= other.GetZ();

    return *this;
}

Vector3d& Vector3d::operator/=(const Vector3d& other) {
    m_x /= other.GetX();
    m_y /= other.GetY();
    m_z /= other.GetZ();

    return *this;
}

Vector3d& Vector3d::operator+=(double scalar) {
    m_x += scalar;
    m_y += scalar;
    m_z += scalar;

    return *this;
}

Vector3d& Vector3d::operator-=(double scalar) {
    m_x -= scalar;
    m_y -= scalar;
    m_z -= scalar;

    return *this;
}

Vector3d& Vector3d::operator*=(double scalar) {
    m_x *= scalar;
    m_y *= scalar;
    m_z *= scalar;

    return *this;
}

Vector3d& Vector3d::operator/=(double scalar) {
    m_x /= scalar;
    m_y /= scalar;
    m_z /= scalar;

    return *this;
}

bool Vector3d::operator==(const Vector3d& other) const {
    return m_x == other.GetX() && m_y == other.GetY() && m_z == other.GetZ();
}

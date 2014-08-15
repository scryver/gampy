__author__ = 'michiel'

from gampy.engine.objects.vectors import Vector3
import numbers


class BaseLight:

    def __init__(self, color, intensity):
        self._color = None
        self._intensity = None
        
        self.color = color
        self.intensity = intensity

    @property
    def color(self):
        return self._color
    @color.setter
    def color(self, color):
        if not isinstance(color, Vector3):
            raise AttributeError('Color {} is not a vector'.format(color))
        self._color = color

    @property
    def intensity(self):
        return self._intensity

    @intensity.setter
    def intensity(self, intensity):
        if not isinstance(intensity, numbers.Number):
            raise AttributeError('Intensity {} is not a number'.format(intensity))
        self._intensity = float(intensity)


class DirectionalLight:

    def __init__(self, base_light, direction):
        self._base = None
        self._direction = None

        self.base = base_light
        self.direction = direction

    @property
    def base(self):
        return self._base
    @base.setter
    def base(self, base):
        if not isinstance(base, BaseLight):
            raise AttributeError('Base {} is not a BaseLight'.format(base))
        self._base = base

    @property
    def direction(self):
        return self._direction
    @direction.setter
    def direction(self, direction):
        if not isinstance(direction, Vector3):
            raise AttributeError('Direction {} is not a vector'.format(direction))
        self._direction = direction.normalized()


class PointLight:

    def __init__(self, base_light, attenuation, position, range_value):
        self._base = None
        self._attenuation = None
        self._position = None
        self._range = None

        self.base = base_light
        self.attenuation = attenuation
        self.position = position
        self.range = range_value

    @property
    def base(self):
        return self._base
    @base.setter
    def base(self, base):
        if not isinstance(base, BaseLight):
            raise AttributeError('Base {} is not a BaseLight'.format(base))
        self._base = base

    @property
    def attenuation(self):
        return self._attenuation
    @attenuation.setter
    def attenuation(self, attenuation):
        if not isinstance(attenuation, Attenuation):
            raise AttributeError('Attenuation {} is not a Attenuation'.format(attenuation))
        self._attenuation = attenuation

    @property
    def position(self):
        return self._position
    @position.setter
    def position(self, position):
        if not isinstance(position, Vector3):
            raise AttributeError('Position {} is not a vector'.format(position))
        self._position = position

    @property
    def range(self):
        return self._range

    @range.setter
    def range(self, range_value):
        if not isinstance(range_value, numbers.Number):
            raise AttributeError('Range {} is not a number'.format(range_value))
        self._range = float(range_value)


class SpotLight:

    def __init__(self, point_light, direction, cutoff):
        self._point_light = None
        self._direction = None
        self._cutoff = None

        self.point_light = point_light
        self.direction = direction
        self.cutoff = cutoff

    @property
    def point_light(self):
        return self._point_light
    @point_light.setter
    def point_light(self, point_light):
        if not isinstance(point_light, PointLight):
            raise AttributeError('Point Light {} is not a PointLight'.format(point_light))
        self._point_light = point_light

    @property
    def direction(self):
        return self._direction
    @direction.setter
    def direction(self, direction):
        if not isinstance(direction, Vector3):
            raise AttributeError('Direction {} is not a vector'.format(direction))
        self._direction = direction.normalized()

    @property
    def cutoff(self):
        return self._cutoff

    @cutoff.setter
    def cutoff(self, cutoff):
        if not isinstance(cutoff, numbers.Number):
            raise AttributeError('Cutoff {} is not a number'.format(cutoff))
        self._cutoff = float(cutoff)


class Attenuation:

    def __init__(self, constant, linear, exponent):
        self._constant = 0.
        self._linear = 0.
        self._exponent = 1.

        self.constant = constant
        self.linear = linear
        self.exponent = exponent

    @property
    def constant(self):
        return self._constant

    @constant.setter
    def constant(self, constant):
        if not isinstance(constant, numbers.Number):
            raise AttributeError('Constant {} is not a number'.format(constant))
        self._constant = abs(float(constant))


    @property
    def linear(self):
        return self._linear

    @linear.setter
    def linear(self, linear):
        if not isinstance(linear, numbers.Number):
            raise AttributeError('Linear {} is not a number'.format(linear))
        self._linear = abs(float(linear))


    @property
    def exponent(self):
        return self._exponent

    @exponent.setter
    def exponent(self, exponent):
        if not isinstance(exponent, numbers.Number):
            raise AttributeError('Exponent {} is not a number'.format(exponent))
        self._exponent = abs(float(exponent))

__author__ = 'michiel'

import gampy.engine.core.util as core_util
import gampy.engine.render.forwardpass as forwardpass
from gampy.engine.components.gamecomponent import GameComponent
from gampy.engine.core.vectors import Vector3
import math


class BaseLight(GameComponent):

    def __init__(self, color, intensity):
        super().__init__()
        self._color = None
        self._intensity = None
        self._shader = None

        self.color = color
        self.intensity = intensity

    @property
    def shader(self):
        return self._shader
    @shader.setter
    def shader(self, shader):
        self._shader = shader

    @property
    def color(self):
        return self._color
    @color.setter
    def color(self, color):
        color = core_util.is_instance(color, 'Color', Vector3)
        self._color = color

    @property
    def intensity(self):
        return self._intensity

    @intensity.setter
    def intensity(self, intensity):
        intensity = core_util.is_float(intensity, 'Intensity')
        self._intensity = float(intensity)

    def add_to_render_engine(self, rendering_engine):
        rendering_engine.add_light(self)


class DirectionalLight(BaseLight):

    def __init__(self, color, intensity, direction):
        super(DirectionalLight, self).__init__(color, intensity)
        self._direction = None
        self._shader = forwardpass.Directional.get_instance()

        self.direction = direction

    @property
    def direction(self):
        return self._direction
    @direction.setter
    def direction(self, direction):
        direction = core_util.is_instance(direction, 'Direction', Vector3)
        self._direction = direction.normalized()


class PointLight(BaseLight):

    COLOR_DEPTH = 256

    def __init__(self, color, intensity, attenuation):
        super().__init__(color, intensity)
        self._attenuation = Vector3(0, 0, 1)
        self._shader = forwardpass.Point.get_instance()

        self.attenuation = attenuation
        self.calc_range()

    @property
    def attenuation(self):
        return self._attenuation
    @attenuation.setter
    def attenuation(self, attenuation):
        attenuation = core_util.is_instance(attenuation, 'Attenuation', Vector3)
        self.constant = attenuation.x
        self.linear = attenuation.y
        self.exponent = attenuation.z

    @property
    def constant(self):
        return self._attenuation.x
    @constant.setter
    def constant(self, constant):
        constant = core_util.is_float(constant, 'Constant')
        self._attenuation.x = abs(constant)

    @property
    def linear(self):
        return self._attenuation.y
    @linear.setter
    def linear(self, linear):
        linear = core_util.is_float(linear, 'Linear')
        self._attenuation.y = abs(linear)

    @property
    def exponent(self):
        return self._attenuation.z
    @exponent.setter
    def exponent(self, exponent):
        exponent = core_util.is_float(exponent, 'Exponent')
        self._attenuation.z = abs(exponent)

    def calc_range(self):
        a = self.exponent
        b = self.linear
        c = self.constant - self.COLOR_DEPTH * self.intensity * self.color.max()
        self.range = (-b + math.sqrt(b * b - 4 * a * c)) / (2 * a)


class SpotLight(PointLight):

    def __init__(self, color, intensity, attenuation, direction, cutoff):
        super().__init__(color, intensity, attenuation)
        self._direction = None
        self._cutoff = None
        self._shader = forwardpass.Spot.get_instance()

        self.direction = direction
        self.cutoff = cutoff

    @property
    def direction(self):
        return self._direction
    @direction.setter
    def direction(self, direction):
        direction = core_util.is_instance(direction, 'Direction', Vector3)
        self._direction = direction.normalized()

    @property
    def cutoff(self):
        return self._cutoff
    @cutoff.setter
    def cutoff(self, cutoff):
        cutoff = core_util.is_float(cutoff, 'Cutoff')
        self._cutoff = cutoff
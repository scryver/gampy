__author__ = 'michiel'

from gampy.engine.components.gamecomponent import GameComponent
from gampy.engine.render.shader import Shader
import math


class BaseLight(GameComponent):

    def __init__(self, color, intensity):
        super().__init__()
        self.color = color
        self.intensity = intensity

    @property
    def shader(self):
        return self._shader
    @shader.setter
    def shader(self, shader):
        self._shader = shader

    def add_to_render_engine(self, render_engine):
        render_engine.add_light(self)


class DirectionalLight(BaseLight):

    def __init__(self, color, intensity):
        super(DirectionalLight, self).__init__(color, intensity)
        self._shader = Shader('forward_directional')

    @property
    def direction(self):
        return self.transform.transformed_rotation().forward


class PointLight(BaseLight):

    COLOR_DEPTH = 256

    def __init__(self, color, intensity, attenuation):
        super().__init__(color, intensity)
        self._shader = Shader('forward_point')

        constant, linear, exponent = attenuation
        self.constant = constant
        self.linear = linear
        self.exponent = exponent
        self.calc_range()

    @property
    def attenuation(self):
        return self.constant, self.linear, self.exponent
    @attenuation.setter
    def attenuation(self, attenuation):
        c, l, e = attenuation
        self.constant = c
        self.linear = l
        self.exponent = e

    def calc_range(self):
        a = self.exponent
        b = self.linear
        c = self.constant - self.COLOR_DEPTH * self.intensity * self.color.max()
        self.range = (-b + math.sqrt(b * b - 4 * a * c)) / (2 * a)


class SpotLight(PointLight):

    def __init__(self, color, intensity, attenuation, cutoff):
        super().__init__(color, intensity, attenuation)
        self._shader = Shader('forward_spot')

        self.cutoff = cutoff

    @property
    def direction(self):
        return self.transform.transformed_rotation().forward
__author__ = 'michiel'

import gampy.engine.render.forwardpass as forwardpass
from gampy.engine.components.gamecomponent import GameComponent
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

    def add_to_render_engine(self, rendering_engine):
        rendering_engine.add_light(self)


class DirectionalLight(BaseLight):

    def __init__(self, color, intensity, direction):
        super(DirectionalLight, self).__init__(color, intensity)
        self._shader = forwardpass.Directional.get_instance()
        self.direction = direction


class PointLight(BaseLight):

    COLOR_DEPTH = 256

    def __init__(self, color, intensity, attenuation):
        super().__init__(color, intensity)
        self._shader = forwardpass.Point.get_instance()

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
        self._shader = forwardpass.Spot.get_instance()

        self.cutoff = cutoff

    @property
    def direction(self):
        return self.transform.rotation.forward
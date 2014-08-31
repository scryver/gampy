__author__ = 'michiel'

from gampy.engine.components.entitycomponent import EntityComponent
from gampy.engine.render.shader import Shader
from gampy.engine.core.math3d import Matrix4
import math


class ShadowInfo:

    def __init__(self, projection=None, bias=0., flip_faces=True):
        if projection is None:
            projection = Matrix4()
        self._projection = projection
        self._bias= bias
        self._flip_faces = flip_faces

    @property
    def projection(self):
        return self._projection

    @property
    def bias(self):
        return self._bias

    @property
    def flip_faces(self):
        return self._flip_faces


class BaseLight(EntityComponent):

    def __init__(self, color, intensity):
        super().__init__()
        self.color = color
        self.intensity = intensity
        self.shadow_info = None

    @property
    def shader(self):
        return self._shader
    @shader.setter
    def shader(self, shader):
        self._shader = shader

    def add_to_engine(self, engine):
        engine.render_engine.add_light(self)


class DirectionalLight(BaseLight):

    def __init__(self, color, intensity):
        super(DirectionalLight, self).__init__(color, intensity)
        self._shader = Shader('forward_directional')
        self.shadow_info = ShadowInfo(Matrix4().init_orthographic(-40, 40, -40, 40, -40, 40), 1.0, True)

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

    def __init__(self, color, intensity, attenuation, view_angle):
        super().__init__(color, intensity, attenuation)
        self._shader = Shader('forward_spot')

        self.cutoff = math.cos(view_angle/2)

    @property
    def direction(self):
        return self.transform.transformed_rotation().forward
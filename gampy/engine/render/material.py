__author__ = 'michiel'


from gampy.engine.render.texture import Texture
from gampy.engine.objects.vectors import Vector3
import numbers


class Material:

    def __init__(self, texture, color=Vector3(1, 1, 1), spec_intensity=1, spec_exp=8):
        self._tex = None
        self._color = None
        self._specular_intensity = None
        self._specular_exponent = None

        self.texture = texture
        self.color = color
        self.specular_intensity = spec_intensity
        self.specular_exponent = spec_exp

    @property
    def texture(self):
        return self._tex

    @texture.setter
    def texture(self, texture):
        if texture is not None and not isinstance(texture, Texture):
            raise AttributeError('Texture is not a texture object')
        self._tex = texture

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, color):
        if not isinstance(color, Vector3):
            raise AttributeError('Color is not a vector')
        self._color = color

    @property
    def specular_intensity(self):
        return self._specular_intensity

    @specular_intensity.setter
    def specular_intensity(self, specular_intensity):
        if not isinstance(specular_intensity, numbers.Number):
            raise AttributeError('Specular intensity is not a number')
        self._specular_intensity = float(specular_intensity)

    @property
    def specular_exponent(self):
        return self._specular_exponent

    @specular_exponent.setter
    def specular_exponent(self, specular_exponent):
        if not isinstance(specular_exponent, numbers.Number):
            raise AttributeError('Specular exponent is not a number')
        self._specular_exponent = float(specular_exponent)
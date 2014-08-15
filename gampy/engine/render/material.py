__author__ = 'michiel'


from gampy.engine.render.texture import Texture
from gampy.engine.objects.vectors import Vector3


class Material:

    def __init__(self, texture, color):
        if texture is not None and not isinstance(texture, Texture):
            raise AttributeError('Texture is not a texture object')
        if color is not None and not isinstance(color, Vector3):
            raise AttributeError('Color is not a vector')

        self._tex = texture
        self._color = color

    @property
    def texture(self):
        return self._tex

    @texture.setter
    def set_texture(self, texture):
        self._tex = texture

    @property
    def color(self):
        return self._color

    @color.setter
    def set_color(self, color):
        self._color = color
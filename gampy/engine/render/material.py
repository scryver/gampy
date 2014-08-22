__author__ = 'michiel'

from gampy.engine.render.texture import Texture
from gampy.engine.render.resourcemanagement import MappedValue

class Material(MappedValue):

    def add_mapped_value(self, name, value):
        if isinstance(value, Texture):
            name = 'tex_' + name
            self._map.update({name: value})
        else:
            super().add_mapped_value(name, value)

    def get_mapped_value(self, name, type=None):
        result = super().get_mapped_value(name, type)
        if result is not None:
            return result

        if type == 'tex':
            return Texture('test.png')
        else:
            return False
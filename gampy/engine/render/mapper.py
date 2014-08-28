__author__ = 'michiel'

from gampy.engine.core.vectors import Vector3, Matrix4
from gampy.engine.render.texture import Texture


class MappedValue:

    def __init__(self):
        self._map = dict()

    def set_mapped_value(self, name, value):
        if isinstance(value, int):
            type = 'int'
        elif isinstance(value, float):
            type = 'float'
        elif isinstance(value, Vector3):
            type = 'vec3'
        elif isinstance(value, Matrix4):
            type = 'mat4'
        elif isinstance(value, Texture):
            type = 'tex'
        else:
            type = False

        if type:
            name = type + '_' + name
        self._map.update({name: value})

    def get_mapped_value(self, name, type=None, default=None):
        if type:
            name = type + '_' + name
        result = self._map.get(name, default)
        if result is not None:
            return result

        if type == 'int':
            return 0
        elif type == 'float':
            return 0.
        elif type == 'vec3':
            return Vector3()
        elif type == 'mat4':
            return Matrix4().init_identity()
        elif type == 'tex':
            return Texture('test.png')
        else:
            return False
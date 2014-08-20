__author__ = 'michiel'

import numbers

from gampy.engine.render.texture import Texture
from gampy.engine.core.vectors import Vector3


class Material:

    def __init__(self):
        self._material_map = dict()

    def add(self, name, value):
        self._material_map.update({name: value})

    def get(self, name, var_type='float'):
        result = self._material_map.get(name)
        if result is not None:
            return result

        if var_type == 'float':
            return 0.
        elif var_type == 'vector3':
            return Vector3()
        elif var_type == 'texture':
            return Texture('test.png')
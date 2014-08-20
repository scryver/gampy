__author__ = 'michiel'

import numbers

from gampy.engine.render.texture import Texture
from gampy.engine.core.vectors import Vector3


class Material:

    def __init__(self):
        self._material_map = dict()

    def add(self, name, value):
        self._material_map.update({name: value})

    def get(self, name):
        return self._material_map[name]
__author__ = 'michiel'

from gampy.engine.core.vectors import Vector3, Matrix4


class Transform:

    def __init__(self):
        self._position = Vector3(0.,0.,0.)
        self._rotation = Vector3(0., 0., 0.)
        self._scale  = Vector3(1., 1., 1.)

    def get_transformation(self):
        translation = Matrix4().init_translation(self._position.x,
                                                self._position.y,
                                                self._position.z)

        rotation = Matrix4().init_rotation(self._rotation.x,
                                          self._rotation.y,
                                          self._rotation.z)

        scale = Matrix4().init_scale(self._scale.x,
                                     self._scale.y,
                                     self._scale.z)

        transformation = translation * rotation * scale

        return transformation

    @property
    def position(self):
        return self._position
    @position.setter
    def position(self, value):
        try:
            x, y, z = value
        except:
            x, y, z = value, None, None

        if y == None and z == None and isinstance(x, Vector3):
            self._position = x
        else:
            self._position = Vector3(x, y, z)

    @property
    def rotation(self):
        return self._rotation
    @rotation.setter
    def rotation(self, value):
        try:
            x, y, z = value
        except:
            x, y, z = value, None, None

        if y == None and z == None and isinstance(x, Vector3):
            self._rotation = x
        else:
            self._rotation = Vector3(x, y, z)

    @property
    def scale(self):
        return self._scale
    @scale.setter
    def scale(self, value):
        try:
            x, y, z = value
        except:
            x, y, z = value, None, None

        if y == None and z == None and isinstance(x, Vector3):
            self._scale = x
        else:
            self._scale = Vector3(x, y, z)
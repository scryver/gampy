__author__ = 'michiel'

from gampy.engine.core.vectors import Vector3, Matrix4, Quaternion


class Transform:

    def __init__(self):
        self._position = Vector3()
        self._rotation = Quaternion()
        self._scale  = Vector3(1., 1., 1.)
        self._old_position = None
        self._old_rotation = None
        self._old_scale  = None
        # self._old_position = Vector3(0, 0, 0)
        # self._old_rotation = Quaternion(0, 0, 0, 0)
        # self._old_scale  = Vector3(0, 0, 0)
        self._parent = None
        self._parent_matrix = Matrix4().init_identity()

    def get_transformation(self):
        """For backward compatibility"""
        return self.transformation

    def has_changed(self):
        if self._old_position is None:
            self._old_position = Vector3(0, 0, 0).set(self._position)
            self._old_rotation = Quaternion(0, 0, 0, 0).set(self._rotation)
            self._old_scale  = Vector3(0, 0, 0).set(self._scale)
            return True

        if self._parent is not None and self._parent.has_changed():
            return True

        if self._position != self._old_position:
            return True

        if self._rotation != self._old_rotation:
            return True

        if self._scale != self._old_scale:
            return True

        return False

    @property
    def transformation(self):
        translation = Matrix4().init_translation(self._position.x,
                                                self._position.y,
                                                self._position.z)

        rotation = self._rotation.to_rotation_matrix()

        scale = Matrix4().init_scale(self._scale.x,
                                     self._scale.y,
                                     self._scale.z)

        if self._parent is not None and self._parent.has_changed():
            self._parent_matrix = self._parent.transformation

        if self._old_position is not None:
            self._old_position.set(self._position)
            self._old_rotation.set(self._rotation)
            self._old_scale.set(self._scale)

        return self._parent_matrix * translation * rotation * scale

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
            x, y, z, w = value
        except:
            x, y, z, w = value, None, None, None

        if y == None and z == None and w == None and isinstance(x, Quaternion):
            self._rotation = x
        else:
            self._rotation = Quaternion(x, y, z, w)

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

    @property
    def parent(self):
        return self._parent
    @parent.setter
    def parent(self, parent):
        self._parent = parent
__author__ = 'michiel'

from gampy.engine.core.vectors import Vector3, Matrix4, Quaternion


class Transform:

    def __init__(self):
        self.position = Vector3()
        self.rotation = Quaternion()
        self.scale  = Vector3(1., 1., 1.)
        self._translation_m = None
        self._rotation_m = None
        self._scale_m = None
        self._transformation = None
        self._old_position = None
        self._old_rotation = None
        self._old_scale  = None
        self._parent = None
        self._parent_matrix = Matrix4().init_identity()
        self._transformed_parent_m = self._parent_matrix.copy()

    def update(self):
        if self._old_position is not None:
            self._old_position = self._position.copy()
            self._old_rotation = self._rotation.copy()
            self._old_scale = self._scale.copy()
        else:
            self._old_position = Vector3(0, 0, 0).set(self._position) + 1.
            self._old_rotation = Quaternion(0, 0, 0, 0).set(self._rotation) * 0.5
            self._old_scale  = Vector3(0, 0, 0).set(self._scale) + 1.

    def rotate(self, axis, angle):
        self.rotation = (Quaternion(axis, angle) * self._rotation).view(Quaternion).normalized()

    def has_changed(self):
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
        if self._transformation is None or self.has_changed():
            if self._translation_m is None:
                self._translation_m = Matrix4().init_translation(self._position.x,
                                                                 self._position.y,
                                                                 self._position.z)
            if self._rotation_m is None:
                self._rotation_m = self._rotation.to_rotation_matrix()
            if self._scale_m is None:
                self._scale_m = Matrix4().init_scale(self._scale.x,
                                                     self._scale.y,
                                                     self._scale.z)

            self._transformation = self._get_parent_matrix() * self._translation_m * self._rotation_m * self._scale_m

        return self._transformation

    def _get_parent_matrix(self):
        if self._parent is not None and self._parent.has_changed():
            self._parent_matrix = self._parent.transformation
        return self._parent_matrix

    def transformed_position(self):
        if self.has_changed() or self._parent.has_changed():
            self._transformed_parent_m = self._get_parent_matrix().transform(self._position)
        return self._transformed_parent_m

    def transformed_rotation(self):
        parent_rotation = Quaternion()

        # if self._parent is not None and self._parent.has_changed():
        if self._parent is not None:
            parent_rotation = self._parent.transformed_rotation()

        return parent_rotation * self._rotation

    def look_at(self, point, up):
        self.rotation = self.look_at_direction(point, up)

    def look_at_direction(self, point, up):
        return Quaternion(Matrix4().init_rotation((point - self.position).normalized(), up))

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

        self._translation_m = Matrix4().init_translation(self._position.x,
                                                         self._position.y,
                                                         self._position.z)

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

        self._rotation_m = self._rotation.to_rotation_matrix()

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

        self._scale_m = Matrix4().init_scale(self._scale.x,
                                             self._scale.y,
                                             self._scale.z)

    @property
    def parent(self):
        return self._parent
    @parent.setter
    def parent(self, parent):
        self._parent = parent
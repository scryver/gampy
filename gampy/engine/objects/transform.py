__author__ = 'michiel'

from gampy.engine.objects.vectors import Vector3, Matrix4


class Transform:

    def __init__(self):
        self.translation = Vector3(0.,0.,0.)
        self.rotation = Vector3(0., 0., 0.)
        self.scale  = Vector3(1., 1., 1.)

    def get_transformation(self):
        translation = Matrix4().initTranslation(self.translation.x,
                                                self.translation.y,
                                                self.translation.z)

        rotation = Matrix4().initRotation(self.rotation.x,
                                          self.rotation.y,
                                          self.rotation.z)

        scale = Matrix4().initScale(self.scale.x,
                                    self.scale.y,
                                    self.scale.z)

        transformation = translation * rotation * scale

        return transformation

    def set_translation(self, x, y=None, z=None):
        if y == None and z == None and isinstance(x, Vector3):
            self.translation = x
        else:
            self.translation = Vector3(x, y, z)

    def set_rotation(self, x, y=None, z=None):
        if y == None and z == None and isinstance(x, Vector3):
            self.rotation = x
        else:
            self.rotation = Vector3(x, y, z)

    def set_scale(self, x, y=None, z=None):
        if y == None and z == None and isinstance(x, Vector3):
            self.scale = x
        else:
            self.scale = Vector3(x, y, z)
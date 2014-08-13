__author__ = 'michiel'

from gampy.engine.objects.vectors import Vector3, Matrix4


class Transform:

    def __init__(self):
        self.translation = Vector3(0.,0.,0.)

    def get_transformation(self):
        translation = Matrix4().initTranslation(self.translation.x,
                                                self.translation.y,
                                                self.translation.z)

        return translation

    def set_translation(self, x, y=None, z=None):
        if y == None and z == None and isinstance(x, Vector3):
            self.translation = x
        else:
            self.translation = Vector3(x, y, z)
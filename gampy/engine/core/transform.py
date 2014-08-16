__author__ = 'michiel'

from gampy.engine.core.vectors import Vector3, Matrix4


class Transform:

    camera = None

    z_near = 0.1
    z_far = 100.0    #
    width = 800     # Width of screen
    height = 600    # Height of screen
    fov = 0.        # Field of view

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

        scale = Matrix4().init_scale(self.scale.x,
                                    self.scale.y,
                                    self.scale.z)

        transformation = translation * rotation * scale

        return transformation

    def get_projected_transformation(self):
        transformation = self.get_transformation()
        projection = Matrix4().init_projection(Transform.fov, Transform.width, Transform.height,
                                               Transform.z_near, Transform.z_far)
        camera_rotation = Matrix4().init_camera(Transform.camera.forward, Transform.camera.up)
        camera_translation = Matrix4().initTranslation(-Transform.camera.pos.x,
                                                       -Transform.camera.pos.y,
                                                       -Transform.camera.pos.z)

        return projection * camera_rotation * camera_translation * transformation


    @classmethod
    def set_projection(cls, fov, width, height, z_near, z_far):
        cls.fov = fov
        cls.width = width
        cls.height = height
        cls.z_near = z_near
        cls.z_far = z_far

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
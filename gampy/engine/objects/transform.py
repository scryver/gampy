__author__ = 'michiel'

# from gampy.engine.objects.vectors import Vector3
# from gampy.engine.objects.vectors import Matrix4
from gampy.core import Matrix4, Vector3
from gampy.engine.events.time import Timing

timings = Timing('Transform')


class Transform:

    z_near = 0.1
    z_far = 100.0    #
    width = 800     # Width of screen
    height = 600    # Height of screen
    fov = 70.        # Field of view
    projection = Matrix4().init_projection(
        fov,
        width,
        height,
        z_near,
        z_far
    )

    def __init__(self):
        self.translation = Vector3(0., 0., 0.)
        self.rotation = Vector3(0., 0., 0.)
        self.scale = Vector3(1., 1., 1.)
        self.projMat = None
        self.is_changed = True

    @timings
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

    @timings
    def get_projected_transformation(self):
        if self.is_changed:
            transformation = self.get_transformation()
            self.projMat = self.projection * transformation
            self.is_changed = False

        return self.projMat

    @classmethod
    def set_projection(cls, fov, width, height, z_near, z_far):
        cls.fov = fov
        cls.width = width
        cls.height = height
        cls.z_near = z_near
        cls.z_far = z_far
        cls.projection = Matrix4().init_projection(
            fov,
            width,
            height,
            z_near,
            z_far
        )

    def set_translation(self, x, y=None, z=None):
        if y is None and z is None and isinstance(x, Vector3):
            self.translation = x
        else:
            self.translation = Vector3(x, y, z)
        self.is_changed = True

    def set_rotation(self, x, y=None, z=None):
        if y is None and z is None and isinstance(x, Vector3):
            self.rotation = x
        else:
            self.rotation = Vector3(x, y, z)
        self.is_changed = True

    def set_scale(self, x, y=None, z=None):
        if y is None and z is None and isinstance(x, Vector3):
            self.scale = x
        else:
            self.scale = Vector3(x, y, z)
        self.is_changed = True

    def __del__(self):
        print(timings)

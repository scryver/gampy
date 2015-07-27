__author__ = 'michiel'

import math

from gampy.engine.core.math3d import Matrix4
from gampy.engine.core.coreengine import Window
from gampy.engine.components.entitycomponent import EntityComponent
import gampy.engine.core.time as timing


timer = timing.Timing()


class Camera(EntityComponent):

    _is_printed = False

    def __init__(self, fov=None, aspect=None, z_near=None, z_far=None):
        super().__init__()
        if fov is None:
            fov = math.radians(70.)
        if aspect is None:
            aspect = Window.width / Window.height
        if z_near is None:
            z_near = 0.1
        if z_far is None:
            z_far = 1000.
        if isinstance(fov, Matrix4):
            self.projection = fov
        else:
            self.projection = Matrix4().init_perspective(fov, aspect, z_near, z_far)

        self._transformation = None

    @timer
    def view_projection(self):
        if self._transformation is None or self.transform.has_changed():
            camera_rotation = self.transform.transformed_rotation().conjugate().to_rotation_matrix()
            camera_position = self.transform.transformed_position() * -1.
            camera_translation = Matrix4().init_translation(camera_position.x,
                                                            camera_position.y,
                                                            camera_position.z)
            self._transformation = self.projection * camera_rotation * camera_translation

        return self._transformation

    def add_to_engine(self, engine):
        engine.render_engine.add_camera(self)

    def __del__(self):
        if not Camera._is_printed:
            Camera._is_printed = True
            print('========CAMERA=======================================================================',
                  timer,
                  '=====================================================================================', sep='\n')
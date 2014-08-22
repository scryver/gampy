__author__ = 'michiel'


from gampy.engine.core.vectors import Vector3, Matrix4, Quaternion
from gampy.engine.core.input import Input
from gampy.engine.core.coreengine import Window
from gampy.engine.components.gamecomponent import GameComponent
import math


class Camera(GameComponent):

    # The global up vector
    y_axis = Vector3(0., 1., 0.)

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
        self.projection = Matrix4().init_perspective(fov, aspect, z_near, z_far)

        self.mouse_locked = False
        self._transformation = None

    def view_projection(self):
        if self._transformation is None or self.transform.has_changed():
            camera_rotation = self.transform.transformed_rotation().conjugate().to_rotation_matrix()
            camera_position = self.transform.transformed_position() * -1.
            camera_translation = Matrix4().init_translation(camera_position.x,
                                                            camera_position.y,
                                                            camera_position.z)
            self._transformation = self.projection * camera_rotation * camera_translation

        return self._transformation

    def add_to_render_engine(self, render_engine):
        render_engine.add_camera(self)

    def input(self, dt):
        sensitivity = 0.5
        move_amount = 10 * dt

        if Input.get_key(Input.KEY_ESCAPE):
            Input.set_cursor(True)
            self.mouse_locked = False
        if Input.get_mouse_down(Input.MOUSE_MIDDLE):
            Input.set_cursor(False)
            Input.set_mouse_position(Window.center.x, Window.center.y)
            self.mouse_locked = True

        if Input.get_key(Input.KEY_W):
            self.move(self.transform.rotation.forward, move_amount)
        if Input.get_key(Input.KEY_S):
            self.move(self.transform.rotation.forward, -move_amount)
        if Input.get_key(Input.KEY_A):
            self.move(self.transform.rotation.left, move_amount)
        if Input.get_key(Input.KEY_D):
            self.move(self.transform.rotation.right, move_amount)

        if self.mouse_locked:
            delta_position = Input.mouse_position() - Window.center
            rot = False
            if delta_position.x != 0:
                self.transform.rotate(Camera.y_axis, math.radians(delta_position.x * sensitivity))
                rot = True
            if delta_position.y != 0:
                self.transform.rotate(self.transform.rotation.right, math.radians(delta_position.y * sensitivity))
                rot = True

            if rot:
                Input.set_mouse_position(Window.center.x, Window.center.y)

            if Input.get_mouse(Input.MOUSE_LEFT):
                self.move(self.transform.rotation.forward, move_amount)
            if Input.get_mouse(Input.MOUSE_RIGHT):
                self.move(self.transform.rotation.forward, -move_amount)


    def move(self, direction, amount):
        result = self.transform.position + direction * amount
        self.transform.position = result
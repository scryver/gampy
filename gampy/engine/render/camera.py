__author__ = 'michiel'


from gampy.engine.core.vectors import Vector3, Matrix4
from gampy.engine.core.input import Input
from gampy.engine.core.coreengine import Window, Time


class Camera:

    # The global up vector
    y_axis = Vector3(0., 1., 0.)

    def __init__(self, fov, aspect, z_near, z_far, position=None, forward=None, up=None):
        if position == None:
            position = Vector3(0., 0., 0.)
        if forward == None:
            forward = Vector3(0., 0., 1.)
        if up == None:
            up = Vector3(0., 1., 0.)

        if not isinstance(position, Vector3):
            raise AttributeError('Position of the camera is not a vector')
        if not isinstance(up, Vector3):
            raise AttributeError('Up direction of the camera is not a vector')
        if not isinstance(forward, Vector3):
            raise AttributeError('Forward direction of the camera is not a vector')

        self.position = position
        self.up = up.normalized()
        self.forward = forward.normalized()
        self.projection = Matrix4().init_perspective(fov, aspect, z_near, z_far)

        self.mouse_locked = False

    def view_projection(self):
        camera_rotation = Matrix4().init_rotation(self.forward, self.up)
        camera_translation = Matrix4().init_translation(-self.position.x, -self.position.y, -self.position.z)

        return self.projection * camera_rotation * camera_translation

    def input(self, dt):
        sensitivity = 0.5
        move_amount = 10 * dt
        # rot_amount = 100. * dt

        if Input.get_key(Input.KEY_ESCAPE):
            Input.set_cursor(True)
            self.mouse_locked = False
        if Input.get_mouse_down(Input.MOUSE_MIDDLE):
            Input.set_cursor(False)
            Input.set_mouse_position(Window.center.x, Window.center.y)
            self.mouse_locked = True

        if Input.get_key(Input.KEY_W):
            self.move(self.forward, move_amount)
        if Input.get_key(Input.KEY_S):
            self.move(self.forward, -move_amount)
        if Input.get_key(Input.KEY_A):
            self.move(self.left, move_amount)
        if Input.get_key(Input.KEY_D):
            self.move(self.right, move_amount)

        if self.mouse_locked:
            delta_position = Input.mouse_position() - Window.center
            rot = False
            if delta_position.x != 0:
                self.rotate_y(delta_position.x * sensitivity)
                rot = True
            if delta_position.y != 0:
                self.rotate_x(delta_position.y * sensitivity)
                rot = True

            if rot:
                Input.set_mouse_position(Window.center.x, Window.center.y)

            if Input.get_mouse(Input.MOUSE_LEFT):
                self.move(self.forward, move_amount)
            if Input.get_mouse(Input.MOUSE_RIGHT):
                self.move(self.forward, -move_amount)


    def move(self, direction, amount):
        self.position = self.position + direction * amount

    def rotate_y(self, angle):
        h_axis = Camera.y_axis.cross(self.forward).normalized()

        self.forward = self.forward.rotate(angle, Camera.y_axis).normalized()

        self.up = self.forward.cross(h_axis).normalized()

    def rotate_x(self, angle):
        h_axis = Camera.y_axis.cross(self.forward).normalized()

        self.forward = self.forward.rotate(angle, h_axis).normalized()

        self.up = self.forward.cross(h_axis).normalized()

    @property
    def left(self):
        return self.forward.cross(self.up).normalized()

    @property
    def right(self):
        return self.up.cross(self.forward).normalized()
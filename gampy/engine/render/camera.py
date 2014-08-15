__author__ = 'michiel'


from gampy.engine.objects.vectors import Vector2, Vector3
import gampy.engine.input.input as gameinput


class Camera:

    # The global up vector
    y_axis = Vector3(0., 1., 0.)

    def __init__(self, pos=None, forward=None, up=None):
        if pos == None:
            pos = Vector3(0., 0., 0.)
        if forward == None:
            forward = Vector3(0., 0., 1.)
        if up == None:
            up = Vector3(0., 1., 0.)

        if not isinstance(pos, Vector3):
            raise AttributeError('Position of the camera is not a vector')
        if not isinstance(up, Vector3):
            raise AttributeError('Up direction of the camera is not a vector')
        if not isinstance(forward, Vector3):
            raise AttributeError('Forward direction of the camera is not a vector')

        self.pos = pos
        self.up = up.normalized()
        self.forward = forward.normalized()

        self.mouse_locked = False

    def input(self, inputs, dt, widget, width, height):
        sensitivity = 0.5
        move_amount = 10 * dt
        # rot_amount = 100. * dt

        if inputs.get_key(gameinput.KEY_ESCAPE):
            inputs.set_cursor(widget, True)
            self.mouse_locked = False
        if inputs.get_mouse_down(gameinput.MOUSE_MIDDLE):
            inputs.set_cursor(widget, False)
            inputs.set_mouse_position(widget, width / 2, height / 2)
            self.mouse_locked = True

        if inputs.get_key(gameinput.KEY_W):
            self.move(self.forward, move_amount)
        if inputs.get_key(gameinput.KEY_S):
            self.move(self.forward, -move_amount)
        if inputs.get_key(gameinput.KEY_A):
            self.move(self.left, move_amount)
        if inputs.get_key(gameinput.KEY_D):
            self.move(self.right, move_amount)

        if self.mouse_locked:
            delta_pos = inputs.mouse_position - Vector2(width / 2, height / 2)
            rot = False
            if delta_pos.x != 0:
                self.rotate_y(delta_pos.x * sensitivity)
                rot = True
            if delta_pos.y != 0:
                self.rotate_x(delta_pos.y * sensitivity)
                rot = True

            if rot:
                inputs.set_mouse_position(widget, width / 2, height / 2)

            if inputs.get_mouse(gameinput.MOUSE_LEFT):
                self.move(self.forward, move_amount)
            if inputs.get_mouse(gameinput.MOUSE_RIGHT):
                self.move(self.forward, -move_amount)


    def move(self, direction, amount):
        self.pos = self.pos + direction * amount

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
        left_vec = self.forward.cross(self.up).normalized()
        return left_vec

    @property
    def right(self):
        right_vec = self.up.cross(self.forward).normalized()
        return right_vec
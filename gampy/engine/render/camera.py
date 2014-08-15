__author__ = 'michiel'


from gampy.engine.objects.vectors import Vector3
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
        self.up = up
        self.forward = forward

        self.up.normalize()
        self.forward.normalize()

    def input(self, inputs, dt):
        move_amount = 10. * dt
        rot_amount = 100. * dt

        if inputs.get_key(gameinput.KEY_W):
            self.move(self.forward, move_amount)
        if inputs.get_key(gameinput.KEY_S):
            self.move(self.forward, -move_amount)
        if inputs.get_key(gameinput.KEY_A):
            self.move(self.left, move_amount)
        if inputs.get_key(gameinput.KEY_D):
            self.move(self.right, move_amount)

        if inputs.get_key(gameinput.KEY_UP):
            self.rotate_x(-rot_amount)
        if inputs.get_key(gameinput.KEY_DOWN):
            self.rotate_x(rot_amount)
        if inputs.get_key(gameinput.KEY_LEFT):
            self.rotate_y(-rot_amount)
        if inputs.get_key(gameinput.KEY_RIGHT):
            self.rotate_y(rot_amount)


    def move(self, direction, amount):
        self.pos = self.pos + direction * amount

    def rotate_y(self, angle):
        h_axis = Camera.y_axis.cross(self.forward)
        h_axis.normalize()

        self.forward.rotate(angle, Camera.y_axis)
        self.forward.normalize()

        self.up = self.forward.cross(h_axis)
        self.up.normalize()

    def rotate_x(self, angle):
        h_axis = Camera.y_axis.cross(self.forward)
        h_axis.normalize()

        self.forward.rotate(angle, h_axis)
        self.forward.normalize()

        self.up = self.forward.cross(h_axis)
        self.up.normalize()

    @property
    def left(self):
        left_vec = self.forward.cross(self.up)
        left_vec.normalize()
        return left_vec

    @property
    def right(self):
        right_vec = self.up.cross(self.forward)
        right_vec.normalize()
        return right_vec
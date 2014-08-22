__author__ = 'michiel'

import math

from gampy.engine.core.vectors import Vector3
from gampy.engine.tkinter.input import Input
from gampy.engine.core.coreengine import Window
from gampy.engine.components.gamecomponent import GameComponent


class FreeLook(GameComponent):

    # The global up vector
    y_axis = Vector3(0., 1., 0.)

    def __init__(self, sensitivity, unlock_mouse_key=None):
        """

        :param sensitivity: 0.5 is a sensible value
        :param unlock_mouse_key: the key to free the mouse of influencing the object
        :return:
        """
        super().__init__()

        self._mouse_locked = False
        self._sensitivity = sensitivity
        self._unlock_mouse = Input.KEY_ESCAPE if unlock_mouse_key is None else unlock_mouse_key

    def input(self, dt):
        if Input.get_key(self._unlock_mouse):
            Input.set_cursor(True)
            self._mouse_locked = False
        if Input.get_mouse_down(Input.MOUSE_MIDDLE):
            Input.set_cursor(False)
            Input.set_mouse_position(Window.center.x, Window.center.y)
            self._mouse_locked = True

        if self._mouse_locked:
            delta_position = Input.mouse_position() - Window.center
            rot = False
            if delta_position.x != 0:
                self.transform.rotate(FreeLook.y_axis, math.radians(delta_position.x * self._sensitivity))
                rot = True
            if delta_position.y != 0:
                self.transform.rotate(self.transform.rotation.right, math.radians(delta_position.y * self._sensitivity))
                rot = True

            if rot:
                Input.set_mouse_position(Window.center.x, Window.center.y)



class FreeMove(GameComponent):

    def __init__(self, speed: float, forward_key=None, back_key=None, left_key=None, right_key=None):
        """

        :param speed: 10 is a sensible value, it gets multiplied with the delta to move a object
        :param forward_key: The input key code (see Input class) to move forward, default = 'w'
        :param back_key: The input key code (see Input class) to move back, default = 's'
        :param left_key: The input key code (see Input class) to move left, default = 'a'
        :param right_key: The input key code (see Input class) to move right, default = 'd'
        :return:
        """
        super().__init__()
        self._speed = speed
        self._forward_key = Input.KEY_W if forward_key is None else forward_key
        self._back_key = Input.KEY_S if back_key is None else back_key
        self._left_key = Input.KEY_A if left_key is None else left_key
        self._right_key = Input.KEY_D if right_key is None else right_key

    def move(self, direction, amount):
        result = self.transform.position + direction * amount
        self.transform.position = result

    def input(self, dt):
        move_amount = self._speed * dt
        if Input.get_key(self._forward_key):
            self.move(self.transform.rotation.forward, move_amount)
        if Input.get_key(self._back_key):
            self.move(self.transform.rotation.forward, -move_amount)
        if Input.get_key(self._left_key):
            self.move(self.transform.rotation.left, move_amount)
        if Input.get_key(self._right_key):
            self.move(self.transform.rotation.right, move_amount)
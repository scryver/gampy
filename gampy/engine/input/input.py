#!/usr/bin/env python
__author__ = 'michiel'

import gampy.engine.objects.vectors as vectors
import ctypes
import sdl2

MOUSE_BUTTONS = {
    1: sdl2.SDL_BUTTON_LEFT,
    2: sdl2.SDL_BUTTON_MIDDLE,
    3: sdl2.SDL_BUTTON_RIGHT,
    4: sdl2.SDL_BUTTON_X1,
    5: sdl2.SDL_BUTTON_X2
}


class Input:
    def __init__(self):
        self.events = sdl2.SDL_Event()
        self._event_keys = {}
        self._last_keys = {}
        self._event_mouse = {}
        self._last_mouse = {}
        self._mouse_position = vectors.Vector2(0, 0)
        self._received_stop = False
        sdl2.SDL_SetRelativeMouseMode(True)

    def get_key(self, key_code):
        return self._event_keys.get(key_code, False)

    def get_key_down(self, key_code):
        return self.get_key(key_code) and not self._last_keys.get(key_code,
                                                                  False)

    def get_key_up(self, key_code):
        return not self.get_key(key_code) and self._last_keys.get(key_code,
                                                                  False)

    def get_mouse(self, mouse_button):
        mouse_button = MOUSE_BUTTONS[mouse_button]
        return self._event_mouse.get(mouse_button, False)

    def get_mouse_down(self, mouse_button):
        mouse_button = MOUSE_BUTTONS[mouse_button]
        return self.get_mouse(mouse_button) and \
            not self._last_mouse.get(mouse_button, False)

    def get_mouse_up(self, mouse_button):
        mouse_button = MOUSE_BUTTONS[mouse_button]
        return not self.get_mouse(mouse_button) and \
            self._last_mouse.get(mouse_button, False)

    def update(self):
        self._last_keys = dict(self._event_keys)
        self._last_mouse = dict(self._event_mouse)
        while sdl2.SDL_PollEvent(ctypes.byref(self.events)) != 0:
            if self.events.type == sdl2.SDL_QUIT or \
                (self.events.type == sdl2.SDL_KEYDOWN and
                 self.events.key.keysym.sym == sdl2.SDLK_ESCAPE):
                self._received_stop = True
            elif self.events.type == sdl2.SDL_KEYDOWN:
                self._event_keys[self.events.key.keysym.sym] = True
            elif self.events.type == sdl2.SDL_KEYUP:
                self._event_keys[self.events.key.keysym.sym] = False
            elif self.events.type == sdl2.SDL_MOUSEMOTION:
                self._mouse_position.x = self.events.motion.x
                self._mouse_position.y = self.events.motion.y
            elif self.events.type == sdl2.SDL_MOUSEBUTTONDOWN:
                self._event_mouse[self.events.button.button] = True
            elif self.events.type == sdl2.SDL_MOUSEBUTTONUP:
                self._event_mouse[self.events.button.button] = False

    @property
    def mouse_position(self):
        return self._mouse_position

    def should_stop(self):
        return self._received_stop

    def set_mouse_position(self, x, y):
        pass

    def destroy(self):
        pass


class KeyboardEvents(sdl2.SDL_KeyboardEvent):

    def __init__(self):
        super(KeyboardEvents, self).__init__()

        self.keys = []

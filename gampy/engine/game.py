__author__ = 'michiel'

import gampy.engine.input.input as gameinput

class Game:

    def __init__(self):
        pass

    def input(self, inputs):
        mouse_pos = inputs.mouse_position
        if inputs.get_key_down(gameinput.KEY_DOWN):
            print('We\'ve just pressed key DOWN')
        if inputs.get_key_up(gameinput.KEY_DOWN):
            print('We\'ve just released key DOWN')
        if inputs.get_mouse_down(1):
            print('We\'ve just pressed mouse Left at {}'.format(mouse_pos))
        if inputs.get_mouse_up(1):
            print('We\'ve just released mouse Left at {}'.format(mouse_pos))

    def update(self):
        pass

    def render(self):
        pass

    def destroy(self):
        pass
__author__ = 'michiel'

import sdl2
import math
import gampy.engine.input.input as game_input
from gampy.engine.render.shader import Shader
from gampy.engine.resource_loader import load_shader, load_mesh
from gampy.engine.objects.transform import Transform
# import gampy.engine.objects.util as util
from gampy.engine.events.time import Timing

timings = Timing()


class Game:

    def __init__(self, width, height):
        self.mesh = load_mesh('cube.obj')

        self.shader = Shader()

        self.shader.add_vertex_shader(load_shader('basic_vertex.vs', 'vertex'))
        self.shader.add_fragment_shader(load_shader('basic_fragment.fs',
                                                    'fragment'))
        self.shader.compile_shader()

        self.shader.add_uniform('transform')

        Transform.set_projection(70., width, height, 0.1, 1000.)
        self.transform = Transform()
        self.tmp = 0.

        self.inputs = game_input.Input()
        self.inputs.set_mouse_position(width // 2, height // 2)

    def input(self):
        self.inputs.update()
        mouse_pos = self.inputs.mouse_position
        if self.inputs.get_key_down(sdl2.SDLK_DOWN):
            print('We\'ve just pressed key DOWN')
        # if self.inputs.get_key(sdl2.SDLK_DOWN):
        #     print('We\'re pressing key DOWN')
        if self.inputs.get_key_up(sdl2.SDLK_DOWN):
            print('We\'ve just released key DOWN')
        if self.inputs.get_mouse_down(1):
            print('We\'ve just pressed mouse Left at {}'.format(mouse_pos))
        # if self.inputs.get_mouse(1):
        #     print('We\'re pressing mouse Left at {}'.format(mouse_pos))
        if self.inputs.get_mouse_up(1):
            print('We\'ve just released mouse Left at {}'.format(mouse_pos))

    def update(self, dt):
        self.tmp += dt
        self.transform.set_translation(math.cos(self.tmp), 0, 5)
        self.transform.set_rotation(math.sin(self.tmp) * 180,
                                    math.cos(self.tmp) * 180, 0)
        self.transform.set_scale(0.6 * math.sin(self.tmp) + 0.6,
                                 0.6 * math.sin(self.tmp) + 0.6,
                                 0.6 * math.sin(self.tmp) + 0.6)
        self.mesh.update(dt)

    @timings
    def render(self):
        self.shader.bind()
        self.shader.set_uniform('transform',
                                self.transform.get_projected_transformation())

        try:
            self.mesh.draw()
        finally:
            self.shader.unbind()

    def should_stop(self):
        return self.inputs.should_stop()

    def destroy(self):
        del self.mesh
        del self.shader
        self.inputs.destroy()

    def __del__(self):
        print("Game", timings)

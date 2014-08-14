__author__ = 'michiel'

import gampy.engine.input.input as gameinput
import gampy.engine.events.time as time
import gampy.engine.objects.meshes as meshes
import gampy.engine.objects.vectors as vec
import math
from gampy.engine.render.shader import Shader
from gampy.engine.resource_loader import load_shader, load_mesh
from gampy.engine.objects.transform import Transform
import gampy.engine.objects.util as util

class Game:

    def __init__(self, width, height):
        self.mesh = load_mesh('sphere.obj')

        self.shader = Shader()

        self.shader.add_vertex_shader(load_shader('basic_vertex_120.vs', 'vertex'))
        self.shader.add_fragment_shader(load_shader('basic_fragment_120.fs', 'fragment'))
        self.shader.compile_shader()

        self.shader.add_uniform('transform')

        self.transform = Transform()
        self.tmp = 0.

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

    def update(self, dt):
        self.tmp += dt
        self.transform.set_translation(math.cos(self.tmp), 0, 5)
        self.transform.set_rotation(0, math.cos(self.tmp) * 180, 0)
        # self.transform.set_scale(0.6 * math.cos(self.tmp), 0.6 * math.cos(self.tmp), 0.6 * math.cos(self.tmp))
        self.mesh.update(dt)

    def render(self):
        self.shader.bind()
        self.shader.set_uniform('transform', self.transform.get_projected_transformation())
        try:
            self.mesh.draw()
        finally:
            self.shader.unbind()

    def destroy(self):
        pass
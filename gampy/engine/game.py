__author__ = 'michiel'

import gampy.engine.input.input as gameinput
import gampy.engine.events.time as time
import gampy.engine.objects.meshes as meshes
import gampy.engine.objects.vectors as vec
import sdl2
import math
from gampy.engine.render.shader import Shader
from gampy.engine.resource_loader import load_shader
from gampy.engine.objects.transform import Transform

class Game:

    def __init__(self):
        self.mesh = meshes.Mesh()

        data = [
            meshes.Vertex(vec.Vector3(1., -1., 0.)),
            meshes.Vertex(vec.Vector3(-1., -1., 0.)),
            meshes.Vertex( vec.Vector3(0., 1., 0.)),
        ]
        self.mesh.add_vertices(data)

        self.shader = Shader()

        self.shader.add_vertex_shader(load_shader('basic_vertex.vs', 'vertex'))
        self.shader.add_fragment_shader(load_shader('basic_fragment.fs', 'fragment'))
        self.shader.compile_shader()

        self.shader.add_uniform('transform')

        self.transform = Transform()
        self.tmp = 0.

    def input(self, inputs):
        mouse_pos = inputs.mouse_position
        if inputs.get_key_down(sdl2.SDLK_DOWN):
            print('We\'ve just pressed key DOWN')
        if inputs.get_key_up(gameinput.KEY_DOWN):
            print('We\'ve just released key DOWN')
        if inputs.get_mouse_down(1):
            print('We\'ve just pressed mouse Left at {}'.format(mouse_pos))
        if inputs.get_mouse_up(1):
            print('We\'ve just released mouse Left at {}'.format(mouse_pos))

    def update(self, dt):
        self.tmp += dt
        self.transform.set_translation(math.cos(self.tmp), 0, 0)
        self.transform.set_rotation(0, 0, math.cos(self.tmp) * 180)
        self.transform.set_scale(math.cos(self.tmp), math.cos(self.tmp), math.cos(self.tmp))
        self.mesh.update(dt)

    def render(self):
        self.shader.bind()
        self.shader.set_uniform('transform', self.transform.get_transformation())
        try:
            self.mesh.draw()
        finally:
            self.shader.unbind()

    def destroy(self):
        pass
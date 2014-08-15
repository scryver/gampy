__author__ = 'michiel'

import gampy.engine.input.input as gameinput
import math
from gampy.engine.render.shader import BasicShader
from gampy.engine.render.material import Material
from gampy.engine.objects.vectors import Vector3
from gampy.engine.resource_loader import load_mesh, load_texture
from gampy.engine.objects.transform import Transform
from gampy.engine.render.camera import Camera
import gampy.engine.render.util as render_util


# Temp function
def test_mesh():
    import numpy
    from gampy.engine.objects.meshes import Mesh, Vertex
    from gampy.engine.objects.vectors import Vector2, Vector3
    mesh = Mesh()

    vertices = [
        Vertex(Vector3(-1, -1, -1), Vector2(0, 0)),
        Vertex(Vector3(0, 1, 0), Vector2(0.5, 0)),
        Vertex(Vector3(1, -1, -1), Vector2(1.0, 0)),
        Vertex(Vector3(0, -1, 1), Vector2(0, 0.5)),
    ]

    indices =[
        3, 1, 0,
        2, 1, 3,
        0, 1, 2,
        0, 2, 3,
    ]

    mesh.add_vertices(vertices, indices)

    return mesh


class Game:

    def __init__(self, width, height):
        self.mesh = test_mesh() # load_mesh('cube.obj')
        self.material = Material(load_texture('test.png'), Vector3(0, 1, 1))

        self.shader = BasicShader()
        self.camera = Camera()
        Transform.camera = self.camera

        self.transform = Transform()
        self.tmp = 0.

    def input(self, inputs, dt, widget):
        self.camera.input(inputs, dt, widget, Transform.width, Transform.height)
        # mouse_pos = inputs.mouse_position
        # if inputs.get_key_down(gameinput.KEY_DOWN):
        #     print('We\'ve just pressed key DOWN')
        # if inputs.get_key_up(gameinput.KEY_DOWN):
        #     print('We\'ve just released key DOWN')
        # if inputs.get_mouse_down(1):
        #     print('We\'ve just pressed mouse Left at {}'.format(mouse_pos))
        # if inputs.get_mouse_up(1):
        #     print('We\'ve just released mouse Left at {}'.format(mouse_pos))

    def update(self, dt):
        self.tmp += dt
        self.transform.set_translation(math.cos(self.tmp), 0, 5)
        # self.transform.set_rotation(0, math.cos(self.tmp) * 180, 0)
        # self.transform.set_scale(0.6 * math.cos(self.tmp), 0.6 * math.cos(self.tmp), 0.6 * math.cos(self.tmp))
        self.mesh.update(dt)

    def render(self):
        render_util.set_clear_color(abs(Transform.camera.pos / 2048.0))
        self.shader.bind()
        self.shader.update_uniforms(self.transform.get_transformation(),
                                    self.transform.get_projected_transformation(),
                                    self.material)
        try:
            self.mesh.draw()
        finally:
            self.shader.unbind()

    def destroy(self):
        pass
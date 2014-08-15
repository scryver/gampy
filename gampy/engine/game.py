__author__ = 'michiel'

import gampy.engine.input.input as gameinput
import math
from gampy.engine.render.shader import *
from gampy.engine.render.material import Material
from gampy.engine.render.texture import Texture
from gampy.engine.objects.vectors import Vector3
from gampy.engine.objects.transform import Transform
from gampy.engine.render.camera import Camera
import gampy.engine.render.util as render_util
from gampy.engine.objects.meshes import Mesh


# Temp function
def test_mesh():
    from gampy.engine.objects.meshes import Vertex
    from gampy.engine.objects.vectors import Vector2

    def create_block(depth, width):
        vertices = [
            Vertex(Vector3(-width, 0, -depth), Vector2(0, 0)),
            Vertex(Vector3(-width, 0, depth * 3), Vector2(0, 1)),
            Vertex(Vector3(width * 3, 0, -depth), Vector2(1, 0)),
            Vertex(Vector3(width * 3, 0, depth * 3), Vector2(1, 1))
        ]

        indices = [
            0, 1, 2,
            2, 1, 3,
        ]

        return vertices, indices

    def create_cube():
        vertices = [
            Vertex(Vector3(-1, -1, -1), Vector2(0, 0)),
            Vertex(Vector3(1, -1, -1), Vector2(0.5, 0)),
            Vertex(Vector3(1, 1, -1), Vector2(1.0, 0)),
            Vertex(Vector3(-1, 1, -1), Vector2(0, 0.5)),
            Vertex(Vector3(-1, 1, 1), Vector2(0, 0.5)),
            Vertex(Vector3(-1, -1, 1), Vector2(0.5, 0)),
            Vertex(Vector3(1, -1, 1), Vector2(0, 1.0)),
            Vertex(Vector3(1, 1, 1), Vector2(1.0, 1.0)),
        ]

        indices = [
            1, 2, 0, # Bottom 1
            0, 2, 3, # Bottom 2
            0, 3, 4, # Side1 1
            0, 4, 5, # Side1 2
            4, 3, 2, # Side2 1
            2, 7, 4, # Side2 2
            1, 7, 2, # Side3 1
            7, 1, 6, # Side3 2
            5, 1, 0, # Side4 1
            5, 6, 1, # Side4 2
            4, 6, 5, # Top 1
            4, 7, 6, # Top 2
        ]

        return vertices, indices

    # vertices = [
    #     Vertex(Vector3(-1, -1, 0.5773), Vector2(0, 0)),
    #     Vertex(Vector3(0, -1, -1.15475), Vector2(0.5, 0)),
    #     Vertex(Vector3(1, -1, 0.5773), Vector2(1.0, 0)),
    #     Vertex(Vector3(0, 1, 0), Vector2(0.5, 1)),
    # ]
    #
    # indices =[
    #     3, 1, 0,
    #     2, 1, 3,
    #     0, 1, 2,
    #     0, 2, 3,
    # ]

    vertices, indices = create_block(10, 10)

    mesh = Mesh(vertices, indices, True)

    return mesh


class Game:

    point_light_1 = lights.PointLight(lights.BaseLight(Vector3(1, 0.5, 0), 0.8), lights.Attenuation(0, 0, 1),
                                      Vector3(-2, 0, 5), 10)
    point_light_2 = lights.PointLight(lights.BaseLight(Vector3(0, 0.5, 1), 0.8), lights.Attenuation(0, 0, 1),
                                      Vector3(2, 0, 7), 10)

    spot_light_1 = lights.SpotLight(lights.PointLight(lights.BaseLight(Vector3(0, 1, 1), 0.8),
                                                      lights.Attenuation(0, 0, .05), Vector3(-2, 0, 5), 30),
                                    Vector3(1, 1, 1), 0.7)

    def __init__(self, width, height):
        PhongShader.ambient_light = Vector3(0.1, 0.1, 0.1)
        PhongShader.directional_light = lights.DirectionalLight(lights.BaseLight(Vector3(1, 1, 1), 0.8), Vector3(1, 1, 1))

        PhongShader.set_point_lights([Game.point_light_1, Game.point_light_2])
        PhongShader.set_spot_lights([Game.spot_light_1])

        self.mesh = test_mesh() # Mesh('cube.obj')
        self.material = Material(Texture('test.png'), Vector3(1, 1, 1))

        self.shader = PhongShader()
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
        self.transform.set_translation(0, -1, 5)
        # self.transform.set_rotation(0, math.cos(self.tmp) * 180, 0)
        # self.transform.set_scale(0.6 * math.cos(self.tmp), 0.6 * math.cos(self.tmp), 0.6 * math.cos(self.tmp))

        Game.point_light_1.position = Vector3(3, 0, 8. * (math.sin(self.tmp) + 1 / 2) + 10)
        Game.point_light_2.position = Vector3(3, 0, 8. * (math.cos(self.tmp) + 1 / 2) + 10)

        Game.spot_light_1.point_light.position = self.camera.pos
        Game.spot_light_1.direction = self.camera.forward

        self.mesh.update(dt)

    def render(self):
        render_util.set_clear_color(abs(Transform.camera.pos / 2048.0))
        self.shader.bind()
        self.shader.update_uniforms(self.transform.get_transformation(),
                                    self.transform.get_projected_transformation(),
                                    Transform.camera,
                                    self.material)
        try:
            self.mesh.draw()
        finally:
            self.shader.unbind()

    def destroy(self):
        pass
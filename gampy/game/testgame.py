__author__ = 'michiel'


from gampy.engine.render.material import Material
from gampy.engine.render.texture import Texture
from gampy.engine.render.window import Window
from gampy.engine.core.vectors import Vector3, Quaternion
from gampy.engine.render.meshes import Mesh
from gampy.engine.core.game import Game
from gampy.engine.core.gameobject import GameObject
from gampy.engine.core.transform import Transform
from gampy.engine.components.meshrenderer import MeshRenderer
from gampy.engine.components.camera import Camera
import gampy.engine.components.lights as light_components
import math


class TestGame(Game):

    def init(self):
        mesh = test_mesh('plane') # Mesh('cube.obj')
        material = Material(Texture('test.png'), Vector3(1, 1, 1))

        mesh_renderer = MeshRenderer(mesh, material)
        transform = Transform()

        plane_object = GameObject()
        plane_object.add_component(mesh_renderer)
        plane_object.transform.position.set(0, -1, 5)
        # plane_object.transform.rotation = 0, -45, 0

        directional_light_object = GameObject()
        directional_light = light_components.DirectionalLight(Vector3(0, 0.2, 0.8),
                                                              0.4,
                                                              Vector3(1, 1, 1))
        directional_light_object.add_component(directional_light)

        point_light_object = GameObject()
        point_light_object.transform.position.set(5, 0, 5)
        point_light = light_components.PointLight(Vector3(0, 1, 0), 0.4, (0, 0, 1))
        point_light_object.add_component(point_light)

        spot_light_object = GameObject()
        spot_light = light_components.SpotLight(Vector3(0, 1, 1), 0.4, (0, 0, .1), 0.7)
        spot_light_object.add_component(spot_light)
        spot_light_object.transform.position.set(5, 0.2, 5)
        spot_light_object.transform.rotation = Quaternion(Vector3(0, 1, 0), math.radians(90))

        self.root_object.add_child(plane_object)
        self.root_object.add_child(directional_light_object)
        self.root_object.add_child(point_light_object)
        self.root_object.add_child(spot_light_object)
        self.root_object.add_child(GameObject().add_component(Camera()))

# Temp function
def test_mesh(type):
    from gampy.engine.render.meshes import Vertex
    from gampy.engine.core.vectors import Vector2

    def create_plane(depth, width):
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

    def create_cube(*args):
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

    def create_pyramid(*args):
        vertices = [
            Vertex(Vector3(-1, -1, 0.5773), Vector2(0, 0)),
            Vertex(Vector3(0, -1, -1.15475), Vector2(0.5, 0)),
            Vertex(Vector3(1, -1, 0.5773), Vector2(1.0, 0)),
            Vertex(Vector3(0, 1, 0), Vector2(0.5, 1)),
        ]

        indices =[
            3, 1, 0,
            2, 1, 3,
            0, 1, 2,
            0, 2, 3,
        ]

        return vertices, indices

    func_name = locals()['create_' + type]
    vertices, indices = func_name(10, 10)

    mesh = Mesh(vertices, indices, True)

    return mesh
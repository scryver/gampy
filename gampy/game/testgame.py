__author__ = 'michiel'


from gampy.engine.render.material import Material
from gampy.engine.render.texture import Texture
from gampy.engine.core.vectors import Vector3
from gampy.engine.core.transform import Transform
from gampy.engine.render.camera import Camera
from gampy.engine.render.meshes import Mesh
from gampy.engine.core.game import Game
from gampy.engine.core.gameobject import GameObject
from gampy.engine.core.coreengine import Window
from gampy.game.meshrenderer import MeshRenderer



# Temp function
def test_mesh():
    from gampy.engine.render.meshes import Vertex
    from gampy.engine.core.vectors import Vector2

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


class TestGame(Game):

    def init(self):
        mesh = test_mesh() # Mesh('cube.obj')
        material = Material(Texture('test.png'), Vector3(1, 1, 1))

        mesh_renderer = MeshRenderer(mesh, material)

        plane_object = GameObject()
        plane_object.add_component(mesh_renderer)

        self.root_object.add_child(plane_object)

        plane_object.transform.position = 0, -1, 5
        plane_object.transform.rotation = 0, -45, 0

    def input(self):
        super().input()

    def destroy(self):
        pass
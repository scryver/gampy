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
import gampy.engine.core.time as timing

timer = timing.Timing()


class TestGame(Game):

    @timer
    def init(self):
        mesh = test_mesh('plane', 10, 10) # Mesh('cube.obj')
        mesh2 = test_mesh('plane', 1, 1)
        material = Material() # (Texture('test.png'), Vector3(1, 1, 1))
        material.add('diffuse', Texture('test.png'))
        material.add('specular_intensity', 1.)
        material.add('specular_exponent', 8.)

        mesh_renderer = MeshRenderer(mesh, material)

        plane_object = GameObject()
        plane_object.add_component(mesh_renderer)
        plane_object.transform.position = (0, -1, 5)
        # plane_object.transform.rotation = 0, -45, 0

        directional_light_object = GameObject()
        directional_light = light_components.DirectionalLight(Vector3(0, 0.2, 0.8),
                                                              0.4)
        directional_light_object.add_component(directional_light)
        directional_light.transform.rotation = Quaternion(Vector3(1, 0, 0), math.radians(-45))

        point_light_object = GameObject()
        # point_light_object.transform.position.set(5, 0, 5)
        point_light = light_components.PointLight(Vector3(0, 1, 0), 0.4, (0, 0, 1))
        point_light_object.add_component(point_light)

        spot_light_object = GameObject()
        spot_light = light_components.SpotLight(Vector3(0, 1, 1), 0.4, (0, 0, .1), 0.7)
        spot_light_object.add_component(spot_light)
        spot_light_object.transform.position = (5, 0.2, 5)
        spot_light_object.transform.rotation = Quaternion(Vector3(0, 1, 0), math.radians(90))

        self.add_object(plane_object)
        self.add_object(directional_light_object)
        self.add_object(point_light_object)
        self.add_object(spot_light_object)

        test_mesh_1 = GameObject().add_component(MeshRenderer(mesh2, material))
        test_mesh_2 = GameObject().add_component(MeshRenderer(mesh2, material))

        test_mesh_1.transform.position = (0, 2, 0)
        test_mesh_1.transform.rotation = Quaternion(Vector3(0, 1, 0), math.radians(45))
        test_mesh_2.transform.position = (0, 0, 5)

        test_mesh_1.add_child(test_mesh_2)
        test_mesh_2.add_child(GameObject().add_component(Camera()))

        self.add_object(test_mesh_1)

        # temp_mesh = Mesh('monkey.obj')
        # temp_material = Material() # (Texture('test.png'), Vector3(1, 1, 1))
        # temp_material.add('diffuse', Texture('tegre_skin.jpg'))
        # temp_material.add('specular_intensity', 1.)
        # temp_material.add('specular_exponent', 8.)
        # test_mesh_3 = GameObject().add_component(MeshRenderer(temp_mesh, temp_material))
        # self.add_object(test_mesh_3)
        # test_mesh_3.transform.position = 5, 5, 5
        # test_mesh_3.transform.rotation = Quaternion(Vector3(0, 1, 0), math.radians(70))
        #
        # self.add_object(GameObject().add_component(MeshRenderer(Mesh('monkey.obj'), material)))

    @timer
    def input(self, dt):
        super().input(dt)

    @timer
    def update(self, dt):
        super().update(dt)

    @timer
    def render(self, render_engine):
        super().render(render_engine)

    def __del__(self):
        print('========GAME=========================================================================',
              timer,
              '=====================================================================================', sep='\n')

# Temp function
def test_mesh(type, *args):
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
    vertices, indices = func_name(*args)

    mesh = Mesh(vertices, indices, True)

    return mesh
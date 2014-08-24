__author__ = 'michiel'


from gampy.engine.render.material import Material
from gampy.engine.render.texture import Texture
from gampy.engine.core.vectors import Vector3, Quaternion, Matrix4
from gampy.engine.render.meshes import Mesh
from gampy.engine.core.game import Game
from gampy.engine.tkinter.input import Input
from gampy.engine.core.gameobject import GameObject
from gampy.engine.components.gamecomponent import GameComponent
from gampy.engine.components.meshrenderer import MeshRenderer
from gampy.engine.components.camera import Camera
from gampy.engine.tkinter.window import Window
from gampy.engine.components.inputs import FreeLook, FreeMove
import gampy.engine.components.lights as light_components
import math
import gampy.engine.core.time as timing
import OpenGL.GL as gl

timer = timing.Timing()


class TestGame(Game):

    # @timer
    def init(self):
        # temp_target = Texture((Window.width, Window.height, None), gl.GL_TEXTURE_2D, gl.GL_NEAREST, None,
        #                            None, False, gl.GL_COLOR_ATTACHMENT0)
        # mesh = Mesh('plane.obj')
        # material = Material(temp_target, 1., 8.)
        # view_plane_obj = GameObject().add_component(MeshRenderer(mesh, material))
        # view_plane_obj.transform.scale
        # self.transform = Transform()
        # self.transform.scale = 0.9
        # self.transform.rotate(Vector3(1, 0, 0), math.radians(90))
        # self.transform.rotate(Vector3(0, 0, 1), math.radians(180))



        camera = GameObject().add_component(Camera()).add_component(FreeMove(10)).add_component(FreeLook(0.5))
        camera.transform.position = (-1, .5, -1)
        self.add_object(camera)

        mesh = test_mesh('plane', 12, 12)
        material = Material(Texture('bricks.jpg'), normal_map=Texture('bricks_normal.jpg'),
                            disp_map=Texture('bricks_disp.png'), disp_map_scale=0.02, disp_map_offset=-0.5)
        mesh2 = test_mesh('plane', 2, 2)
        mesh2 = test_mesh('plane', 1, 1)
        material2 = Material(Texture('bricks2.jpg'), normal_map=Texture('bricks2_normal.jpg'),
                             disp_map=Texture('bricks2_disp.jpg'), disp_map_scale=0.02, disp_map_offset=1.)

        mesh_renderer = MeshRenderer(mesh, material)

        plane_object = GameObject()
        plane_object.add_component(mesh_renderer)
        plane_object.add_component(ChangeTexComponent(Texture('bricks_normal.jpg'), Texture('bricks_normal_i.jpg'),
                                                     Input.KEY_M))
        plane_object.transform.position = (0, -.5, 0)
        plane_object.transform.scale = (12, 12, 12)

        directional_light_object = GameObject()
        directional_light = light_components.DirectionalLight(Vector3(1, 1, 1), 0.3)
        directional_light_object.add_component(directional_light)
        directional_light.transform.rotation = Quaternion(Vector3(1, 0, 0), math.radians(-45))

        point_light_object = GameObject()
        point_light = light_components.PointLight(Vector3(0., 1., 0.), 0.4, (0., 0., 0.8))
        point_light_object.add_component(point_light)
        point_light.transform.position = (0, 2, 0)

        spot_light_object = GameObject()
        spot_light = light_components.SpotLight(Vector3(1., 1., 0.), 0.4, (0., 0., 0.5), 0.3)
        spot_light_object.add_component(spot_light)
        spot_light_object.transform.position = (5, 3, 5)
        spot_light_object.transform.rotation = Quaternion(Vector3(0, 1, 0), math.radians(90))
        spot_light_object.transform.rotation += Quaternion(Vector3(1, 0, 0), math.radians(30))

        self.add_object(plane_object)
        self.add_object(directional_light_object)
        self.add_object(point_light_object)
        self.add_object(spot_light_object)

        test_mesh_1 = GameObject().add_component(MeshRenderer(mesh2, material2))
        test_mesh_1.add_component(ChangeTexComponent(Texture('bricks2_normal.jpg'), Texture('bricks2_normal_i.jpg'),
                                                     Input.KEY_N))
        test_mesh_2 = GameObject().add_component(MeshRenderer(mesh2, material2))

        test_mesh_1.transform.position = (0, 0.25, 0)
        test_mesh_1.transform.rotation = Quaternion(Vector3(0, 1, 0), math.radians(45))
        test_mesh_2.transform.position = (0, 0.25, 7)
        test_mesh_2.transform.scale = (2, 2, 2)

        test_mesh_1.add_child(test_mesh_2)
        # test_mesh_2.add_child(GameObject().add_component(Camera()))

        self.add_object(test_mesh_1)

        # mesh3 = GameObject().add_component(LookAtComponent()).add_component(MeshRenderer(Mesh('cube.obj'), material))
        # mesh3.transform.position = 0, 5, 0
        # self.add_object(mesh3)

        # temp_mesh = Mesh('monkey.obj')
        # temp_material = Material(Texture('tegre_skin.jpg'), 2., 32.) # (Texture('test.png'), Vector3(1, 1, 1))
        # test_mesh_3 = GameObject().add_component(MeshRenderer(temp_mesh, temp_material))
        # self.add_object(test_mesh_3)
        # test_mesh_3.transform.position = (5, 5, 5)
        # test_mesh_3.transform.rotation = Quaternion(Vector3(0, 1, 0), math.radians(-90))

        # self.add_object(GameObject().add_component(MeshRenderer(Mesh('suzanne.obj'), material)))

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


class LookAtComponent(GameComponent):

    def __init__(self):
        super().__init__()
        self._render_engine = None

    def update(self, dt):
        if self._render_engine is not None:
            new_rotation = self.transform.look_at_direction(self._render_engine.main_camera.transform.transformed_position(), Vector3(0, 1, 0))

            # self.transform.rotation = self.transform.rotation.nlerp(new_rotation, dt * 5, True)
            self.transform.rotation = self.transform.rotation.slerp(new_rotation, dt * 5, True)

    def render(self, shader, render_engine, camera_view, camera_pos):
        self._render_engine = render_engine


class ChangeTexComponent(GameComponent):

    def __init__(self, normal_map, inv_normal_map, key=Input.KEY_N):
        super().__init__()
        self._render_engine = None
        self._mesh_renderer = None
        self._key = key
        self._normal_map = normal_map
        self._i_normal_map = inv_normal_map
        self._normal = True

    def get_mesh_renderer(self):
        if self._mesh_renderer:
            return self._mesh_renderer

        parent = self.parent
        for component in parent.components:
            if isinstance(component, MeshRenderer):
                self._mesh_renderer = component

    def input(self, dt):
        mesh_renderer = self.get_mesh_renderer()
        self._normal = not self._normal
        if Input.get_key(self._key):
            mesh_renderer.material.add_mapped_value('normalMap', self._normal_map if self._normal else self._i_normal_map)


# Temp function
def test_mesh(type, *args):
    from gampy.engine.render.meshes import Vertex
    from gampy.engine.core.vectors import Vector2

    def create_plane(depth, width):
        vertices = [
            Vertex(Vector3(-width, 0, -depth), Vector2(0, 0)),
            Vertex(Vector3(-width, 0, depth), Vector2(0, 1)),
            Vertex(Vector3(width, 0, -depth), Vector2(1, 0)),
            Vertex(Vector3(width, 0, depth), Vector2(1, 1))
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

    mesh = Mesh(vertices, indices, True, True)

    return mesh
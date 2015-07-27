__author__ = 'michiel'

import math

from gampy.engine.render.material import Material
from gampy.engine.render.texture import Texture
from gampy.engine.core.math3d import Vector3, Quaternion, Matrix4
from gampy.engine.render.meshes import Mesh, Vertex
from gampy.engine.core.game import Game
from gampy.engine.tkinter.input import Input
from gampy.engine.core.entity import Entity
from gampy.engine.components.entitycomponent import EntityComponent
from gampy.engine.components.meshrenderer import MeshRenderer
from gampy.engine.components.camera import Camera
from gampy.engine.tkinter.window import Window
from gampy.engine.components.inputs import FreeLook, FreeMove
import gampy.engine.components.lights as light_components
import gampy.engine.components.physics as physics_components
import gampy.engine.core.time as timing
import gampy.engine.physics.bounding as bounding
import gampy.engine.physics.physicsengine as physicsengine
from gampy.engine.physics.physicsengine import PhysicsObject, PhysicsEngine, BoundingSphere


timer = timing.Timing()


class TestGame(Game):

    # @timer
    def init(self):
        bounding.test()
        physicsengine.test()
        material = Material(Texture('bricks.jpg'), 0.0, 0, normal_map=Texture('bricks_normal.jpg'),
                            disp_map=Texture('bricks_disp.png'), disp_map_scale=0.03, disp_map_offset=-.5)
        material2 = Material(Texture('bricks2.jpg'), 0.0, 0, normal_map=Texture('bricks2_normal.jpg'),
                             disp_map=Texture('bricks2_disp.jpg'), disp_map_scale=0.04, disp_map_offset=-1)

        custom_mesh = Mesh([
            Vertex([1.0, -1.0, 0.0], [1.0, 1.0]),
            Vertex([1.0, 1.0, 0.0], [1.0, 0.0]),
            Vertex([-1.0, -1.0, 0.0], [0.0, 1.0]),
            Vertex([-1.0, 1.0, 0.0], [1.0, 1.0]),
        ], [0, 1, 2, 2, 1, 3], True, True)

        # self.add_to_scene(Entity(Vector3(0, -1, 5), scale=32.)
        #       .add_component(MeshRenderer(Mesh('terrain02.obj'), material)))
        #
        # self.add_to_scene(Entity(Vector3(7, 0, 7)).add_component(light_components.PointLight(Vector3(0, 1, 0), 0.4,
        #                                                                                      (0., 0., 1.))))
        #
        # self.add_to_scene(Entity(Vector3(20, -11, 5), Quaternion(Vector3(1, 0, 0), math.radians(-60)) *
        #                          Quaternion(Vector3(0, 1, 0), math.radians(90)))
        #       .add_component(light_components.SpotLight(Vector3(0, 1, 1), 0.4, (0., 0., 0.02), math.radians(91.1))))

        self.add_to_scene(Entity(rotation=Quaternion(Vector3(1, 0, 0), math.radians(-45)))
              .add_component(light_components.DirectionalLight(Vector3(1, 1, 1), 0.4)))

        self.add_to_scene(Entity(Vector3(0, 2, 0), Quaternion(Vector3(0, 1, 0), 0.4))
              .add_component(MeshRenderer(test_mesh('plane', 4, 4), material2))
              .add_child(Entity(Vector3(0, 0, 25))
                     .add_component(MeshRenderer(test_mesh('plane', 4, 4), material2))
                     .add_child(Entity(Vector3(0, 1, 0), Quaternion(Vector3(0, 1, 0), math.radians(180)))
                            .add_component(Camera(Matrix4().init_perspective(math.radians(70.),
                                                                             Window.aspect, 0.1,
                                                                             1000.)))
                            .add_component(FreeLook(0.5)).add_component(FreeMove(10.)))))

        # self.add_to_scene(Entity(Vector3(24, -12, 5), Quaternion(Vector3(0, 1, 0), math.radians(30.)))
        #       .add_component(MeshRenderer(Mesh('cube.obj'), material2)))
        #
        # self.add_to_scene(Entity(Vector3(24, -12, 5), Quaternion(Vector3(0, 1, 0), math.radians(30.)))
        #       .add_component(MeshRenderer(custom_mesh, material2)))

        physics_engine = PhysicsEngine()

        physics_engine.add_object(PhysicsObject(BoundingSphere([-10, 4, 10], 1.), [1, 0, 0]))
        physics_engine.add_object(PhysicsObject(BoundingSphere([10, 4, 9], 1.), [-1, 0, 0]))

        physics_engine_component = physics_components.PhysicsEngineComponent(physics_engine)
        for index in range(physics_engine.num_objects):
            self.add_to_scene(Entity()
                .add_component(physics_components.PhysicsObjectComponent(physics_engine.get_object(index)))
                .add_component(MeshRenderer(Mesh('sphere.obj', calc_norm=True, calc_tangent=True), material)))

        self.add_to_scene(Entity().add_component(physics_engine_component))


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


class LookAtComponent(EntityComponent):

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


class ChangeTexComponent(EntityComponent):

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
            mesh_renderer.material.set_mapped_value('normalMap', self._normal_map if self._normal else self._i_normal_map)


# Temp function
def test_mesh(type, *args):
    from gampy.engine.render.meshes import Vertex
    from gampy.engine.core.math3d import Vector2

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
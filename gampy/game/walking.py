import math
import random

from gampy.engine.components.camera import Camera
from gampy.engine.components.inputs import FreeLook, FreeMove
from gampy.engine.components.meshrenderer import MeshRenderer
from gampy.engine.components.physics import PhysicsObjectComponent
from gampy.engine.core.coreengine import CoreEngine
from gampy.engine.core.entity import Entity
from gampy.engine.core.game import Game
from gampy.engine.core.math3d import Vector2, Vector3, Quaternion
from gampy.engine.physics.physicsengine import (PhysicsObject, PhysicsEngine,
                                                BoundingSphere, AABB)
from gampy.engine.render.material import Material
from gampy.engine.render.meshes import Mesh, Vertex
from gampy.engine.render.texture import Texture
from gampy.engine.tkinter.window import Window
import gampy.engine.components.lights as light_components
import gampy.engine.components.physics as physics_components


__author__ = 'michiel'


def main():
    engine = CoreEngine(800, 600, 60, WalkingGame())
    engine.create_window('Super Duper Walking Game')
    engine.start()


class WalkingGame(Game):

    def init(self):
        material = Material(Texture('bricks.jpg'), 0.0, 0,
                            normal_map=Texture('bricks_normal.jpg'),
                            disp_map=Texture('bricks_disp.png'),
                            disp_map_scale=0.03, disp_map_offset=-.5)
        material2 = Material(Texture('bricks2.jpg'), 0.0, 0,
                             normal_map=Texture('bricks2_normal.jpg'),
                             disp_map=Texture('bricks2_disp.jpg'),
                             disp_map_scale=0.04, disp_map_offset=-1)

        ground = Mesh([
            Vertex(Vector3(-20, 0, -20), Vector2(0, 0)),
            Vertex(Vector3(-20, 0, 20), Vector2(0, 10)),
            Vertex(Vector3(20, 0, -20), Vector2(10, 0)),
            Vertex(Vector3(20, 0, 20), Vector2(10, 10))
        ], [0, 1, 2, 2, 1, 3], True, True)

        person = Mesh([
            Vertex(Vector3(-0.5, -0.5, -0.5)),
            Vertex(Vector3(0.5, -0.5, -0.5)),
            Vertex(Vector3(0.5, 0.5, -0.5)),
            Vertex(Vector3(-0.5, 0.5, -0.5)),
            Vertex(Vector3(0.5, 0.5, 0.5)),
            Vertex(Vector3(-0.5, 0.5, 0.5)),
            Vertex(Vector3(-0.5, -0.5, 0.5)),
            Vertex(Vector3(0.5, -0.5, 0.5)),
        ], [0, 2, 1, 3, 2, 0,
            1, 4, 7, 2, 4, 1,
            7, 5, 6, 4, 5, 7,
            6, 3, 0, 5, 3, 6,
            6, 1, 7, 0, 1, 6,
            3, 4, 2, 5, 4, 3], True, True)

        self.add_to_scene(Entity().add_component(MeshRenderer(ground,
                                                              material2)))
        self.add_to_scene(
            Entity(rotation=Quaternion(Vector3(1, 0, 0), math.radians(-45)) *
                   Quaternion(Vector3(0, 0, 1), math.radians(-65))
                   ).add_component(
                       light_components.DirectionalLight(
                           Vector3(1, 0.7, 0), 0.5)))

        camera = Camera(math.radians(70), Window.width / Window.height,
                        0.1, 100.)
        camera_obj = Entity(Vector3(0, 2, -20)).add_component(camera)
        camera_obj.add_component(FreeMove(10.)).add_component(FreeLook(.5))
        camera_obj.transform.look_at(Vector3(0, 0, 0), Vector3(0, 1, 0))
        self.add_to_scene(camera_obj)

        physics_engine = PhysicsEngine()
        physics_engine_component = physics_components.PhysicsEngineComponent(physics_engine)
        self.add_to_scene(Entity().add_component(physics_engine_component))

        for i in range(-2, 2):
            for j in range(-1, 2):
                # physics_obj = PhysicsObject(AABB((Vector3(-0.5 + i, -0.5, -0.5 + j), Vector3(0.5 + i, 0.5, 0.5 + j))), [0, 0, 0])
                physics_obj = PhysicsObject(BoundingSphere([i * 5, 0.5, j * 5], 0.5), [0, 0, 0])
                physics_engine.add_object(physics_obj)
                entity = Entity().add_component(MeshRenderer(person, material)).add_component(RandomMove(physics_obj))
                self.add_to_scene(entity)
                del physics_obj
                del entity


class RandomMove(PhysicsObjectComponent):

    def update(self, dt):
        self._physics_object.velocity.x += (random.random() * 2 - 1)
        self._physics_object.velocity.z += (random.random() * 2 - 1)
        if self._physics_object.velocity.max_value() > 100:
            self._physics_object.velocity = Vector3(0, 0, 0)
        super().update(dt)

        if abs(self.transform.position.x) > 20:
            self._physics_object.velocity.x = -self._physics_object.velocity.x
        if abs(self.transform.position.z) > 20:
            self._physics_object.velocity.z = -self._physics_object.velocity.z


if __name__ == '__main__':
    main()

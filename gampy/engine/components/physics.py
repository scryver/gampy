__author__ = 'michiel'

from gampy.engine.physics.physicsengine import PhysicsEngine, PhysicsObject
from gampy.engine.components.entitycomponent import EntityComponent

class PhysicsEngineComponent(EntityComponent):

    def __init__(self, physics_engine):
        super().__init__()
        self._physics_engine = physics_engine

    @property
    def physics_engine(self):
        return self._physics_engine

    def update(self, dt):
        self._physics_engine.simulate(dt)
        self._physics_engine.handle_collisions()


class PhysicsObjectComponent(EntityComponent):

    def __init__(self, physics_object):
        super().__init__()
        self._physics_object = physics_object

    def update(self, dt):
        self.transform.position = self._physics_object.position

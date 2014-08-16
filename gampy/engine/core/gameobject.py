__author__ = 'michiel'

from gampy.engine.core.eventinterface import EventInterface
from gampy.engine.core.gamecomponent import GameComponent
from gampy.engine.core.transform import Transform
from gampy.engine.render.shader import Shader

class GameObject(EventInterface):

    def __init__(self):
        self.children = []
        self.components = []
        self.transform = Transform()

    def add_child(self, child):
        if isinstance(child, GameObject):
            self.children.append(child)
        else:
            raise AttributeError('Child is not a GameObject')

    def add_component(self, component):
        if isinstance(component, GameComponent):
            self.components.append(component)
        else:
            raise AttributeError('Component is not a GameComponent')

    def input(self, dt):
        [component.input(dt, self.transform) for component in self.components]
        [child.input(dt) for child in self.children]

    def update(self, dt):
        [component.update(dt, self.transform) for component in self.components]
        [child.update(dt) for child in self.children]

    def render(self, shader):
        if not isinstance(shader, Shader):
            raise AttributeError('Invalid shader supplied')
        [component.render(self.transform, shader) for component in self.components]
        [child.render(shader) for child in self.children]
__author__ = 'michiel'

from gampy.engine.core.eventinterface import EventInterface
from gampy.engine.core.transform import Transform

class GameObject(EventInterface):

    def __init__(self):
        self.children = []
        self.components = []
        self.transform = Transform()

    def add_child(self, child):
        self.children.append(child)
        child.transform.parent = self.transform

    def add_component(self, component):
        self.components.append(component)
        component.parent = self
        return self

    def input(self, dt):
        self.transform.update()

        [component.input(dt) for component in self.components]
        [child.input(dt) for child in self.children]

    def update(self, dt):
        [component.update(dt) for component in self.components]
        [child.update(dt) for child in self.children]

    def render(self, shader):
        [component.render(shader) for component in self.components]
        [child.render(shader) for child in self.children]

    def add_to_render_engine(self, rendering_engine):
        [component.add_to_render_engine(rendering_engine) for component in self.components]
        [child.add_to_render_engine(rendering_engine) for child in self.children]
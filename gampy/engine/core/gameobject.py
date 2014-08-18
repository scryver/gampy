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

    def add_component(self, component):
        self.components.append(component)

    def input(self, dt):
        [component.input(dt, self.transform) for component in self.components]
        [child.input(dt) for child in self.children]

    def update(self, dt):
        [component.update(dt, self.transform) for component in self.components]
        [child.update(dt) for child in self.children]

    def render(self, shader):
        [component.render(self.transform, shader) for component in self.components]
        [child.render(shader) for child in self.children]

    def add_to_render_engine(self, rendering_engine):
        [component.add_to_render_engine(rendering_engine) for component in self.components]
        [child.add_to_render_engine(rendering_engine) for child in self.children]
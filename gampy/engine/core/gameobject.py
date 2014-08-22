__author__ = 'michiel'

from gampy.engine.core.eventinterface import EventInterface
from gampy.engine.core.transform import Transform


class GameObject(EventInterface):

    def __init__(self):
        self.children = []
        self.components = []
        self.transform = Transform()
        self._engine = None

    def get_engine(self):
        return self._engine

    def set_engine(self, engine):
        if self._engine != engine:
            self._engine = engine
            [component.add_to_engine(engine) for component in self.components]
            [child.set_engine(engine) for child in self.children]

    def add_child(self, child):
        self.children.append(child)
        child.set_engine(self._engine)
        child.transform.parent = self.transform

    def add_component(self, component):
        self.components.append(component)
        component.parent = self
        return self

    def all_attached(self, result=None):
        if result is None:
            result = []
        [child.all_attached(result) for child in self.children]
        result.append(self)
        return result

    def input(self, dt):
        self.transform.update()
        [component.input(dt) for component in self.components]

    def update(self, dt):
        [component.update(dt) for component in self.components]

    def render(self, shader, render_engine):
        [component.render(shader, render_engine) for component in self.components]

    def input_all(self, dt):
        self.input(dt)
        [child.input(dt) for child in self.children]

    def update_all(self, dt):
        self.update(dt)
        [child.update(dt) for child in self.children]

    def render_all(self, shader, render_engine):
        self.render(shader, render_engine)
        [child.render(shader, render_engine) for child in self.children]
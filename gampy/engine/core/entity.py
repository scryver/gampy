__author__ = 'michiel'

from gampy.engine.core.eventinterface import EventInterface
from gampy.engine.core.transform import Transform


class Entity(EventInterface):

    def __init__(self, position=None, rotation=None, scale=None):
        self.children = []
        self.components = []
        self.transform = Transform(position, rotation, scale)
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
        return self

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

    def all_generator(self):
        yield self
        for child in self.children:
            for c in child.all_generator():
                yield c

    def input(self, dt):
        self.transform.clear_has_changed()
        self.transform.update()
        for component in self.components:
            component.input(dt)
        # [component.input(dt) for component in self.components]

    def update(self, dt):
        for component in self.components:
            component.update(dt)
        # [component.update(dt) for component in self.components]

    def render(self, shader, render_engine, camera_view, camera_pos):
        for component in self.components:
            component.render(shader, render_engine, camera_view, camera_pos)

    def input_all(self, dt):
        for e in self.all_generator():
            e.input(dt)
        # self.input(dt)
        # [child.input_all(dt) for child in self.children]

    def update_all(self, dt):
        for e in self.all_generator():
            e.update(dt)
        # self.update(dt)
        # [child.update_all(dt) for child in self.children]

    def render_all(self, shader, render_engine, camera_view, camera_pos):
        for e in self.all_generator():
            e.render(shader, render_engine, camera_view, camera_pos)
        # self.render(shader, render_engine, camera_view, camera_pos)
        # [child.render_all(shader, render_engine, camera_view, camera_pos) for child in self.children]

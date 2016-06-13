__author__ = 'michiel'

from gampy.engine.core.eventinterface import EventInterface
from gampy.engine.core.transform import Transform

import gampy.engine.core.time as timing

timer = timing.Timing()


class Entity(EventInterface):

    _is_printed = False

    @timer
    def __init__(self, position=None, rotation=None, scale=None):
        self.children = []
        self.components = []
        self.transform = Transform(position, rotation, scale)
        self._engine = None

    # @timer
    def get_engine(self):
        return self._engine

    # @timer
    def set_engine(self, engine):
        if self._engine != engine:
            self._engine = engine
            [component.add_to_engine(engine) for component in self.components]
            [child.set_engine(engine) for child in self.children]

    # @timer
    def add_child(self, child):
        self.children.append(child)
        child.set_engine(self._engine)
        child.transform.parent = self.transform
        return self

    # @timer
    def add_component(self, component):
        self.components.append(component)
        component.parent = self
        return self

    # @timer
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

    # @timer
    def input(self, dt):
        self.transform.clear_has_changed()
        self.transform.update()
        [component.input(dt) for component in self.components]

    # @timer
    def update(self, dt):
        [component.update(dt) for component in self.components]

    @timer
    def render(self, shader, render_engine, camera_view, camera_pos):
        for component in self.components:
            component.render(shader, render_engine, camera_view, camera_pos)

    # @timer
    def input_all(self, dt):
        self.input(dt)
        [child.input_all(dt) for child in self.children]

    # @timer
    def update_all(self, dt):
        self.update(dt)
        [child.update_all(dt) for child in self.children]

    @timer
    def render_all(self, shader, render_engine, camera_view, camera_pos):
        self.render(shader, render_engine, camera_view, camera_pos)
        [child.render_all(shader, render_engine, camera_view, camera_pos) for child in self.children]

    def __del__(self):
        if not Entity._is_printed:
            Entity._is_printed = True
            print('========ENTITY=======================================================================',
                  timer,
                  '=====================================================================================', sep='\n')

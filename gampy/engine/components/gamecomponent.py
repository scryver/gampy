__author__ = 'michiel'

from gampy.engine.core.eventinterface import EventInterface


class GameComponent(EventInterface):

    def __init__(self):
        self.parent = None

    def input(self, dt):
        pass

    def update(self, dt):
        pass

    def render(self, shader, render_engine, camera_view, camera_pos):
        pass

    @property
    def transform(self):
        return self.parent.transform

    def add_to_engine(self, engine):
        pass
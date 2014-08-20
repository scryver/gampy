__author__ = 'michiel'

from gampy.engine.core.eventinterface import EventInterface
from gampy.engine.core.transform import Transform
import gampy.engine.core.util as core_util

class GameComponent(EventInterface):

    def __init__(self):
        self.parent = None

    def input(self, dt):
        pass

    def update(self, dt):
        pass

    def render(self, shader, render_engine):
        pass

    @property
    def transform(self):
        return self.parent.transform

    def add_to_render_engine(self, render_engine):
        pass
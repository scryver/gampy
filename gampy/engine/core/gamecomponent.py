__author__ = 'michiel'

from gampy.engine.core.eventinterface import EventInterface

class GameComponent(EventInterface):

    def init(self):
        pass

    def input(self):
        pass

    def update(self):
        pass

    def render(self):
        pass
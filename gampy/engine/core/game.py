__author__ = 'michiel'

from gampy.engine.core.eventinterface import EventInterface

class Game(EventInterface):

    def init(self):
        raise NotImplemented

    def input(self):
        raise NotImplemented

    def update(self):
        raise NotImplemented

    def render(self):
        raise NotImplemented
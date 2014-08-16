__author__ = 'michiel'

from gampy.engine.core.eventinterface import EventInterface
from gampy.engine.core.gameobject import GameObject

class Game(EventInterface):

    def init(self):
        raise NotImplemented

    def input(self):
        self.root_object.input()

    def update(self):
        self.root_object.update()

    @property
    def root_object(self):
        try:
            root = self._root
        except:
            root = GameObject()
            self._root = root

        return root
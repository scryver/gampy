__author__ = 'michiel'

from gampy.engine.core.eventinterface import EventInterface
from gampy.engine.core.gameobject import GameObject

class Game(EventInterface):

    def init(self):
        raise NotImplemented

    def input(self, dt):
        self.root_object.input(dt)

    def update(self, dt):
        self.root_object.update(dt)

    @property
    def root_object(self):
        try:
            root = self._root
        except:
            root = GameObject()
            self._root = root

        return root

    def destroy(self):
        pass
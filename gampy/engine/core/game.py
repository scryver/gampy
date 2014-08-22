__author__ = 'michiel'

from gampy.engine.core.eventinterface import EventInterface
from gampy.engine.core.gameobject import GameObject

class Game(EventInterface):

    def init(self):
        self._root = self._root_object

    def input(self, dt):
        self._root_object.input_all(dt)

    def update(self, dt):
        self._root_object.update_all(dt)

    def render(self, render_engine):
        render_engine.render_all(self._root_object)

    def add_object(self, game_object):
        self._root_object.add_child(game_object)

    def engine(self, engine):
        self._root_object.set_engine(engine)

    @property
    def _root_object(self):
        try:
            root = self._root
        except:
            root = GameObject()
            self._root = root

        return root

    def destroy(self):
        pass
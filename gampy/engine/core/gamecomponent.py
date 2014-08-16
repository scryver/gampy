__author__ = 'michiel'

from gampy.engine.core.eventinterface import EventInterface
from gampy.engine.core.transform import Transform

class GameComponent(EventInterface):

    def input(self, dt, transform):
        if not isinstance(transform, Transform):
            raise AttributeError('Transformation is not of type Transform')

        return

    def update(self, dt, transform):
        if not isinstance(transform, Transform):
            raise AttributeError('Transformation is not of type Transform')

        return

    def render(self, transform, shader):
        if not isinstance(transform, Transform):
            raise AttributeError('Transformation is not of type Transform')

        return
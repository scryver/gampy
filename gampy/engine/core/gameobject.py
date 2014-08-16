__author__ = 'michiel'

from gampy.engine.core.eventinterface import EventInterface
from gampy.engine.core.gamecomponent import GameComponent
from gampy.engine.core.transform import Transform

class GameObject(EventInterface):

    def __init__(self):
        self.children = []
        self.components = []
        self.transform = Transform()

    def add_child(self, child):
        if isinstance(child, GameObject):
            self.children.append(child)
        else:
            raise AttributeError('Child is not a GameObject')

    def add_component(self, component):
        if isinstance(component, GameComponent):
            self.components.append(component)
        else:
            raise AttributeError('Component is not a GameComponent')

    def input(self):
        [component.input() for component in self.components]
        [child.input() for child in self.children]

    def update(self):
        [component.update() for component in self.components]
        [child.update() for child in self.children]

    def render(self):
        [component.render() for component in self.components]
        [child.render() for child in self.children]
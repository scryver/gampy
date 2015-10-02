__author__ = 'michiel'

from gampy.engine.maincomponent import MainComponent
from gampy.engine.game import Game

W, H = 640, 480

m = MainComponent(W, H, "Testing")


def updater(self, dt):
    self.tmp += dt
    self.mesh.update(dt)

setattr(Game, 'update', updater)
g = Game(W, H)
g.transform.set_translation(0, 0, 10)
g.transform.set_rotation(45, 0, 0)
g.transform.set_scale(10, 10, 1)

m.game = g

try:
    m.start()
except KeyboardInterrupt:
    pass

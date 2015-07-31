__author__ = 'michiel'

from gampy.engine.maincomponent import MainComponent

m = MainComponent(640, 480, "Testing")
try:
    m.start()
except KeyboardInterrupt:
    pass

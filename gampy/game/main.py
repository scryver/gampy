__author__ = 'michiel'

from gampy.engine.core.coreengine import CoreEngine
from gampy.game.testgame import TestGame

class Main:

    @classmethod
    def main(cls, *args, **kwargs):
        engine = CoreEngine(800, 600, 300, TestGame())
        engine.create_window('Super Duper 3D Game Engine')
        engine.start()


if __name__ == '__main__':
    Main.main()
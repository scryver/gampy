__author__ = 'michiel'

from gampy.engine.core.coreengine import CoreEngine
from gampy.game.testgame import TestGame
from gampy.engine.core.math3d import Matrix4
from gampy.engine.core.transform import Transform

class Main:

    @classmethod
    def main(cls, *args, **kwargs):
        engine = CoreEngine(800, 600, 60, TestGame())
        engine.create_window('Super Duper 3D Game Engine')
        engine.start()
        Matrix4.print_timing()
        Transform.print_timing()


if __name__ == '__main__':
    # import profile
    # main = 'Main.main()'
    # profile.run(main)
    Main.main()

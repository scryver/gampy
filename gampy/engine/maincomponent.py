__author__ = 'michiel'

import gampy.engine.render.window as window
import gampy.engine.events.time as time
import gampy.engine.game as game
import gampy.engine.input.input as game_input
import gampy.engine.render.util as render_util
import os
import sdl2
import ctypes
from gampy.engine.events.time import Timing

timings = Timing()

class MainComponent:

    WIDTH = 800
    HEIGHT = 600
    TITLE = 'Super Duper 3D Game Engine'
    FRAME_CAP = 5000.

    @timings
    def __init__(self, width=0, height=0, title=None):
        if width == 0:
            width = MainComponent.WIDTH
        if height == 0:
            height = MainComponent.HEIGHT
        if title == None:
            title = MainComponent.TITLE

        self.window = window.Window(width, height, title)
        # Create a gl context first (self.window)
        print('%s' % render_util.get_open_gl_version())
        render_util.init_graphics()

        self.is_running = False
        self.game = game.Game(MainComponent.WIDTH, MainComponent.HEIGHT)
        self.time = time.Time()

    @timings
    def start(self):
        if self.is_running:
            return

        self._run()

    @timings
    def stop(self):
        if not self.is_running:
            return

        self.is_running = False
        self.input.destroy()

    @timings
    def _run(self):
        self.is_running = True
        self.event = sdl2.SDL_Event()
        self.input = game_input.Input(self.event)

        frames = 0
        frame_counter = 0.

        frame_time = 1.0 / MainComponent.FRAME_CAP

        last_time = time.Time.get_time()
        unprocessed_time = 0.

        while self.is_running:
            while sdl2.SDL_PollEvent(ctypes.byref(self.event)) != 0:
                if self.event.type == sdl2.SDL_QUIT or \
                  (self.event.type == sdl2.SDL_KEYDOWN and self.event.key.keysym.scancode == sdl2.SDL_SCANCODE_ESCAPE):
                    self.is_running = False

            render = False

            start_time = time.Time.get_time()
            passed_time = start_time - last_time
            last_time = start_time

            unprocessed_time += passed_time
            frame_counter += passed_time

            while unprocessed_time > frame_time:
                render = True
                unprocessed_time -= frame_time

                if not self.window.is_display_open:
                    self.stop()

                self.time.delta = frame_time

                self.game.input(self.input)
                self.input.update()

                self.game.update(self.time.delta)

                if frame_counter >= 1.0:
                    # Frame Rate
                    print('Frame rate: ', frames)
                    frames = 0
                    frame_counter = 0.

            if render:
                self._render()
                frames += 1
            else:
                time.Time.sleep()

        self._cleanUp()

    @timings
    def _render(self):
        render_util.clear_screen()
        self.game.render()
        self.window.render()

    @timings
    def _cleanUp(self):
        self.game.destroy()
        self.window.dispose()
        sdl2.SDL_Quit()

    @staticmethod
    def main(*args, **kwargs):
        game = MainComponent()
        game.start()

    def __del__(self):
        print(timings)


if __name__ == '__main__':

    MainComponent.main()

    # try:
    #     # HACK FOR REPEATING KEYS
    #     os.system('xset r off')
    #     MainComponent.main()
    #     # HACK FOR REPEATING KEYS
    #     os.system('xset r on')
    # except Exception as err:
    #     print(err.with_traceback(None))
    #     # HACK FOR REPEATING KEYS
    #     os.system('xset r on')
    #     exit(1)
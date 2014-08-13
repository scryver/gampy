__author__ = 'michiel'

import gampy.engine.render.window as window
import gampy.engine.events.time as time
import gampy.engine.game as game
import gampy.engine.input.input as game_input
import gampy.engine.render.util as render_util

class MainComponent:

    WIDTH = 800
    HEIGHT = 600
    TITLE = 'Super Duper 3D Game Engine'
    FRAME_CAP = 5000.

    def __init__(self, width=0, height=0, title=None):
        render_util.init_graphics()

        if width == 0:
            width = MainComponent.WIDTH
        if height == 0:
            height = MainComponent.HEIGHT
        if title == None:
            title = MainComponent.TITLE

        self.window = window.Window(width, height, title)
        self.is_running = False
        self.game = game.Game()
        self.input = game_input.Input()
        self.time = time.Time()

    def start(self):
        if self.is_running:
            return

        self._run()

    def stop(self):
        if not self.is_running:
            return

        self.is_running = False
        self.input.destroy()

    def _run(self):
        self.is_running = True
        self.input.bind_window(self.window)

        frames = 0
        frame_counter = 0.

        frame_time = 1.0 / MainComponent.FRAME_CAP

        last_time = time.Time.get_time()
        unprocessed_time = 0.;

        while self.is_running:
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

                self.game.update()

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

    def _render(self):
        render_util.clear_screen()
        self.game.render()
        self.window.render()

    def _cleanUp(self):
        self.window.dispose()
        self.game.destroy()

    @staticmethod
    def main(*args, **kwargs):
        game = MainComponent()
        game.start()


if __name__ == '__main__':
    MainComponent.main()
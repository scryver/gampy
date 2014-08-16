__author__ = 'michiel'

from gampy.engine.render.window import Window
from gampy.engine.core.time import Time
from gampy.engine.core.input import Input
import gampy.engine.render.util as render_util


class CoreEngine:

    def __init__(self, width, height, fps, game):
        # self.game = game.Game()

        self.is_running = False
        self.game = game
        self.frame_rater = 0.
        self.frame_rater_count = 0.
        self.width = width
        self.height = height
        self.frame_time = 1 / fps

    def start(self):
        if self.is_running:
            return

        self._run()

    def stop(self):
        if not self.is_running:
            return

        self.is_running = False

    def _input_updater(self, delta):
        time_delta = delta / 1000
        self.game.input(time_delta, Window.display)
        Input.update(time_delta)
        Window.root.after(delta, self._input_updater, delta)

    def _run(self):
        self.is_running = True

        frames = 0
        frame_counter = 0.

        self.game.init()

        Input.bind_window(Window)
        self._input_updater(20)

        last_time = Time.get_time()
        unprocessed_time = 0.

        while self.is_running:
            render = False

            start_time = Time.get_time()
            passed_time = start_time - last_time
            last_time = start_time

            unprocessed_time += passed_time
            frame_counter += passed_time
            self.frame_rater_count += passed_time

            while unprocessed_time > self.frame_time:
                render = True
                unprocessed_time -= self.frame_time

                if not Window.is_display_open:
                    self.stop()

                Time.delta = self.frame_time

                self.game.update(Time.delta)

                Window.update(Time.delta)

                if frame_counter >= 1.0:
                    # Frame Rate
                    print('Frame rate: ', frames)
                    frames = 0
                    frame_counter = 0.

            if render:
                self._render()
                frames += 1
                self.frame_rater += 1
            else:
                Time.sleep()

        self._cleanUp()

    def _render(self):
        render_util.clear_screen()
        self.game.render()
        Window.render()

    def _cleanUp(self):
        Input.destroy()
        self.game.destroy()
        Window.dispose()

    def init_rendering_engine(self):
        print('%s' % render_util.get_open_gl_version())
        render_util.init_graphics()

    def create_window(self, title):
        Window.create(self.width, self.height, title)

    def __del__(self):
        print('Average FPS: {avg:7.2f} | Total frames rendered: {tot:.0f}'.format(avg=self.frame_rater / self.frame_rater_count,
                                                                                  tot=self.frame_rater))
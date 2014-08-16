__author__ = 'michiel'

from gampy.engine.render.window import Window
from gampy.engine.core.time import Time
from gampy.engine.core.input import Input
from gampy.engine.core.renderingengine import RenderingEngine
import _thread


class CoreEngine:

    def __init__(self, width, height, fps, game):
        # self.game = game.Game()

        self.is_running = False
        self.game = game
        self.width = width
        self.height = height
        self.frame_time = 1 / fps
        self.rendering_engine = None

        self.frame_rater = 0.
        self.frame_rater_count = 0.000001

    def start(self):
        if self.is_running:
            return

        self._run()

    def stop(self):
        if not self.is_running:
            return

        self.is_running = False

    def _run(self):
        self.is_running = True

        frames = 0
        frame_counter = 0.

        self.game.init()
        Input.init()

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

                self.game.input()
                self.rendering_engine.input()
                Input.update()
                self.game.update()

                if frame_counter >= 1.0:
                    # Frame Rate
                    print('Frame rate: ', frames)
                    frames = 0
                    frame_counter = 0.

            if render:
                self.rendering_engine.render(self.game.root_object)
                Window.add_to_queue(Window.render)
                Window.update()
                frames += 1
                self.frame_rater += 1
            else:
                Time.sleep()

        self._cleanUp()

    def _cleanUp(self):
        self.game.destroy()
        Input.destroy()
        Window.dispose()

    def create_window(self, title):
        Window.create(self.width, self.height, title)
        self.rendering_engine = RenderingEngine()

    def __del__(self):
        print('Average FPS: {avg:7.2f} | Total frames rendered: {tot:.0f}'.format(avg=self.frame_rater / self.frame_rater_count,
                                                                                  tot=self.frame_rater))
__author__ = 'michiel'

from gampy.engine.tkinter.window import Window
from gampy.engine.core.time import Time
from gampy.engine.tkinter.input import Input
from gampy.engine.render.renderengine import RenderEngine


class CoreEngine:

    def __init__(self, width, height, fps, game):
        # self.game = game.Game()

        self.is_running = False
        self.game = game
        self.width = width
        self.height = height
        self.frame_time = 1 / fps
        self.render_engine = None
        self.game.engine(self)
        self._fullscreen = False

        self.frame_rater = 0.
        self.frame_rater_count = 0.

    def toggle_fullscreen(self):
        self._fullscreen = not self._fullscreen
        Window.root.attributes('-fullscreen', self._fullscreen)
        Window.update()

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

                self.game.input(self.frame_time)
                Input.update()
                self.game.update(self.frame_time)

                if frame_counter >= 1.0:
                    # Frame Rate
                    print('Frame rate: ', frames)
                    frames = 0
                    frame_counter = 0.

            if render:
                self.game.render(self.render_engine)
                Window.add_to_queue(Window.render)
                Window.update()
                frames += 1
                self.frame_rater += 1
            else:
                Time.sleep(1)

        self._cleanUp()

    def _cleanUp(self):
        self.game.destroy()
        Input.destroy()
        Window.dispose()

    def create_window(self, title):
        Window.create(self.width, self.height, title)
        self.render_engine = RenderEngine()

    def __del__(self):
        if self.frame_rater_count:
            print('Average FPS: {avg:7.2f} | Total frames rendered: {tot:.0f}'.format(avg=self.frame_rater / self.frame_rater_count,
                                                                                  tot=self.frame_rater))
        else:
            print('No frames rendered!')
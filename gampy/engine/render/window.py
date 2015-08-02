__author__ = 'michiel'

import sdl2
from gampy.engine.events.time import Timing

timings = Timing()


class Window:

    MIN_WIDTH = 100
    MIN_HEIGHT = 100

    def __init__(self, width: int, height: int, title: str):
        if sdl2.SDL_Init(sdl2.SDL_INIT_VIDEO) != 0:
            print(sdl2.SDL_GetError())
            exit(1)

        self.is_display_open = True
        self.display = sdl2.SDL_CreateWindow(bytes(title, 'utf8'),
                                             sdl2.SDL_WINDOWPOS_UNDEFINED,
                                             sdl2.SDL_WINDOWPOS_UNDEFINED,
                                             width, height,
                                             sdl2.SDL_WINDOW_OPENGL)

        if not self.display:
            print(sdl2.SDL_GetError())
            exit(1)

        self.context = sdl2.SDL_GL_CreateContext(self.display)

        x = sdl2.SDL_GL_SetSwapInterval(0)
        if x < 0:
            print("Setting swap interval failed")
            print(sdl2.SDL_GetError())

    @timings
    def render(self):
        if self.is_display_open:
            sdl2.SDL_GL_SwapWindow(self.display)
        # sdl2.SDL_Delay(10)

    def display_closed(self):
        self.is_display_open = False

    def dispose(self):
        sdl2.SDL_GL_DeleteContext(self.context)
        sdl2.SDL_DestroyWindow(self.display)
        sdl2.SDL_Quit()

    def resize(self, event):
        pass
        # width = self.display.winfo_width()
        # height = self.display.winfo_height()
        # if width != event.width or height != event.height:
        #     self.display.config(width=event.width, height=event.height)
        #     gl.glViewport(0, 0, event.width, event.height)
        #     gl.glMatrixMode(gl.GL_PROJECTION)
        #     gl.glLoadIdentity()
        #     gl.glOrtho(-1, 1, -1, 1, -1, 1)

    # @property
    # def width(self):
    #     return self.display.winfo_width()
    #
    # @property
    # def height(self):
    #     return self.display.winfo_height()
    #
    # @property
    # def title(self):
    #     return self.display.title()

    def __del__(self):
        print("Window", timings)

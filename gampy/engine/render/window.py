__author__ = 'michiel'

import OpenGL.Tk


class Window:

    MIN_WIDTH = 100
    MIN_HEIGHT = 100
    display = None

    def __init__(self, width: int, height: int, title: str):

        self.is_display_open = True
        self.display = OpenGL.Tk.Togl(width=width, height=height)
        self.root = self.display.master
        self.root.title(title)
        self.root.minsize(self.MIN_WIDTH, self.MIN_HEIGHT)
        self.root.geometry("{width}x{height}".format(width=width, height=height))
        self.root.protocol('WM_DELETE_WINDOW', self.display_closed)

    def render(self):
        self.display.update()
        self.display.render()
        self.display.swapbuffers()

    def display_closed(self):
        self.is_display_open = False

    def dispose(self):
        self.display.destroy()

    @property
    def width(self):
        return self.display.winfo_width()

    @property
    def height(self):
        return self.display.winfo_height()

    @property
    def title(self):
        return self.display.title()
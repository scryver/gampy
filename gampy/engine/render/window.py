__author__ = 'michiel'

import OpenGL.Tk
import tkinter
import OpenGL.GL as gl
from gampy.engine.objects.transform import Transform


class Window:

    MIN_WIDTH = 100
    MIN_HEIGHT = 100
    display = None

    def __init__(self, width: int, height: int, title: str):

        self.is_display_open = True
        self.display = OpenGL.Tk.Togl(width=width, height=height)
        self.display.pack(fill=tkinter.BOTH, expand=True)
        self.root = self.display.master
        self.root.title(title)
        self.root.minsize(self.MIN_WIDTH, self.MIN_HEIGHT)
        self.root.geometry("{width}x{height}".format(width=width, height=height))
        self.root.protocol('WM_DELETE_WINDOW', self.display_closed)
        self.root.bind('<Configure>', self.resize)

    def update(self, delta):
        self.display.update()

    def render(self):
        self.display.render()
        self.display.swapbuffers()

    def display_closed(self):
        self.is_display_open = False

    def dispose(self):
        self.display.destroy()

    def resize(self, event):
        width = event.width
        height = event.height

        if height <= 0:
            height = 1

        Transform.set_projection(70., width, height, 0.1, 1000.)

    @property
    def width(self):
        return self.root.winfo_width()

    @property
    def height(self):
        return self.root.winfo_height()

    @property
    def title(self):
        return self.root.title()
__author__ = 'michiel'

import tkinter

import OpenGL.Tk

from gampy.engine.core.transform import Transform


class Window:

    MIN_WIDTH = 100
    MIN_HEIGHT = 100
    display = None
    root = None
    is_display_open = False
    width = 0
    height = 0

    @classmethod
    def create(cls, width: int, height: int, title: str):
        cls.is_display_open = True
        cls.display = OpenGL.Tk.Togl(width=width, height=height)
        cls.display.pack(fill=tkinter.BOTH, expand=True)
        cls.root = cls.display.master
        cls.root.title(title)
        cls.root.minsize(cls.MIN_WIDTH, cls.MIN_HEIGHT)
        cls.root.geometry("{width}x{height}".format(width=width, height=height))
        cls.root.protocol('WM_DELETE_WINDOW', cls.display_closed)
        cls.root.bind('<Configure>', cls.resize)
        cls.width = width
        cls.height = height

    @classmethod
    def update(cls, delta):
        cls.display.update()

    @classmethod
    def render(cls):
        cls.display.render()
        cls.display.swapbuffers()

    @classmethod
    def display_closed(cls):
        cls.is_display_open = False

    @classmethod
    def dispose(cls):
        cls.display.destroy()

    @classmethod
    def resize(cls, event):
        cls.width = event.width
        cls.height = event.height

        if cls.height <= 0:
            cls.height = 1

        Transform.set_projection(70., cls.width, cls.height, 0.1, 1000.)
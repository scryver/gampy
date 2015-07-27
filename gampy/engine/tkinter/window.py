__author__ = 'michiel'

import tkinter
import queue

import OpenGL.Tk
import OpenGL.GL as gl

from gampy.engine.core.transform import Transform
from gampy.engine.core.math3d import Vector2


class Window:

    MIN_WIDTH = 100
    MIN_HEIGHT = 100
    display = None
    root = None
    is_display_open = False
    width = 0
    height = 0
    aspect = 0
    queue = None
    center = Vector2(width // 2, height // 2)

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
        cls.set_center(width, height)
        if height == 0:
            height = 1
        cls.aspect = width / height

        cls.queue = queue.Queue()
        cls.process_queue()

    @classmethod
    def process_queue(cls):
        try:
            while 1:
                process = cls.queue.get_nowait()
                if process is None:
                    pass
                else:
                    process()
                cls.display.update_idletasks()
        except queue.Empty:
            pass
        cls.display.after(10, cls.process_queue)

    @classmethod
    def add_to_queue(cls, process):
        cls.queue.put(process)

    @classmethod
    def clear_queue(cls):
        cls.queue.put(None)

    @classmethod
    def update(cls):
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
        cls.aspect = cls.width / cls.height

        Transform.width = event.width
        Transform.height = event.height

        cls.set_center(event.width, event.height)

    @classmethod
    def set_center(cls, width, height):
        cls.center.x = width // 2
        cls.center.y = height // 2

    @classmethod
    def bind_as_render_target(cls):
        gl.glBindTexture(gl.GL_TEXTURE_2D, 0)
        gl.glBindFramebuffer(gl.GL_FRAMEBUFFER, 0)
        gl.glViewport(0, 0, cls.width, cls.height)
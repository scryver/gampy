__author__ = 'michiel'

from gampy.engine.objects.vectors import Vector3
import OpenGL.GL as gl
from OpenGL.arrays import vbo
from gampy.engine.events.time import Timing

timings = Timing()


class Vertex:

    # Amount of numbers in vertex
    SIZE = 3

    def __init__(self, pos=None):
        if pos == None:
            pos = Vector3()
        self.pos = pos


class Mesh:

    def __init__(self):
        self.size = 0
        self.ibo = None     # Index Buffer Object id
        self.vbo = None     # Vertex Buffer Object id

    def add_vertices(self, vertices, indices, usage=None):
        self.size = len(indices)

        if usage == None:
            usage = gl.GL_STATIC_DRAW

        self.vbo = vbo.VBO(data=vertices, usage=usage, target=gl.GL_ARRAY_BUFFER)
        self.ibo = vbo.VBO(data=indices, usage=usage, target=gl.GL_ELEMENT_ARRAY_BUFFER)

    @timings
    def draw(self):
        self.vbo.bind()
        self.ibo.bind()
        try:
            gl.glEnableClientState(gl.GL_VERTEX_ARRAY)
            gl.glVertexPointer(3, gl.GL_FLOAT, 0, self.vbo)
            gl.glDrawElements(gl.GL_TRIANGLES, self.size, gl.GL_UNSIGNED_INT, None)
        finally:
            self.vbo.unbind()
            self.ibo.unbind()
            gl.glDisableClientState(gl.GL_VERTEX_ARRAY)

    def update(self, dt):
        pass

    def __del__(self):
        if self.vbo is not None:
            self.vbo.delete()
        if self.ibo is not None:
            self.ibo.delete()
        print("Mesh", timings)

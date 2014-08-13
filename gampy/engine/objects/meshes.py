__author__ = 'michiel'

from gampy.engine.objects.vectors import Vector3
import gampy.engine.objects.util as util
import OpenGL.GL as gl
from OpenGL.arrays import vbo


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
        self.vbo = None

    def add_vertices(self, vertices, usage=None):
        self.size = len(vertices)

        if usage == None:
            usage = gl.GL_STATIC_DRAW

        self.vbo = vbo.VBO(data=util.cast_object_array(vertices), usage=usage, target=gl.GL_ARRAY_BUFFER)

    def draw(self):
        self.vbo.bind()
        try:
            gl.glEnableClientState(gl.GL_VERTEX_ARRAY)
            gl.glVertexPointer( 3, gl.GL_FLOAT, 0, self.vbo)
            gl.glDrawArrays(gl.GL_TRIANGLES, 0, self.size)
        finally:
            self.vbo.unbind()
            gl.glDisableClientState(gl.GL_VERTEX_ARRAY)

    def update(self, dt):
        pass
__author__ = 'michiel'

from gampy.engine.objects.vectors import Vector3, Vector2
import OpenGL.GL as gl
import ctypes
from OpenGL.arrays import vbo
from gampy.engine.objects.util import cast_object_indices, cast_object_vertexes


class Vertex:

    # Amount of numbers in vertex
    SIZE = 5

    def __init__(self, pos=None, tex_coord=None):
        if pos == None:
            pos = Vector3()
        if tex_coord == None:
            tex_coord = Vector2()
        self.pos = pos
        self.tex_coord = tex_coord


class Mesh:

    def __init__(self):
        self.size = 0
        self.ibo = None     # Index Buffer Object id
        self.vbo = None     # Vertex Buffer Object id

    def add_vertices(self, vertices, indices, usage=None):
        self.size = len(indices)

        if usage == None:
            usage = gl.GL_STATIC_DRAW

        self.vbo = vbo.VBO(data=cast_object_vertexes(vertices), usage=usage, target=gl.GL_ARRAY_BUFFER)
        self.ibo = vbo.VBO(data=cast_object_indices(indices), usage=usage, target=gl.GL_ELEMENT_ARRAY_BUFFER)

    def draw(self):
        self.vbo.bind()
        self.ibo.bind()
        try:
            gl.glEnableVertexAttribArray(0)
            gl.glEnableVertexAttribArray(1)

            gl.glVertexAttribPointer(0, 3, gl.GL_FLOAT, False, Vertex.SIZE * 4, None)
            gl.glVertexAttribPointer(1, 2, gl.GL_FLOAT, False, Vertex.SIZE * 4, self.vbo + 12)

            gl.glDrawElements(gl.GL_TRIANGLES, self.size, gl.GL_UNSIGNED_INT, None)
        finally:
            self.vbo.unbind()
            self.ibo.unbind()
            gl.glDisableVertexAttribArray(0)
            gl.glDisableVertexAttribArray(1)

    def update(self, dt):
        pass
__author__ = 'michiel'

import OpenGL.GL as gl
from OpenGL.arrays import vbo
from gampy.engine.core.util import cast_object_indices, cast_object_vertexes
import numpy

class MeshResource:

    def __init__(self, vertices, indices, usage=None):
        if usage is None:
            usage = gl.GL_STATIC_DRAW

        self._vbo = vbo.VBO(data=numpy.array(vertices, dtype=numpy.float32), usage=usage, target=gl.GL_ARRAY_BUFFER)            # Vertex Buffer Object id
        self._ibo = vbo.VBO(data=numpy.array(indices, dtype=numpy.uint32), usage=usage, target=gl.GL_ELEMENT_ARRAY_BUFFER)    # Index Buffer Object id
        self._size = len(indices)
        self._ref_count = 1 # keep track of references to this data block

    @property
    def ibo(self):
        return self._ibo

    @property
    def vbo(self):
        return self._vbo

    @property
    def size(self):
        return self._size

    def add_reference(self):
        self._ref_count += 1

    def remove_reference(self):
        self._ref_count -= 1

        return self._ref_count == 0

    def bind(self):
        self._vbo.bind()
        self._ibo.bind()

    def unbind(self):
        self._ibo.unbind()
        self._vbo.unbind()

    def draw(self, vertex_size):
        self.bind()
        try:
            gl.glEnableVertexAttribArray(0)     # Vertices attributes
            gl.glEnableVertexAttribArray(1)     # Texture coordinate attributes
            gl.glEnableVertexAttribArray(2)     # Normals attributes

            gl.glVertexAttribPointer(0, 3, gl.GL_FLOAT, False, vertex_size * 4, None)
            gl.glVertexAttribPointer(1, 2, gl.GL_FLOAT, False, vertex_size * 4, self._vbo + 12)
            gl.glVertexAttribPointer(2, 3, gl.GL_FLOAT, False, vertex_size * 4, self._vbo + 20)

            gl.glDrawElements(gl.GL_TRIANGLES, self._size, gl.GL_UNSIGNED_INT, None)
        finally:
            self.unbind()
            gl.glDisableVertexAttribArray(0)
            gl.glDisableVertexAttribArray(1)
            gl.glDisableVertexAttribArray(2)

    def __del__(self):
        self._vbo.delete()
        self._ibo.delete()


class TextureResource:

    def __init__(self, id):
        self._ref_count = 1 # keep track of references to this data block
        self._id = id

    def add_reference(self):
        self._ref_count += 1

    def remove_reference(self):
        self._ref_count -= 1
        return self._ref_count == 0

    @property
    def id(self):
        return self._id

    def __del__(self):
        gl.glDeleteBuffers(1, self._id)

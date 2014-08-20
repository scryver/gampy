__author__ = 'michiel'

from gampy.engine.core.vectors import Vector3, Vector2
import OpenGL.GL as gl
import numpy
from OpenGL.arrays import vbo
import os
from gampy.engine.core.util import cast_object_indices, cast_object_vertexes, remove_empty_strings
from gampy.engine.render.meshloading import OBJModel

class MeshLoadError(Exception):

    def __init__(self, message='ERROR'):
        message = '\nMesh Loading Failed: ' + str(message)
        super(MeshLoadError, self).__init__(message)


class Vertex:

    # Amount of numbers in vertex
    SIZE = 8

    def __init__(self, position=None, tex_coord=None, normal=None):
        if position == None:
            position = Vector3()
        if tex_coord == None:
            tex_coord = Vector2()
        if normal == None:
            normal = Vector3()

        if not isinstance(position, Vector3):
            position = Vector3(position)
        if not isinstance(tex_coord, Vector2):
            tex_coord = Vector2(tex_coord)
        if not isinstance(normal, Vector3):
            normal = Vector3(normal)

        self.position = position
        self.tex_coord = tex_coord
        self._normal = normal

    @property
    def normal(self):
        return self._normal

    @normal.setter
    def normal(self, normal):
        self._normal = normal


class Mesh:

    def __init__(self, vertices, indices=None, calc_norm=False, usage=None):
        self.size = 0
        self.ibo = None     # Index Buffer Object id
        self.vbo = None     # Vertex Buffer Object id

        if isinstance(vertices, str):
            """A file has been passed in"""
            self._load_mesh(vertices)
        else:
            self._add_vertices(vertices, indices, calc_norm, usage)

    def _add_vertices(self, vertices, indices, calc_norm=False, usage=None):
        if calc_norm:
            self._calc_normals(vertices, indices)

        self.size = len(indices)

        if usage == None:
            usage = gl.GL_STATIC_DRAW

        self.vbo = vbo.VBO(data=cast_object_vertexes(vertices), usage=usage, target=gl.GL_ARRAY_BUFFER)
        self.ibo = vbo.VBO(data=cast_object_indices(indices), usage=usage, target=gl.GL_ELEMENT_ARRAY_BUFFER)

    def draw(self):
        self.vbo.bind()
        self.ibo.bind()
        try:
            gl.glEnableVertexAttribArray(0)     # Vertices attributes
            gl.glEnableVertexAttribArray(1)     # Texture coordinate attributes
            gl.glEnableVertexAttribArray(2)     # Normals attributes

            gl.glVertexAttribPointer(0, 3, gl.GL_FLOAT, False, Vertex.SIZE * 4, None)
            gl.glVertexAttribPointer(1, 2, gl.GL_FLOAT, False, Vertex.SIZE * 4, self.vbo + 12)
            gl.glVertexAttribPointer(2, 3, gl.GL_FLOAT, False, Vertex.SIZE * 4, self.vbo + 20)

            gl.glDrawElements(gl.GL_TRIANGLES, self.size, gl.GL_UNSIGNED_INT, None)
        finally:
            self.vbo.unbind()
            self.ibo.unbind()
            gl.glDisableVertexAttribArray(0)
            gl.glDisableVertexAttribArray(1)
            gl.glDisableVertexAttribArray(2)

    def _calc_normals(self, vertices, indices):
        for i in range(0, len(indices), 3):
            i0 = indices[i]
            i1 = indices[i + 1]
            i2 = indices[i + 2]

            v1 = vertices[i1].position - vertices[i0].position
            v2 = vertices[i2].position - vertices[i0].position

            normal = v1.cross(v2).normalized()

            vertices[i0].normal = vertices[i0].normal + normal
            vertices[i1].normal = vertices[i1].normal + normal
            vertices[i2].normal = vertices[i2].normal + normal

        for i in range(len(vertices)):
            vertices[i].normal = vertices[i].normal.normalized()

    def update(self):
        pass

    def _load_mesh(self, file_name: str):
        split_array = file_name.split('.')
        ext = split_array[len(split_array) - 1]

        if ext != 'obj':
            raise MeshLoadError('Not an OBJ file')

        test = OBJModel(os.path.join(os.path.dirname(__file__), '..', '..', 'res', 'models', file_name))
        model = test.to_indexed_model()
        model.calc_normals()

        vertices = []
        for i in range(len(model.indices)):
            vertex = Vertex(model.positions[i], model.tex_coords[i], model.normals[i])
            vertices.append(vertex)

        indices = model.indices

        self._add_vertices(vertices, indices)
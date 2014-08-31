__author__ = 'michiel'

import os
import numpy
from gampy.engine.core.math3d import Vector3, Vector2
from gampy.engine.render.meshloading import OBJModel
from gampy.engine.render.resourcemanagement import MeshResource

class MeshLoadError(Exception):

    def __init__(self, message='ERROR'):
        message = '\nMesh Loading Failed: ' + str(message)
        super(MeshLoadError, self).__init__(message)


class Vertex(numpy.ndarray):

    # Amount of numbers in vertex
    SIZE = 11

    def __new__(subtype, position=None, tex_coord=None, normal=None, tangent=None,
                shape=None, dtype=numpy.float32):
        if shape is None:
            shape = Vertex.SIZE
        obj = numpy.zeros(shape, dtype).view(Vertex)
        if position is not None:
            obj[0:3] = position
        if tex_coord is not None:
            obj[3:5] = tex_coord
        if normal is not None:
            obj[5:8] = normal
        if tangent is not None:
            obj[8:] = tangent
        return obj

    def __array_finalize__(self, obj):
        if obj is None: return

    # def __init__(self, position=None, tex_coord=None, normal=None):
    #     if position == None:
    #         position = Vector3()
    #     if tex_coord == None:
    #         tex_coord = Vector2()
    #     if normal == None:
    #         normal = Vector3()
    #
    #     if not isinstance(position, Vector3):
    #         position = Vector3(position)
    #     if not isinstance(tex_coord, Vector2):
    #         tex_coord = Vector2(tex_coord)
    #     if not isinstance(normal, Vector3):
    #         normal = Vector3(normal)
    #
    #     self._array = numpy.zeros(Vertex.SIZE, dtype=numpy.float32)
    #
    #     self.position = position
    #     self.tex_coord = tex_coord
    #     self.normal = normal

    @property
    def position(self):
        return self[0:3]

    @position.setter
    def position(self, value):
        self[0:3] = value

    @property
    def tex_coord(self):
        return self[3:5]

    @tex_coord.setter
    def tex_coord(self, value):
        self[3:5] = value

    @property
    def normal(self):
        return self[5:8]

    @normal.setter
    def normal(self, normal):
        self[5:8] = normal

    @property
    def tangent(self):
        return self[8:]

    @tangent.setter
    def tangent(self, normal):
        self[8:] = normal


class Mesh:

    loaded_models = dict()

    def __init__(self, vertices, indices=None, calc_norm=False, calc_tangent=False, usage=None):
        self.resource = None
        self._filename = None

        if isinstance(vertices, str):
            """A file has been passed in"""
            old_resource = Mesh.loaded_models.get(vertices, None)
            self._filename = vertices
            if old_resource is not None:
                self.resource = old_resource
                self.resource.add_reference()
            else:
                self._load_mesh(vertices)
                Mesh.loaded_models.update({vertices: self.resource})
        else:
            self._add_vertices(vertices, indices, calc_norm, calc_tangent)

    def _add_vertices(self, vertices, indices, calc_norm=False, calc_tangent=False):
        if calc_norm:
            self._calc_normals(vertices, indices)
        if calc_tangent:
            self._calc_tangents(vertices)

        self.resource = MeshResource(vertices, indices)

    def draw(self):
        self.resource.draw(Vertex.SIZE)

    def _calc_normals(self, vertices, indices):
        for i in range(0, len(indices), 3):
            i0 = indices[i]
            i1 = indices[i + 1]
            i2 = indices[i + 2]

            edge1 = Vector3(vertices[i1].position - vertices[i0].position)
            edge2 = Vector3(vertices[i2].position - vertices[i0].position)

            normal = edge1.cross(edge2).view(Vector3).normalized()

            vertices[i0].normal = vertices[i0].normal + normal
            vertices[i1].normal = vertices[i1].normal + normal
            vertices[i2].normal = vertices[i2].normal + normal

        for i in range(len(vertices)):
            vertices[i].normal = vertices[i].normal.view(Vector3).normalized()

    def _calc_tangents(self, vertices, indices=None):
        for i in range(len(vertices)):
            c1 = numpy.cross(vertices[i].normal, Vector3(0, 0, 1)).view(Vector3)
            c2 = numpy.cross(vertices[i].normal, Vector3(0, 1, 0)).view(Vector3)

            if c1.length > c2.length:
                tangent = c1.normalized()
            else:
                tangent = c2.normalized()

            vertices[i].tangent = tangent

    def update(self):
        pass

    def _load_mesh(self, file_name: str):
        split_array = file_name.split('.')
        ext = split_array[len(split_array) - 1]

        if ext != 'obj':
            raise MeshLoadError('Not an OBJ file "{filename}"'.format(file_name))

        test = OBJModel(os.path.join(os.path.dirname(__file__), '..', '..', 'res', 'models', file_name))
        model = test.to_indexed_model()
        # model.calc_normals()

        vertices = []
        for i in range(len(model.positions)):
            vertex = Vertex(model.positions[i], model.tex_coords[i], model.normals[i])
            vertices.append(vertex)

        indices = model.indices

        self._add_vertices(vertices, indices)

    def __del__(self):
        if self.resource.remove_reference() and self._filename is not None:
            Mesh.loaded_models.pop(self._filename)
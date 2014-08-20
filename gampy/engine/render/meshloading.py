__author__ = 'michiel'

import os.path
import numpy
from gampy.engine.core.util import cast_object_indices, cast_object_vertexes, remove_empty_strings
from gampy.engine.core.vectors import Vector2, Vector3


class IndexedModel:

    def __init__(self):
        self._positions = []
        self._tex_coords = []
        self._normals = []
        self._indices = []

    @property
    def positions(self):
        return self._positions

    @property
    def indices(self):
        return self._indices

    @property
    def tex_coords(self):
        return self._tex_coords

    @property
    def normals(self):
        return self._normals

    def calc_normals(self):
        for i in range(0, len(self._indices), 3):
            i0 = self._indices[i]
            i1 = self._indices[i + 1]
            i2 = self._indices[i + 2]

            v1 = self._positions[i1] - self._positions[i0]
            v2 = self._positions[i2] - self._positions[i0]

            normal = v1.cross(v2).normalized()

            self._normals[i0] = self._normals[i0] + normal
            self._normals[i1] = self._normals[i1] + normal
            self._normals[i2] = self._normals[i2] + normal

        for i in range(len(self._normals)):
            self._normals[i] = self._normals[i].normalized()


class OBJModel:

    def __init__(self, file_name):
        positions = []
        tex_coords = []
        normals = []
        indices = []
        self._has_tex_coords = False
        self._has_normals = False

        with open(file_name, 'r', 1) as mesh_reader:
            for line in mesh_reader:
                tokens = line.split(' ')
                tokens = remove_empty_strings(tokens)

                # empty lines and comments
                if len(tokens) == 0 or tokens[0] == '#':
                    continue
                elif tokens[0] == 'v':
                    positions.append(Vector3(tokens[1], tokens[2], tokens[3]))
                elif tokens[0] == 'vt':
                    tex_coords.append(Vector2(tokens[1], tokens[2]))
                elif tokens[0] == 'vn':
                    normals.append(Vector3(tokens[1], tokens[2], tokens[3]))
                elif tokens[0] == 'f':
                    for i in range(len(tokens) - 3):
                        indices.append(self._parse_obj_index(tokens[1]))
                        indices.append(self._parse_obj_index(tokens[2 + i]))
                        indices.append(self._parse_obj_index(tokens[3 + i]))
        mesh_reader.close()

        self._positions = positions
        self._tex_coords = tex_coords
        self._normals = normals
        self._indices = indices

    @property
    def positions(self):
        return self._positions

    @property
    def indices(self):
        return self._indices

    @property
    def tex_coords(self):
        return self._tex_coords

    @property
    def normals(self):
        return self._normals

    def to_indexed_model(self):
        result = IndexedModel()
        index_map = dict()

        current_vertex_index = 0
        for i in range(len(self._indices)):
            current_index = self._indices[i]

            current_pos = self._positions[current_index.vertex_index]
            if self._has_tex_coords:
                current_tex = self._tex_coords[current_index.tex_coords_index]
            else:
                current_tex = [0, 0]
            if self._has_normals:
                current_norm = self._normals[current_index.normal_index]
            else:
                current_norm = [0, 0, 0]

            prev_vertex_index = -1
            for j in range(i):
                old_index = self._indices[j]

                if current_index.vertex_index == old_index.vertex_index and \
                    current_index.tex_coords_index == old_index.tex_coords_index and \
                    current_index.normal_index == old_index.normal_index:
                    prev_vertex_index = j
                    break

            if prev_vertex_index == -1:
                index_map.update({i: current_vertex_index})
                result._positions.append(current_pos)
                result._tex_coords.append(current_tex)
                result._normals.append(current_norm)
                result._indices.append(current_vertex_index)
                current_vertex_index += 1
            else:
                result._indices.append(index_map[prev_vertex_index])

        result._indices = numpy.array(result._indices, dtype=numpy.uint32)
        return result

    def _parse_obj_index(self, token):
        values = token.split('/')

        result = OBJIndex()
        result.vertex_index = int(values[0]) - 1

        if len(values) > 1:
            self._has_tex_coords = True
            result.tex_coords_index = int(values[1]) - 1
            if len(values) > 2:
                self._has_normals = True
                result.normal_index = int(values[2]) - 1

        return result


class OBJIndex:

    def __init__(self):
        self.vertex_index = None
        self.tex_coords_index = None
        self.normal_index = None
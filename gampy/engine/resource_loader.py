__author__ = 'michiel'


import numpy as np
from gampy.engine.util import remove_empty_strings
from gampy.engine.objects.meshes import Mesh


class ResourceException(Exception):

    def __init__(self, message='ERROR'):
        message = '\nResource Exception: ' + str(message)
        super(ResourceException, self).__init__(message)


class MeshLoadError(ResourceException):

    def __init__(self, message='ERROR'):
        message = '\n\tMesh Loading Failed: ' + str(message)
        super(MeshLoadError, self).__init__(message)


def load_shader(fileName, type='vertex'):
    file = open('../res/shaders/{type}/{fileName}'.format(type=type, fileName=fileName), 'r', 1)
    shader = ''
    for line in file:
        shader += line + '\n'

    file.close()

    return shader

def load_mesh(fileName: str):
    split_array = fileName.split('.')
    ext = split_array[len(split_array) - 1]

    if ext != 'obj':
        raise MeshLoadError('Not an OBJ file')

    vertices = []
    indices = []

    mesh_reader = open('../res/models/{fileName}'.format(type=type, fileName=fileName), 'r', 1)
    for line in mesh_reader:
        tokens = line.split(' ')
        tokens = remove_empty_strings(tokens)

        # empty lines and comments
        if len(tokens) == 0 or tokens[0] == '#':
            continue
        elif tokens[0] == 'v':
            vertices.append([float(tokens[1]),
                             float(tokens[2]),
                             float(tokens[3])])
        elif tokens[0] == 'f':
            indices.append(int(tokens[1]) - 1)
            indices.append(int(tokens[2]) - 1)
            indices.append(int(tokens[3]) - 1)

    mesh_reader.close()

    vertices = np.array(vertices, dtype=np.float32)
    indices = np.array(indices, dtype=np.uint32)

    mesh = Mesh()
    mesh.add_vertices(vertices, indices)

    return mesh
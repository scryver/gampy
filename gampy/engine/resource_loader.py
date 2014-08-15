__author__ = 'michiel'


import numpy as np
import OpenGL.GL as gl
from gampy.engine.util import remove_empty_strings
from gampy.engine.objects.meshes import Mesh
from gampy.engine.render.texture import Texture
from PIL import Image


class ResourceException(Exception):

    def __init__(self, message='ERROR'):
        message = '\nResource Exception: ' + str(message)
        super(ResourceException, self).__init__(message)


class MeshLoadError(ResourceException):

    def __init__(self, message='ERROR'):
        message = '\n\tMesh Loading Failed: ' + str(message)
        super(MeshLoadError, self).__init__(message)


class TextureLoadError(ResourceException):

    def __init__(self, message='ERROR'):
        message = '\n\tTexture Loading Failed: ' + str(message)
        super(TextureLoadError, self).__init__(message)


def load_shader(file_name, type='vertex'):
    shader = ''
    with open('../res/shaders/{type}/{fileName}'.format(type=type, fileName=file_name), 'r', 1) as file:
        for line in file:
            shader += line + '\n'

        file.close()

    return shader


def load_mesh(file_name: str):
    split_array = file_name.split('.')
    ext = split_array[len(split_array) - 1]

    if ext != 'obj':
        raise MeshLoadError('Not an OBJ file')

    vertices = []
    indices = []

    with open('../res/models/{fileName}'.format(fileName=file_name), 'r', 1) as mesh_reader:
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
                indices.append(int(tokens[1].split('/')[0]) - 1)
                indices.append(int(tokens[2].split('/')[0]) - 1)
                indices.append(int(tokens[3].split('/')[0]) - 1)

                # For quad faces
                if len(tokens) > 4:
                    indices.append(int(tokens[1].split('/')[0]) - 1)
                    indices.append(int(tokens[3].split('/')[0]) - 1)
                    indices.append(int(tokens[4].split('/')[0]) - 1)


    mesh_reader.close()

    vertices = np.array(vertices, dtype=np.float32)
    indices = np.array(indices, dtype=np.uint32)

    mesh = Mesh()
    mesh.add_vertices(vertices, indices)

    return mesh


def load_texture(texture_name: str):
    # # http://pyopengl.sourceforge.net/context/tutorials/nehe6.html
    #
    # # PIL defines an "open" method which is Image specific!
    # tex = Image.open('../res/textures/{tex}'.format(tex=texture_name))
    # if tex.mode == 'P':
    #     tex = tex.convert('RGB')
    # components, format = getLengthFormat(tex)
    #
    # tx, ty, texture = tex.size[0], tex.size[1], tex.tostring("raw", tex.mode, 0, -1)
    #
    # # Generate a texture ID
    # id = gl.glGenTextures(1)
    # # Make our new texture ID the current 2D texture
    # gl.glBindTexture(gl.GL_TEXTURE_2D, id)
    # gl.glPixelStorei(gl.GL_UNPACK_ALIGNMENT, 1)
    # # Copy the texture data into the current texture ID
    # # gl.glPixelStorei(gl.GL_PACK_ALIGNMENT, 1)
    # gl.glTexImage2D(
    #     gl.GL_TEXTURE_2D, 0, components, tx, ty, 0,
    #     format, gl.GL_UNSIGNED_BYTE, texture
    # )
    #
    # return id

    img = Image.open('../res/textures/{tex}'.format(tex=texture_name)) # .jpg, .bmp, etc. also work
    if img.mode == 'P':
        img = img.convert('RGB')
    img_data = np.array(list(img.getdata()), np.int8)
    components, format = getLengthFormat(img)

    texture = gl.glGenTextures(1)
    # gl.glPixelStorei(gl.GL_UNPACK_ALIGNMENT,1)        # Don't know why
    # gl.glPixelStorei(gl.GL_PACK_ALIGNMENT,1)          # Don't know why
    gl.glBindTexture(gl.GL_TEXTURE_2D, texture)
    gl.glTexParameterf(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_WRAP_S, gl.GL_CLAMP)         # Don't know why
    gl.glTexParameterf(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_WRAP_T, gl.GL_CLAMP)         # Don't know why
    gl.glTexParameterf(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_NEAREST)    # Don't know why
    gl.glTexParameterf(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MIN_FILTER, gl.GL_NEAREST)    # Don't know why
    gl.glTexImage2D(gl.GL_TEXTURE_2D, 0, components, img.size[0], img.size[1], 0, format, gl.GL_UNSIGNED_BYTE, img_data)

    return Texture(texture)



def getLengthFormat( image ):
	"""Return PIL image component-length and format

	This returns the number of components, and the OpenGL
	mode constant describing the PIL image's format.  It
	currently only supports GL_RGBA, GL_RGB and GL_LUIMANCE
	formats (PIL: RGBA, RGBX, RGB, and L), the Texture
	object's ensureRGB converts Paletted images to RGB
	before they reach this function.
	"""
	if image.mode == "RGB":
		length = 3
		format = gl.GL_RGB
	elif image.mode in ("RGBA","RGBX"):
		length = 4
		format = gl.GL_RGBA
	elif image.mode == "L":
		length = 1
		format = gl.GL_LUMINANCE
	else:
		raise TypeError ("Currently only support Luminance, RGB and RGBA images. Image is type %s"%image.mode)
	return length, format
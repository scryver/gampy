__author__ = 'michiel'

import OpenGL.GL as gl
from OpenGL.arrays import vbo
from gampy.engine.core.vectors import Vector3
import numpy
from PIL import Image

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
            gl.glEnableVertexAttribArray(3)     # Tangent attributes

            gl.glVertexAttribPointer(0, 3, gl.GL_FLOAT, False, vertex_size * 4, None)
            gl.glVertexAttribPointer(1, 2, gl.GL_FLOAT, False, vertex_size * 4, self._vbo + 12)
            gl.glVertexAttribPointer(2, 3, gl.GL_FLOAT, False, vertex_size * 4, self._vbo + 20)
            gl.glVertexAttribPointer(3, 3, gl.GL_FLOAT, False, vertex_size * 4, self._vbo + 32)

            gl.glDrawElements(gl.GL_TRIANGLES, self._size, gl.GL_UNSIGNED_INT, None)
        finally:
            self.unbind()
            gl.glDisableVertexAttribArray(0)
            gl.glDisableVertexAttribArray(1)
            gl.glDisableVertexAttribArray(2)
            gl.glDisableVertexAttribArray(3)

    def __del__(self):
        self._vbo.delete()
        self._ibo.delete()


class TextureResource:

    def __init__(self, width, height, num_textures = 1, data=None, filters=None, components=gl.GL_RGBA,
                 formats=gl.GL_RGBA, tex_target=gl.GL_TEXTURE_2D, attachments=None, clamp=False):
        if data is None:
            raise ValueError('Texture resource data is none')
        if num_textures == 1:
            data = [data]
            filters = [filters]
            components = [components]
            formats = [formats]
            attachments = [attachments]
        self._ref_count = 1 # keep track of references to this data block'
        self._id = []
        self._num_texs = num_textures
        self._tex_target = tex_target
        self._width = width
        self._height = height
        self._frame_buffer = 0

        self.init_textures(data, filters, components, formats, clamp)
        self.init_render_targets(attachments)

    def add_reference(self):
        self._ref_count += 1

    def remove_reference(self):
        self._ref_count -= 1
        return self._ref_count == 0

    @property
    def id(self):
        return self._id[0]

    @property
    def num_textures(self):
        return self._num_texs

    def init_textures(self, data, filters, components, formats, clamp):
        if filters[0] is None:
            filters = [gl.GL_LINEAR for i in range(self._num_texs)]
        for i in range(self._num_texs):
            self._id.append(gl.glGenTextures(1))
            gl.glBindTexture(self._tex_target, self._id[i])
            gl.glTexParameterf(self._tex_target, gl.GL_TEXTURE_MIN_FILTER, filters[i])    # Linear filter for colors
            gl.glTexParameterf(self._tex_target, gl.GL_TEXTURE_MAG_FILTER, filters[i])

            if clamp:
                gl.glTexParameterf(self._tex_target, gl.GL_TEXTURE_WRAP_S, gl.GL_CLAMP_TO_EDGE)        # Repeat texture in x and y
                gl.glTexParameterf(self._tex_target, gl.GL_TEXTURE_WRAP_T, gl.GL_CLAMP_TO_EDGE)
            # else:
            #     gl.glTexParameterf(self._tex_target, gl.GL_TEXTURE_WRAP_S, gl.GL_REPEAT)        # Repeat texture in x and y
            #     gl.glTexParameterf(self._tex_target, gl.GL_TEXTURE_WRAP_T, gl.GL_REPEAT)

            gl.glTexImage2D(self._tex_target, 0, components[i], self._width, self._height, 0,
                            formats[i], gl.GL_UNSIGNED_BYTE, data[i])

            if filters[i] == gl.GL_NEAREST_MIPMAP_NEAREST or filters[i] == gl.GL_NEAREST_MIPMAP_LINEAR or \
               filters[i] == gl.GL_LINEAR_MIPMAP_NEAREST or filters[i] == gl.GL_LINEAR_MIPMAP_LINEAR:
                pass
            else:
                gl.glTexParameteri(self._tex_target, gl.GL_TEXTURE_BASE_LEVEL, 0)
                gl.glTexParameteri(self._tex_target, gl.GL_TEXTURE_MAX_LEVEL, 0)

    def init_render_targets(self, attachments):
        if attachments[0] is None:
            return

        draw_buffers = numpy.array([0 for i in range(self._num_texs)])

        for i in range(self._num_texs):
            # Todo add stencil buffer
            if attachments[i] == gl.GL_DEPTH_ATTACHMENT:
                draw_buffers[i] = gl.GL_NONE
            else:
                draw_buffers[i] = attachments[i]

            if attachments[i] == gl.GL_NONE:
                continue
            if self._frame_buffer == 0:
                self._frame_buffer = gl.glGenFramebuffers(1)
                gl.glBindFramebuffer(gl.GL_FRAMEBUFFER, self._frame_buffer)

            gl.glFramebufferTexture2D(gl.GL_FRAMEBUFFER, attachments[i], self._tex_target, self._id[i], 0)

        if self._frame_buffer == 0:
            return

        gl.glDrawBuffers(self._num_texs, draw_buffers)

        if gl.glCheckFramebufferStatus(gl.GL_FRAMEBUFFER) != gl.GL_FRAMEBUFFER_COMPLETE:
            raise gl.error.GLError('Framebuffer not completed in texture resource render target init.\n')

        gl.glBindFramebuffer(gl.GL_FRAMEBUFFER, 0)

    def bind(self, tex_id):
        gl.glBindTexture(self._tex_target, self._id[tex_id])

    def bind_as_render_target(self):
        self.bind(0)
        gl.glBindFramebuffer(gl.GL_FRAMEBUFFER, self._frame_buffer)
        gl.glViewport(0, 0, self._width, self._height)

    def __del__(self):
        for i in range(len(self._id)):
            gl.glDeleteTextures(self._id[i])
        if self._frame_buffer != 0:
            gl.glDeleteFramebuffers(int(self._frame_buffer))


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


class ShaderResource:

    def __init__(self):
        self._ref_count = 1 # keep track of references to this data block
        self._program = gl.glCreateProgram()

        if self._program == 0:
            raise gl.Error('Could not find valid memory location for shader program in constructor')

        self._uniforms = dict()
        self._uniform_names = dict()
        self._uniform_types = dict()

    @property
    def uniforms(self):
        return self._uniforms

    @property
    def uniform_names(self):
        return self._uniform_names

    @property
    def uniform_types(self):
        return self._uniform_types

    def add_reference(self):
        self._ref_count += 1

    def remove_reference(self):
        self._ref_count -= 1
        return self._ref_count == 0

    @property
    def program(self):
        return self._program

    def __del__(self):
        gl.glDeleteBuffers(1, self._program)


class MappedValue:

    def __init__(self):
        self._map = dict()

    def add_mapped_value(self, name, value):
        if isinstance(value, int):
            type = 'int'
        elif isinstance(value, float):
            type = 'float'
        elif isinstance(value, Vector3):
            type = 'vec3'
        else:
            type = False

        if type:
            name = type + '_' + name
        self._map.update({name: value})

    def get_mapped_value(self, name, type=None):
        if type:
            name = type + '_' + name
        result = self._map.get(name)
        if result is not None:
            return result

        if type == 'int':
            return 0
        elif type == 'float':
            return 0.
        elif type == 'vec3':
            return Vector3()
        else:
            return False
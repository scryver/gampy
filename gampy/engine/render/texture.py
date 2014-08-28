__author__ = 'michiel'

import OpenGL.GL as gl
import uuid
from PIL import Image
import numpy
import os.path
import gampy.engine.render.resourcemanagement as resourcemanagement

class Texture:

    loaded_textures = dict()

    def __init__(self, texture, tex_target=gl.GL_TEXTURE_2D, filters=None, internal_format=gl.GL_RGBA,
                 format=gl.GL_RGBA, clamp=False, attachments=None):
        self.resource = None
        self._filename = None

        if isinstance(texture, str):
            """A file has been passed in"""
            old_resource = Texture.loaded_textures.get(texture, False)
            self._filename = texture
            if old_resource:
                self.resource = old_resource
                self.resource.add_reference()
            else:
                self.resource = Texture._load_texture(texture, tex_target, filters, attachments, clamp)
                Texture.loaded_textures.update({texture: self.resource})
        elif isinstance(texture, tuple):
            width, height, data = texture
            self._filename = uuid.uuid4()
            self.resource = resourcemanagement.TextureResource(width, height, 1, data, filters, internal_format, format, tex_target, attachments, clamp)
            Texture.loaded_textures.update({self._filename: self.resource})
        else:
            raise TypeError('Texture "{tex}" not supported'.format(tex=texture))

    def bind(self, sampler_slot):
        assert isinstance(sampler_slot, int) and sampler_slot >= 0 and sampler_slot < 32
        gl.glActiveTexture(gl.GL_TEXTURE0 + sampler_slot)
        self.resource.bind(0)

    def __del__(self):
        if self.resource.remove_reference() and self._filename is not None:
            Texture.loaded_textures.pop(self._filename)

    @classmethod
    def unbind(cls):
        gl.glBindTexture(gl.GL_TEXTURE_2D, 0)

    @classmethod
    def _load_texture(cls, texture_name: str, tex_target, filters, attachments, clamp):
        # http://pyopengl.sourceforge.net/context/tutorials/nehe6.html

        img = Image.open(os.path.join(os.path.dirname(__file__), '..', '..', 'res', 'textures', texture_name)) # .jpg, .bmp, etc. also work
        return cls._load_texture_from_image(img, tex_target, filters, attachments, clamp)

    @classmethod
    def _load_texture_from_image(cls, image, tex_target, filters, attachments, clamp, flip=True, internal_format=gl.GL_RGBA,
                 format=gl.GL_RGBA):
        if image.mode == 'P':
            image = image.convert('RGB')

        img_data = numpy.array(list(image.getdata()), numpy.int16)
        if flip:
            img_data = img_data[::-1]
        components, format = resourcemanagement.getLengthFormat(image)

        texture = resourcemanagement.TextureResource(image.size[0], image.size[1], 1, img_data, filters, components, format, tex_target, attachments, clamp)

        return texture

    def bind_as_render_target(self):
        self.resource.bind_as_render_target()
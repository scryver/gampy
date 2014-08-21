__author__ = 'michiel'

import OpenGL.GL as gl
from PIL import Image
import numpy
import os.path
import numbers
from gampy.engine.render.resourcemanagement import TextureResource

class Texture:

    loaded_textures = dict()

    def __init__(self, texture):
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
                self.resource = TextureResource(Texture._load_texture(texture))
                Texture.loaded_textures.update({texture: self.resource})
        else:
            self.resource = TextureResource(Texture._load_texture(texture))

    def bind(self):
        gl.glBindTexture(gl.GL_TEXTURE_2D, self.resource.id)

    def __del__(self):
        if self.resource.remove_reference() and self._filename is not None:
            Texture.loaded_textures.pop(self._filename)

    @classmethod
    def unbind(cls):
        gl.glBindTexture(gl.GL_TEXTURE_2D, 0)

    @classmethod
    def _load_texture(cls, texture_name: str):
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

        img = Image.open(os.path.join(os.path.dirname(__file__), '..', '..', 'res', 'textures', texture_name)) # .jpg, .bmp, etc. also work
        if img.mode == 'P':
            img = img.convert('RGB')
        img_data = numpy.array(list(img.getdata()), numpy.int8)[::-1]
        components, format = getLengthFormat(img)

        texture = gl.glGenTextures(1)
        gl.glBindTexture(gl.GL_TEXTURE_2D, texture)

        gl.glTexParameterf(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_WRAP_S, gl.GL_REPEAT)        # Repeat texture in x and y
        gl.glTexParameterf(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_WRAP_T, gl.GL_REPEAT)
        gl.glTexParameterf(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MIN_FILTER, gl.GL_LINEAR)    # Linear filter for colors
        gl.glTexParameterf(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_LINEAR)

        gl.glTexImage2D(gl.GL_TEXTURE_2D, 0, components, img.size[0], img.size[1], 0, format, gl.GL_UNSIGNED_BYTE, img_data)

        return texture



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
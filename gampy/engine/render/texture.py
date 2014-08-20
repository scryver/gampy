__author__ = 'michiel'

import OpenGL.GL as gl
from PIL import Image
import numpy
import os.path
import numbers

class Texture:

    def __init__(self, texture):
        if isinstance(texture, numbers.Number):
            id = texture
        elif isinstance(texture, str):
            id = Texture._load_texture(texture)
        else:
            raise AttributeError('Texture is not a file or number')
        self._id = id

    def bind(self):
        gl.glBindTexture(gl.GL_TEXTURE_2D, self._id)

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
        # gl.glPixelStorei(gl.GL_UNPACK_ALIGNMENT,1)        # Don't know why
        # gl.glPixelStorei(gl.GL_PACK_ALIGNMENT,1)          # Don't know why
        gl.glBindTexture(gl.GL_TEXTURE_2D, texture)
        gl.glTexParameterf(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_WRAP_S, gl.GL_CLAMP)         # Don't know why
        gl.glTexParameterf(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_WRAP_T, gl.GL_CLAMP)         # Don't know why
        gl.glTexParameterf(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_NEAREST)    # Don't know why
        gl.glTexParameterf(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MIN_FILTER, gl.GL_NEAREST)    # Don't know why
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
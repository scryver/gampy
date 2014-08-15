__author__ = 'michiel'

import OpenGL.GL as gl


class Texture:

    def __init__(self, id):
        self._id = id

    def bind(self):

        gl.glBindTexture(gl.GL_TEXTURE_2D, self._id)
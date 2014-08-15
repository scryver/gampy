__author__ = 'michiel'

import OpenGL.GL as gl


def clear_screen():
    # todo: Add stencil buffer
    gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)


def set_clear_color(color):
    gl.glClearColor(color.x, color.y, color.z, 1.0)


def init_graphics():
    gl.glClearColor(0., 0., 0., 0.)
    #
    # do not render backfacing faces and front is determined by clockwise
    gl.glFrontFace(gl.GL_CW)
    gl.glCullFace(gl.GL_BACK)
    gl.glEnable(gl.GL_CULL_FACE)

    # let open gl test the depth for new objects
    gl.glClearDepth(1.0)
    gl.glDepthFunc(gl.GL_LESS)
    gl.glEnable(gl.GL_DEPTH_TEST)

    gl.glEnable(gl.GL_DEPTH_CLAMP)

    gl.glEnable(gl.GL_TEXTURE_2D)
    # Gamma correction so linear colors can be used (instead of exponential)
    # gl.glEnable(gl.GL_FRAMEBUFFER_SRGB)

    # gl.glMatrixMode(gl.GL_PROJECTION | gl.GL_MODELVIEW)
    # gl.glLoadIdentity()
    # gl.glOrtho(-1, 1, -1, 1, 0.1, 1)
    # gl.glFrustum(-1, 1, -1, 1, 0.1, 1)


def get_open_gl_version():
    return gl.glGetString(gl.GL_VERSION)


def set_textures(enabled=False):
    if enabled:
        gl.glEnable(gl.GL_TEXTURE_2D)
    else:
        gl.glDisable(gl.GL_TEXTURE_2D)

def unbind_textures():
    gl.glBindTexture(gl.GL_TEXTURE_2D, 0)
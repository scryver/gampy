__author__ = 'michiel'

import OpenGL.GL as gl


def clear_screen():
    # todo: Add stencil buffer
    gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)


def init_graphics():
    gl.glClearColor(0., 0., 0., 0.)

    # do not render backfacing faces and front is determined by clockwise
    gl.glFrontFace(gl.GL_CW)
    gl.glCullFace(gl.GL_BACK)
    gl.glEnable(gl.GL_CULL_FACE)
    # let open gl test the depth for new objects
    gl.glEnable(gl.GL_DEPTH_TEST)

    # todo: Depth Clamp

    # Gamma correction so linear colors can be used (instead of exponential)
    gl.glEnable(gl.GL_FRAMEBUFFER_SRGB)
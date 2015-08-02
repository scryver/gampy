__author__ = 'michiel'

import OpenGL.GL as gl
from gampy.engine.events.time import Timing

timings = Timing('Render Util')


@timings
def clear_screen():
    # todo: Add stencil buffer
    gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)


@timings
def render():
    gl.glFlush()
    gl.glFinish()


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

    # todo: Depth Clamp

    # Gamma correction so linear colors can be used (instead of exponential)
    gl.glEnable(gl.GL_FRAMEBUFFER_SRGB)
    gl.glMatrixMode(gl.GL_PROJECTION | gl.GL_MODELVIEW)
    gl.glLoadIdentity()
    # gl.glOrtho(-1, 1, -1, 1, 0.1, 1)
    # gl.glFrustum(-1, 1, -1, 1, 0.1, 1)


def get_open_gl_version():
    return gl.glGetString(gl.GL_VERSION)

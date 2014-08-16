__author__ = 'michiel'


from gampy.engine.core.gameobject import GameObject
from gampy.engine.render.shader import BasicShader
import OpenGL.GL as gl

class RenderingEngine:

    def __init__(self):
        print(RenderingEngine.get_open_gl_version())
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

    def render(self, object):
        if not isinstance(object, GameObject):
            raise AttributeError('Cannot render other things then Game Objects')

        self._clear_screen()
        object.render(BasicShader.get_instance())

    @classmethod
    def _clear_screen(cls):
        # todo: Add stencil buffer
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)

    @classmethod
    def _set_clear_color(cls, color):
        gl.glClearColor(color.x, color.y, color.z, 1.0)

    @classmethod
    def get_open_gl_version(cls):
        return gl.glGetString(gl.GL_VERSION)

    @classmethod
    def _set_textures(cls, enabled=False):
        if enabled:
            gl.glEnable(gl.GL_TEXTURE_2D)
        else:
            gl.glDisable(gl.GL_TEXTURE_2D)
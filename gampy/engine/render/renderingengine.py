__author__ = 'michiel'

from gampy.engine.core.coreengine import Window
from gampy.engine.core.vectors import Vector3
from gampy.engine.render.camera import Camera
import gampy.engine.render.forwardpass as forward_pass
import OpenGL.GL as gl
import math

class RenderingEngine:

    def __init__(self):
        print(RenderingEngine.get_open_gl_version())
        gl.glClearColor(0., 0., 0., 0.)

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

        self.main_camera = Camera(math.radians(70.), Window.width / Window.height, 0.1, 1000.)
        self.active_ambient_light = Vector3(0.1, 0.1, 0.1)

        self.lights = []
        self.active_light = None

    def add_light(self, light):
        self.lights.append(light)

    def input(self, dt):
        self.main_camera.input(dt)

    def render(self, object):
        self._clear_screen()

        self.lights.clear()
        object.add_to_render_engine(self)

        forwardAmbient = forward_pass.Ambient.get_instance()
        forwardAmbient.render_engine = self
        object.render(forwardAmbient)

        # Add colors together (will be disabled through gl.glDisable(gl.GL_BLEND)
        gl.glEnable(gl.GL_BLEND)
        # One * color1 + One * color2
        gl.glBlendFunc(gl.GL_ONE, gl.GL_ONE)
        # We don't need to check the depth again (already done by ambient light)
        gl.glDepthMask(gl.GL_FALSE)
        # Only add color if the pixel is same as previous
        gl.glDepthFunc(gl.GL_EQUAL)

        object_render = object.render
        [object_render(shader) for shader in self._render_lights()]

        gl.glDepthFunc(gl.GL_LESS)
        gl.glDepthMask(gl.GL_TRUE)
        gl.glDisable(gl.GL_BLEND)

    def _render_lights(self):
        for light in self.lights:
            light.shader.render_engine = self
            self.active_light = light
            yield light.shader

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
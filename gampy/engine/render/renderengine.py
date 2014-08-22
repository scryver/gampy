__author__ = 'michiel'

import OpenGL.GL as gl

from gampy.engine.core.vectors import Vector3
import gampy.engine.core.time as timing
from gampy.engine.render.resourcemanagement import MappedValue
from gampy.engine.render.shader import Shader

timer = timing.Timing()


class RenderEngine(MappedValue):

    @timer
    def __init__(self):
        super().__init__()

        self.main_camera = None

        self.lights = []
        self.active_light = None
        self._forward_ambient = Shader('forward_ambient')
        self._sampler_map = {'diffuse': 0, 'normal': 1}
        self._map = dict()
        self.add_mapped_value('ambient', Vector3(0.1, 0.1, 0.1))

        print(RenderEngine.open_gl_version())
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

    @timer
    def add_light(self, light):
        self.lights.append(light)

    @timer
    def add_camera(self, camera):
        self.main_camera = camera

    def update_uniform_struct(self, transform, material, shader, uniform_name, uniform_type):
        raise NotImplementedError('Set invalid rendering uniform type "{}" with name "{}"'.format(uniform_type, uniform_name))

    @timer
    def render(self, object):
        # todo: Add stencil buffer
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)

        object.render(self._forward_ambient, self)

        # Add colors together (will be disabled through gl.glDisable(gl.GL_BLEND)
        gl.glEnable(gl.GL_BLEND)
        # One * color1 + One * color2
        gl.glBlendFunc(gl.GL_ONE, gl.GL_ONE)
        # We don't need to check the depth again (already done by ambient light)
        gl.glDepthMask(gl.GL_FALSE)
        # Only add color if the pixel is same as previous
        gl.glDepthFunc(gl.GL_EQUAL)

        object_render = object.render
        [object_render(shader, self) for shader in self._render_lights()]

        gl.glDepthFunc(gl.GL_LESS)
        gl.glDepthMask(gl.GL_TRUE)
        gl.glDisable(gl.GL_BLEND)

    def sampler_slot(self, sampler_name: str):
        return self._sampler_map[sampler_name]

    @timer
    def _render_lights(self):
        for light in self.lights:
            self.active_light = light
            yield light.shader

    @classmethod
    @timer
    def open_gl_version(cls):
        return gl.glGetString(gl.GL_VERSION)

    @classmethod
    @timer
    def _set_textures(cls, enabled=False):
        if enabled:
            gl.glEnable(gl.GL_TEXTURE_2D)
        else:
            gl.glDisable(gl.GL_TEXTURE_2D)

    def __del__(self):
        print('========RENDER ENGINE================================================================',
              timer,
              '=====================================================================================', sep='\n')
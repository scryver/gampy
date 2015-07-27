__author__ = 'michiel'

import OpenGL.GL as gl

from gampy.engine.core.math3d import Vector3, Matrix4
from gampy.engine.render.mapper import MappedValue
from gampy.engine.render.shader import Shader
from gampy.engine.tkinter.window import Window
import gampy.engine.core.time as timing


timer = timing.Timing()


class RenderEngine(MappedValue):

    @timer
    def __init__(self):
        super().__init__()
        self._sampler_map = {'diffuse': 0, 'normalMap': 1, 'dispMap': 2}

        self.set_mapped_value('ambient', Vector3(0.2, 0.2, 0.2))
        self._forward_ambient = Shader('forward_ambient')

        print('OpenGL version: ', RenderEngine.open_gl_version())
        gl.glClearColor(0., 0., 0., 0.)

        self.main_camera = None
        self.lights = []
        self.light_matrix = Matrix4().init_identity()
        self.active_light = None

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
        Window.bind_as_render_target()
        camera_view = self.main_camera.view_projection()
        camera_pos = self.main_camera.transform.transformed_position()

        gl.glClearColor(0., 0., 0., 0.)
        # todo: Add stencil buffer
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)

        [obj.render(self._forward_ambient, self, camera_view, camera_pos) for obj in object.all_generator()]

        gl.glEnable(gl.GL_BLEND)                # Add colors together (will be disabled through gl.glDisable(gl.GL_BLEND)
        gl.glBlendFunc(gl.GL_ONE, gl.GL_ONE)    # One * color1 + One * color2
        gl.glDepthMask(gl.GL_FALSE)             # We don't need to check the depth again (already done by ambient light)
        gl.glDepthFunc(gl.GL_EQUAL)             # Only add color if the pixel is same as previous

        # object_render = object.render_all
        [[obj.render(light.shader, self, camera_view, camera_pos) for obj in object.all_generator()]
            for light in self._render_lights()]

        gl.glDepthMask(gl.GL_TRUE)
        gl.glDepthFunc(gl.GL_LESS)
        gl.glDisable(gl.GL_BLEND)

    def sampler_slot(self, sampler_name: str):
        return self._sampler_map[sampler_name]

    @timer
    def _render_lights(self):
        for light in self.lights:
            self.active_light = light
            yield light

    @classmethod
    # @timer
    def open_gl_version(cls):
        return gl.glGetString(gl.GL_VERSION).decode()

    def __del__(self):
        print('========RENDER ENGINE================================================================',
              timer,
              '=====================================================================================', sep='\n')
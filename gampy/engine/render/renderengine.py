__author__ = 'michiel'

import OpenGL.GL as gl

from gampy.engine.core.vectors import Vector3, Matrix4, Quaternion
from gampy.engine.render.resourcemanagement import MappedValue
from gampy.engine.tkinter.window import Window
from gampy.engine.render.shader import Shader
# Temp imports
from gampy.engine.render.meshes import Mesh
from gampy.engine.core.transform import Transform
from gampy.engine.render.material import Material
from gampy.engine.render.texture import Texture
from gampy.engine.components.camera import Camera
from gampy.engine.core.gameobject import GameObject
import math
# import gampy.engine.core.time as timing

# timer = timing.Timing()


class RenderEngine(MappedValue):

    # @timer
    def __init__(self):
        super().__init__()
        # Temp vars
        # self.temp_target = Texture((Window.width, Window.height, None), gl.GL_TEXTURE_2D, gl.GL_NEAREST, None,
        #                            None, False, gl.GL_COLOR_ATTACHMENT0)
        # self.mesh = Mesh('plane.obj')
        # self.material = Material(self.temp_target, 1., 8.)
        # self.transform = Transform()
        # self.transform.scale = 0.9
        # self.transform.rotate(Vector3(1, 0, 0), math.radians(90))
        # self.transform.rotate(Vector3(0, 0, 1), math.radians(180))
        # self.camera = Camera(Matrix4().init_identity())
        # self.camera_obj = GameObject().add_component(self.camera)
        # self.camera.transform.rotate(Vector3(0, 1, 0), math.radians(180.))

        self.main_camera = None

        self.lights = []
        self.active_light = None
        self._forward_ambient = Shader('forward_ambient')
        self._sampler_map = {'diffuse': 0, 'normalMap': 1, 'dispMap': 2}
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

    # @timer
    def add_light(self, light):
        self.lights.append(light)

    # @timer
    def add_camera(self, camera):
        self.main_camera = camera

    def update_uniform_struct(self, transform, material, shader, uniform_name, uniform_type):
        raise NotImplementedError('Set invalid rendering uniform type "{}" with name "{}"'.format(uniform_type, uniform_name))

    # @timer
    def render(self, object):
        Window.bind_as_render_target()
        # self.temp_target.bind_as_render_target()
        # gl.glClearColor(0., 0., 0., 0.)

        # todo: Add stencil buffer
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
        camera_view = self.main_camera.view_projection()
        camera_pos = self.main_camera.transform.transformed_position()

        object.render_all(self._forward_ambient, self, camera_view, camera_pos)

        # Add colors together (will be disabled through gl.glDisable(gl.GL_BLEND)
        gl.glEnable(gl.GL_BLEND)
        # One * color1 + One * color2
        gl.glBlendFunc(gl.GL_ONE, gl.GL_ONE)
        # We don't need to check the depth again (already done by ambient light)
        gl.glDepthMask(gl.GL_FALSE)
        # Only add color if the pixel is same as previous
        gl.glDepthFunc(gl.GL_EQUAL)

        object_render = object.render_all
        [object_render(shader, self, camera_view, camera_pos) for shader in self._render_lights()]

        gl.glDepthFunc(gl.GL_LESS)
        gl.glDepthMask(gl.GL_TRUE)
        gl.glDisable(gl.GL_BLEND)

        # TEMP RENDER
        # Window.bind_as_render_target()
        #
        # temp = self.main_camera
        # self.main_camera = self.camera
        #
        # gl.glClearColor(0., 0., 0.5, 1.)
        # gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
        # self._forward_ambient.bind()
        # self._forward_ambient.update_uniforms(self.transform, self.material, self, self.main_camera.view_projection(), self.main_camera.transform.transformed_position())
        # try:
        #     self.mesh.draw()
        # finally:
        #     self._forward_ambient.unbind()
        # self.main_camera = temp

    def sampler_slot(self, sampler_name: str):
        return self._sampler_map[sampler_name]

    # @timer
    def _render_lights(self):
        for light in self.lights:
            self.active_light = light
            yield light.shader

    @classmethod
    # @timer
    def open_gl_version(cls):
        return gl.glGetString(gl.GL_VERSION)

    @classmethod
    # @timer
    def _set_textures(cls, enabled=False):
        if enabled:
            gl.glEnable(gl.GL_TEXTURE_2D)
        else:
            gl.glDisable(gl.GL_TEXTURE_2D)

    # def __del__(self):
    #     print('========RENDER ENGINE================================================================',
    #           timer,
    #           '=====================================================================================', sep='\n')
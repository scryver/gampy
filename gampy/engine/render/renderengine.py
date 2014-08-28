__author__ = 'michiel'

import OpenGL.GL as gl

from gampy.engine.core.vectors import Vector3, Matrix4, Quaternion
from gampy.engine.render.mapper import MappedValue
from gampy.engine.render.shader import Shader
# Temp imports
from gampy.engine.tkinter.window import Window
from gampy.engine.render.meshes import Mesh
from gampy.engine.render.material import Material
from gampy.engine.core.transform import Transform
from gampy.engine.render.texture import Texture
from gampy.engine.components.camera import Camera
from gampy.engine.core.gameobject import GameObject
import math
import gampy.engine.core.time as timing

timer = timing.Timing()


class RenderEngine(MappedValue):

    bias_matrix = Matrix4().init_scale(.5, .5, .5) * Matrix4().init_translation(1, 1, 1)

    @timer
    def __init__(self):
        super().__init__()
        self._sampler_map = {'diffuse': 0, 'normalMap': 1, 'dispMap': 2, 'shadowMap': 3}

        self.set_mapped_value('ambient', Vector3(0.1, 0.1, 0.1))
        self.set_mapped_value('shadowMap', Texture((1024, 1024, None), gl.GL_TEXTURE_2D,gl.GL_NEAREST,
                                                   gl.GL_DEPTH_COMPONENT, gl.GL_DEPTH_COMPONENT, True,
                                                   gl.GL_DEPTH_ATTACHMENT))
        self._forward_ambient = Shader('forward_ambient')
        self._shadow_map_shader = Shader('shadow_map_generator')

        print(RenderEngine.open_gl_version())
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

        self._alt_camera = Camera(Matrix4().init_identity())
        self._alt_camera_obj = GameObject().add_component(self._alt_camera)
        self._alt_camera_obj.transform.rotate(Vector3(0, 1, 0), math.radians(180.))
        self._temp_target = Texture((Window.width, Window.height, None), filters=gl.GL_NEAREST, attachments=gl.GL_COLOR_ATTACHMENT0)
        self._plane_material = Material(self._temp_target)
        self._plane = Mesh('plane.obj')
        self._plane_transform = Transform()
        self._plane_transform.scale = 1.
        self._plane_transform.rotate(Vector3(1, 0, 0), math.radians(90))
        self._plane_transform.rotate(Vector3(0, 0, 1), math.radians(180))

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

        objects = object.all_attached()

        [obj.render(self._forward_ambient, self, camera_view, camera_pos) for obj in objects]

        texture = self.get_mapped_value('shadowMap', 'tex')
        for light in self._render_lights():
            shadow_info = light.shadow_info

            #switching of this target makes the screen flikker
            texture.bind_as_render_target()

            gl.glClearColor(0., 0., 0., 0.)
            # todo: Add stencil buffer
            gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)

            if shadow_info:
                # gl.glPushAttrib(gl.GL_VIEWPORT_BIT)
                self._alt_camera.projection = shadow_info.projection
                self._alt_camera.transform.position = light.transform.transformed_position()
                self._alt_camera.transform.rotation = light.transform.transformed_rotation()
                alt_camera_view = self._alt_camera.view_projection()
                alt_camera_pos = self._alt_camera.transform.transformed_position()

                self.light_matrix = RenderEngine.bias_matrix * alt_camera_view

                self.set_mapped_value('shadowTexelSize', Vector3(1/1024, 1/1024, 0.))
                self.set_mapped_value('shadowBias', shadow_info.bias/1024)
                flip_faces = shadow_info.flip_faces

                temp = self.main_camera
                self.main_camera = self._alt_camera

                if flip_faces: gl.glCullFace(gl.GL_FRONT)
                [obj.render(self._shadow_map_shader, self, alt_camera_view, alt_camera_pos) for obj in objects]
                if flip_faces: gl.glCullFace(gl.GL_BACK)

                self.main_camera = temp
                # gl.glPopAttrib()

            Window.bind_as_render_target()

            gl.glEnable(gl.GL_BLEND)                # Add colors together (will be disabled through gl.glDisable(gl.GL_BLEND)
            gl.glBlendFunc(gl.GL_ONE, gl.GL_ONE)    # One * color1 + One * color2
            gl.glDepthMask(gl.GL_FALSE)             # We don't need to check the depth again (already done by ambient light)
            gl.glDepthFunc(gl.GL_EQUAL)             # Only add color if the pixel is same as previous

            # object_render = object.render_all
            [obj.render(light.shader, self, camera_view, camera_pos) for obj in objects]

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
        return gl.glGetString(gl.GL_VERSION)

    def __del__(self):
        print('========RENDER ENGINE================================================================',
              timer,
              '=====================================================================================', sep='\n')
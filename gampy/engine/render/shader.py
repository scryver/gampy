__author__ = 'michiel'

import OpenGL.GL as gl
from gampy.engine.objects.vectors import Vector3, Matrix4
from gampy.engine.objects.util import cast_matrix
from gampy.engine.render.util import unbind_textures
import gampy.engine.render.lights as lights
import os.path

class ShaderException(Exception):

    def __init__(self, message='ERROR'):
        message = '\nShader Exception: ' + str(message)
        super(ShaderException, self).__init__(message)


class ShaderCreateError(ShaderException):

    def __init__(self, message='ERROR'):
        message = '\n\tShader Creation Failed: ' + str(message)
        super(ShaderCreateError, self).__init__(message)


class ShaderCompileError(ShaderException):

    def __init__(self, message='ERROR'):
        message = '\n\tShader Compile Failed: ' + str(message)
        super(ShaderCompileError, self).__init__(message)


class UniformAddError(ShaderException):

    def __init__(self, message='ERROR'):
        message = '\n\tUniform Add Failed: ' + str(message)
        super(UniformAddError, self).__init__(message)


class Shader:

    def __init__(self):
        self.program = gl.glCreateProgram()
        self.uniforms = dict()

        if self.program == 0:
            raise ShaderCreateError('Could not find valid memory location in constructor')

    def bind(self):
        gl.glUseProgram(self.program)

    def unbind(self):
        gl.glUseProgram(0)

    def update_uniforms(self, world_matrix, projected_matrix, camera, material):
        pass

    def add_uniform(self, uniform):
        uniform_location = gl.glGetUniformLocation(self.program, uniform)

        if uniform_location == -1:
            raise UniformAddError('Could not find uniform "{}"'.format(uniform))

        updateDict = { uniform: uniform_location }
        self.uniforms.update(updateDict)

    def add_vertex_shader(self, text):
        self._add_program(text, gl.GL_VERTEX_SHADER)

    def add_geometry_shader(self, text):
        self._add_program(text, gl.GL_GEOMETRY_SHADER)

    def add_fragment_shader(self, text):
        self._add_program(text, gl.GL_FRAGMENT_SHADER)

    def compile_shader(self):
        gl.glLinkProgram(self.program)

        if gl.glGetProgramiv(self.program, gl.GL_LINK_STATUS) == 0:
            raise ShaderCompileError(gl.glGetProgramInfoLog(self.program))

        gl.glValidateProgram(self.program)

        if gl.glGetProgramiv(self.program, gl.GL_VALIDATE_STATUS) == 0:
            raise ShaderCompileError(gl.glGetProgramInfoLog(self.program))

    def _add_program(self, text, type):
        shader = gl.glCreateShader(type)

        if shader == 0:
            raise ShaderCreateError('Could not find valid memory location when adding shader')

        gl.glShaderSource(shader, text)
        gl.glCompileShader(shader)

        if gl.glGetShaderiv(shader, gl.GL_COMPILE_STATUS) == 0:
            raise ShaderCreateError(gl.glGetShaderInfoLog(shader))

        gl.glAttachShader(self.program, shader)

    def set_uniform(self, uniform, value):
        if uniform in self.uniforms.keys():
            if isinstance(value, int):
                gl.glUniform1i(self.uniforms.get(uniform), value)
            elif isinstance(value, float):
                gl.glUniform1f(self.uniforms.get(uniform), value)
            elif isinstance(value, Vector3):
                gl.glUniform3f(self.uniforms.get(uniform), value.x, value.y, value.z)
            elif isinstance(value, Matrix4):
                gl.glUniformMatrix4fv(self.uniforms.get(uniform), 1, True, cast_matrix(value))
            else:
                raise AttributeError('Value "{}" is not an int, float, Vector3 or Matrix'.format(value))
        else:
            raise AttributeError('Uniform "{}" is not added to the list'.format(uniform))

    @classmethod
    def load_shader(cls, file_name, type='vertex'):
        shader = ''
        with open(os.path.join(os.path.dirname(__file__), '..', '..', 'res', 'shaders', type, file_name), 'r', 1) as file:
            for line in file:
                shader += line + '\n'

            file.close()

        return shader


class BasicShader(Shader):

    def __init__(self):
        super(BasicShader, self).__init__()

        self.add_vertex_shader(BasicShader.load_shader('basic_vertex.vs', 'vertex'))
        self.add_fragment_shader(BasicShader.load_shader('basic_fragment.fs', 'fragment'))
        self.compile_shader()

        self.add_uniform('transform')
        self.add_uniform('color')

    def update_uniforms(self, world_matrix, projected_matrix, camera, material):
        if material.texture is not None:
            material.texture.bind()
        else:
            unbind_textures()

        self.set_uniform('transform', projected_matrix)
        self.set_uniform('color', material.color)


class PhongShader(Shader):

    MAX_POINT_LIGHTS = 4
    MAX_SPOT_LIGHTS = 4

    ambient_light = Vector3(0.1, 0.1, 0.1)
    directional_light = lights.DirectionalLight(lights.BaseLight(Vector3(1, 1, 1), 0.), Vector3(0, 0, 0))
    point_lights = []
    spot_lights = []

    def __init__(self):
        super(PhongShader, self).__init__()
        self.add_vertex_shader(PhongShader.load_shader('phong_vertex.vs', 'vertex'))
        self.add_fragment_shader(PhongShader.load_shader('phong_fragment.fs', 'fragment'))
        self.compile_shader()

        self.add_uniform('transform')
        self.add_uniform('transformProjected')
        self.add_uniform('cameraPos')

        self.add_uniform('baseColor')
        self.add_uniform('specularIntensity')
        self.add_uniform('specularExponent')

        self.add_uniform('ambientLight')

        self.add_uniform('directionalLight.base.color')
        self.add_uniform('directionalLight.base.intensity')
        self.add_uniform('directionalLight.direction')

        for i in range(PhongShader.MAX_POINT_LIGHTS):
            self.add_uniform('pointLights[{i}].base.color'.format(i=i))
            self.add_uniform('pointLights[{i}].base.intensity'.format(i=i))
            self.add_uniform('pointLights[{i}].attenuation.constant'.format(i=i))
            self.add_uniform('pointLights[{i}].attenuation.linear'.format(i=i))
            self.add_uniform('pointLights[{i}].attenuation.exponent'.format(i=i))
            self.add_uniform('pointLights[{i}].position'.format(i=i))
            self.add_uniform('pointLights[{i}].range'.format(i=i))

        for i in range(PhongShader.MAX_SPOT_LIGHTS):
            self.add_uniform('spotLights[{i}].pointLight.base.color'.format(i=i))
            self.add_uniform('spotLights[{i}].pointLight.base.intensity'.format(i=i))
            self.add_uniform('spotLights[{i}].pointLight.attenuation.constant'.format(i=i))
            self.add_uniform('spotLights[{i}].pointLight.attenuation.linear'.format(i=i))
            self.add_uniform('spotLights[{i}].pointLight.attenuation.exponent'.format(i=i))
            self.add_uniform('spotLights[{i}].pointLight.position'.format(i=i))
            self.add_uniform('spotLights[{i}].pointLight.range'.format(i=i))
            self.add_uniform('spotLights[{i}].direction'.format(i=i))
            self.add_uniform('spotLights[{i}].cutoff'.format(i=i))

    def update_uniforms(self, world_matrix, projected_matrix, camera, material):
        if material.texture is not None:
            material.texture.bind()
        else:
            unbind_textures()

        self.set_uniform('transform', world_matrix)
        self.set_uniform('transformProjected', projected_matrix)
        self.set_uniform('cameraPos', camera.pos)

        self.set_uniform('baseColor', material.color)
        self.set_uniform('specularIntensity', material.specular_intensity)
        self.set_uniform('specularExponent', material.specular_exponent)

        self.set_uniform('ambientLight', PhongShader.ambient_light)
        self.set_uniform('directionalLight', PhongShader.directional_light)
        for i in range(len(PhongShader.point_lights)):
            self.set_uniform('pointLights[{i}]'.format(i=i), PhongShader.point_lights[i])
        for i in range(len(PhongShader.spot_lights)):
            self.set_uniform('spotLights[{i}]'.format(i=i), PhongShader.spot_lights[i])

    def set_uniform(self, uniform, value):
        try:
            super(PhongShader, self).set_uniform(uniform, value)
        except AttributeError:
            if next(v for k,v in self.uniforms.items() if k.startswith(uniform)):
                if isinstance(value, lights.DirectionalLight):
                    self.set_uniform(uniform + '.base', value.base)
                    self.set_uniform(uniform + '.direction', value.direction)
                elif isinstance(value, lights.BaseLight):
                    self.set_uniform(uniform + '.color', value.color)
                    self.set_uniform(uniform + '.intensity', value.intensity)
                elif isinstance(value, lights.PointLight):
                    self.set_uniform(uniform + '.base', value.base)
                    self.set_uniform(uniform + '.attenuation', value.attenuation)
                    self.set_uniform(uniform + '.position', value.position)
                    self.set_uniform(uniform + '.range', value.range)
                elif isinstance(value, lights.SpotLight):
                    self.set_uniform(uniform + '.pointLight', value.point_light)
                    self.set_uniform(uniform + '.direction', value.direction)
                    self.set_uniform(uniform + '.cutoff', value.cutoff)
                elif isinstance(value, lights.Attenuation):
                    self.set_uniform(uniform + '.constant', value.constant)
                    self.set_uniform(uniform + '.linear', value.linear)
                    self.set_uniform(uniform + '.exponent', value.exponent)
                else:
                    raise AttributeError('Value "{}" is not an int, float, Vector3 or Matrix'.format(value))
            else:
                raise AttributeError('Uniform "{}" is not added to the list'.format(uniform))

    @classmethod
    def set_point_lights(cls, point_lights):
        if len(point_lights) > cls.MAX_POINT_LIGHTS:
            raise AttributeError('To many point lights! You passed {amount} '
                                 'and the max is {max}'.format(amount=len(point_lights), max=cls.MAX_POINT_LIGHTS))

        cls.point_lights = point_lights

    @classmethod
    def set_spot_lights(cls, spot_lights):
        if len(spot_lights) > cls.MAX_SPOT_LIGHTS:
            raise AttributeError('To many spot lights! You passed {amount} '
                                 'and the max is {max}'.format(amount=len(spot_lights), max=cls.MAX_SPOT_LIGHTS))

        cls.spot_lights = spot_lights
__author__ = 'michiel'

import os.path
import OpenGL.GL as gl
import numpy
from gampy.engine.core.vectors import Vector3, Matrix4

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

    _instance = None

    def __init__(self):
        self.program = gl.glCreateProgram()
        self.uniforms = dict()

        if self.program == 0:
            raise ShaderCreateError('Could not find valid memory location in constructor')

    def bind(self):
        gl.glUseProgram(self.program)

    def unbind(self):
        gl.glUseProgram(0)

    def update_uniforms(self, transform, material, render_engine):
        pass

    def add_uniform(self, uniform):
        uniform_location = gl.glGetUniformLocation(self.program, uniform)

        if uniform_location == -1:
            raise UniformAddError('Could not find uniform "{}"'.format(uniform))

        updateDict = { uniform: uniform_location }
        self.uniforms.update(updateDict)

    def add_vertex_shader_from_file(self, text):
        self._add_program(Shader._load_shader(text, 'vertex'), gl.GL_VERTEX_SHADER)

    def add_geometry_shader_from_file(self, text):
        self._add_program(Shader._load_shader(text, 'geometry'), gl.GL_GEOMETRY_SHADER)

    def add_fragment_shader_from_file(self, text):
        self._add_program(Shader._load_shader(text, 'fragment'), gl.GL_FRAGMENT_SHADER)

    def add_vertex_shader(self, text):
        self._add_program(text, gl.GL_VERTEX_SHADER)

    def add_geometry_shader(self, text):
        self._add_program(text, gl.GL_GEOMETRY_SHADER)

    def add_fragment_shader(self, text):
        self._add_program(text, gl.GL_FRAGMENT_SHADER)

    def set_attribute_location(self, attribute_name, location):
        gl.glBindAttribLocation(self.program, location, attribute_name)

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
                gl.glUniformMatrix4fv(self.uniforms.get(uniform), 1, True, value.m.view(numpy.ndarray))
            else:
                raise AttributeError('Value "{}" is not an int, float, Vector3 or Matrix'.format(value))
        else:
            raise AttributeError('Uniform "{}" is not added to the list'.format(uniform))

    @classmethod
    def _load_shader(cls, file_name, type='vertex'):
        INCLUDE_DIRECTIVE = '#include'
        file_name = '{file}.glsl{ext}'.format(file=file_name, ext=type[0])
        shader_list = []
        with open(os.path.join(os.path.dirname(__file__), '..', '..', 'res', 'shaders', type, file_name), 'r', 1) as file:
            for line in file:
                if line.startswith(INCLUDE_DIRECTIVE):
                    shader_list.append(cls._load_shader(line[len(INCLUDE_DIRECTIVE) + 2:-6], 'headers'))
                else:
                    shader_list.append(line + '\n')

            file.close()

        return ''.join(shader_list)

    @classmethod
    def get_instance(cls):
        if not cls._instance:
            cls._instance = cls()
        return cls._instance
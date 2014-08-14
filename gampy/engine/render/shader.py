__author__ = 'michiel'

import OpenGL.GL as gl
from gampy.engine.objects.vectors import Vector3, Matrix4
from gampy.engine.objects.util import cast_matrix


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

    def add_uniform(self, uniform):
        uniform_location = gl.glGetUniformLocation(self.program, uniform)

        if uniform_location == -1:
            raise UniformAddError('Could not find uniform "{}"'.format(uniform))

        updateDict = { uniform: uniform_location }
        self.uniforms.update(updateDict)
        print(self.uniforms)

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
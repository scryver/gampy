__author__ = 'michiel'

import OpenGL.GL as gl
from OpenGL.GL import shaders


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


class Shader:

    def __init__(self):
        self.program = gl.glCreateProgram()

        if self.program == 0:
            raise ShaderCreateError('Could not find valid memory location in constructor')

    def bind(self):
        gl.glUseProgram(self.program)

    def unbind(self):
        gl.glUseProgram(0)

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
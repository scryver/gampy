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
    INCLUDE_DIRECTIVE = '#include'
    UNIFORM_KEYWORD = 'uniform'
    ATTRIBUTE_KEYWORD = 'attribute'
    STRUCT_KEYWORD = 'struct'

    def __init__(self, file_name):
        self.program = gl.glCreateProgram()
        self.uniforms = dict()

        vertex_shader_text = self._load_shader(file_name, 'vertex')
        fragment_shader_text = self._load_shader(file_name, 'fragment')

        self._add_vertex_shader(vertex_shader_text)
        self._add_fragment_shader(fragment_shader_text)

        self._add_all_attributes(vertex_shader_text)

        self._compile_shader()

        self._add_all_uniforms(vertex_shader_text)
        self._add_all_uniforms(fragment_shader_text)

        if self.program == 0:
            raise ShaderCreateError('Could not find valid memory location in constructor')

    def bind(self):
        gl.glUseProgram(self.program)

    def unbind(self):
        gl.glUseProgram(0)

    def update_uniforms(self, transform, material, render_engine):
        pass

    def _add_uniform(self, uniform):
        uniform_location = gl.glGetUniformLocation(self.program, uniform)

        if uniform_location == -1:
            raise UniformAddError('Could not find uniform "{}"'.format(uniform))

        updateDict = { uniform: uniform_location }
        self.uniforms.update(updateDict)

    def _add_all_attributes(self, shader_txt: str):
        attribute_start_location = shader_txt.find(Shader.ATTRIBUTE_KEYWORD)
        attribute_index = 0

        while attribute_start_location != -1:
            if not (attribute_start_location != 0 and (
                            shader_txt[attribute_start_location -1].isspace() or
                            shader_txt[attribute_start_location - 1] == ';'
                        ) and shader_txt[attribute_start_location + len(Shader.ATTRIBUTE_KEYWORD)].isspace()):
                continue

            begin = attribute_start_location + len(Shader.ATTRIBUTE_KEYWORD) + 1
            end = shader_txt.find(';', begin)

            attribute_line = shader_txt[begin:end].strip()
            attribute_type = attribute_line[:attribute_line.find(' ')].strip()
            attribute_name = attribute_line[attribute_line.find(' ') + 1:].strip()

            self._set_attribute_location(attribute_name, attribute_index)
            attribute_index += 1

            attribute_start_location = shader_txt.find(Shader.ATTRIBUTE_KEYWORD,
                                                       attribute_start_location + len(Shader.ATTRIBUTE_KEYWORD))

    def _find_uniform_structs(self, shader_txt: str):
        structs = dict()
        struct_start_location = shader_txt.find(Shader.STRUCT_KEYWORD)

        while struct_start_location != -1:
            if not (struct_start_location != 0 and (
                            shader_txt[struct_start_location -1].isspace() or
                            shader_txt[struct_start_location - 1] == ';'
                        ) and shader_txt[struct_start_location + len(Shader.STRUCT_KEYWORD)].isspace()):
                continue
            name_begin = struct_start_location + len(Shader.STRUCT_KEYWORD) + 1
            brace_begin = shader_txt.find('{', name_begin)
            brace_end = shader_txt.find('}', brace_begin)

            struct_name = shader_txt[name_begin:brace_begin].strip()
            struct_components = dict()

            component_semicolon_pos = shader_txt.find(';', brace_begin)
            while component_semicolon_pos != -1 and component_semicolon_pos < brace_end:
                comp_name_end = component_semicolon_pos + 1

                while shader_txt[comp_name_end - 1].isspace() or shader_txt[comp_name_end - 1] == ';':
                    comp_name_end -= 1

                comp_name_start = comp_name_end

                while not shader_txt[comp_name_start - 1].isspace():
                    comp_name_start -= 1

                comp_type_end = comp_name_start

                while shader_txt[comp_type_end - 1].isspace():
                    comp_type_end -= 1

                comp_type_start = comp_type_end

                while not shader_txt[comp_type_start - 1].isspace():
                    comp_type_start -= 1

                component_name = shader_txt[comp_name_start:component_semicolon_pos]
                component_type = shader_txt[comp_type_start:comp_type_end]
                struct_components.update({component_name: component_type})

                component_semicolon_pos = shader_txt.find(';', component_semicolon_pos + 1)

            structs.update({struct_name: struct_components})

            struct_start_location = shader_txt.find(Shader.STRUCT_KEYWORD,
                                                    struct_start_location + len(Shader.STRUCT_KEYWORD))

        return structs

    def _add_all_uniforms(self, shader_txt: str):
        structs = self._find_uniform_structs(shader_txt)
        uniform_start_location = shader_txt.find(Shader.UNIFORM_KEYWORD)

        while uniform_start_location != -1:
            if not (uniform_start_location != 0 and (
                            shader_txt[uniform_start_location -1].isspace() or
                            shader_txt[uniform_start_location - 1] == ';'
                        ) and shader_txt[uniform_start_location + len(Shader.UNIFORM_KEYWORD)].isspace()):
                continue

            begin = uniform_start_location + len(Shader.UNIFORM_KEYWORD) + 1
            end = shader_txt.find(';', begin)

            uniform_line = shader_txt[begin:end].strip()
            unif_name_end = end + 1

            while shader_txt[unif_name_end - 1].isspace() or shader_txt[unif_name_end - 1] == ';':
                unif_name_end -= 1

            unif_name_start = unif_name_end

            while not shader_txt[unif_name_start - 1].isspace():
                unif_name_start -= 1

            unif_type_end = unif_name_start

            while shader_txt[unif_type_end - 1].isspace():
                unif_type_end -= 1

            unif_type_start = unif_type_end

            while not shader_txt[unif_type_start - 1].isspace():
                unif_type_start -= 1

            uniform_type = uniform_line[unif_type_start:unif_type_end]
            uniform_name = uniform_line[unif_name_start:unif_name_end]

            self._add_uniform_with_struct_check(uniform_name, uniform_type, structs)

            uniform_start_location = shader_txt.find(Shader.UNIFORM_KEYWORD,
                                                     uniform_start_location + len(Shader.UNIFORM_KEYWORD))

    def _add_uniform_with_struct_check(self, uniform_name: str, uniform_type: str, structs: dict):
        add_this = True
        struct_components = structs.get(uniform_type)

        if struct_components is not None:
            add_this = False

            for name in struct_components:
                self._add_uniform_with_struct_check(uniform_name + '.' + name, struct_components[name], structs)

        if add_this:
            self._add_uniform(uniform_name)

    def _add_vertex_shader(self, text):
        self._add_program(text, gl.GL_VERTEX_SHADER)

    # def _add_geometry_shader(self, text):
    #     self._add_program(text, gl.GL_GEOMETRY_SHADER)

    def _add_fragment_shader(self, text):
        self._add_program(text, gl.GL_FRAGMENT_SHADER)

    def _set_attribute_location(self, attribute_name, location):
        gl.glBindAttribLocation(self.program, location, attribute_name)

    def _compile_shader(self):
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
        file_name = '{file}.glsl{ext}'.format(file=file_name, ext=type[0])
        shader_list = []
        with open(os.path.join(os.path.dirname(__file__), '..', '..', 'res', 'shaders', type, file_name), 'r', 1) as file:
            for line in file:
                if line.startswith(Shader.INCLUDE_DIRECTIVE):
                    shader_list.append(cls._load_shader(line[len(Shader.INCLUDE_DIRECTIVE) + 2:-6], 'headers'))
                else:
                    shader_list.append(line + '\n')

            file.close()

        return ''.join(shader_list)

    @classmethod
    def get_instance(cls):
        if not cls._instance:
            cls._instance = cls()
        return cls._instance
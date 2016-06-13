__author__ = 'michiel'

import os.path

import OpenGL.GL as gl
import numpy

from gampy.engine.core.math3d import Vector3, Matrix4
from gampy.engine.render.resourcemanagement import ShaderResource


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


import gampy.engine.core.time as timing

timer = timing.Timing()


class Shader:

    loaded_shaders = dict()

    _cache = dict()

    _instance = None
    INCLUDE_DIRECTIVE = '#include'
    UNIFORM_KEYWORD = 'uniform'
    ATTRIBUTE_KEYWORD = 'attribute'
    STRUCT_KEYWORD = 'struct'
    COMMENT_DIRECTIVE = '//'

    def __init__(self, file_name):
        self.resource = None
        self._filename = None

        old_resource = Shader.loaded_shaders.get(file_name, False)
        self._filename = file_name
        if old_resource:
            self.resource = old_resource
            self.resource.add_reference()
        else:
            self.resource = ShaderResource()

            vertex_shader_text = self._load_shader(file_name, 'vertex')
            fragment_shader_text = self._load_shader(file_name, 'fragment')

            self._add_vertex_shader(vertex_shader_text)
            self._add_fragment_shader(fragment_shader_text)

            self._add_all_attributes(vertex_shader_text)

            self._compile_shader()

            self._add_all_uniforms(vertex_shader_text)
            self._add_all_uniforms(fragment_shader_text)

            Shader.loaded_shaders.update({file_name: self.resource})

    def bind(self):
        gl.glUseProgram(self.resource.program)

    def unbind(self):
        gl.glUseProgram(0)

    @timer
    def _calc_vars(self, transform, camera_view):
        # update = False
        # if self._cache.get('transform', None) != transform:
        #     self._cache.update({'transform': transform})
        #     update = True
        # if self._cache.get('camera_view', None) != camera_view:
        #     self._cache.update({'camera_view': camera_view})
        #     update = True

        # if update:
        #     self._cache.update({
        #         'world': transform.transformation,
        #         'cam_world': camera_view * transform.transformation,
        #     })

        # return self._cache.get('world'), self._cache.get('cam_world')
        world = transform.transformation
        return world, camera_view * world

    @timer
    def update_uniforms(self, transform, material, render_engine, camera_view, camera_pos):
        world_matrix, MVP_matrix = self._calc_vars(transform, camera_view)
        for uniform_name in self.resource.uniform_names:
            type = self.resource.uniform_types[uniform_name]

            if uniform_name.startswith('R_'):
                name = uniform_name[2:]
                if name == 'lightMatrix':
                    self.set_uniform(uniform_name, render_engine.light_matrix * world_matrix)
                elif type == 'sampler2D':
                    sampler_slot = render_engine.sampler_slot(name)
                    render_engine.get_mapped_value(name, 'tex').bind(sampler_slot)
                    self.set_uniform(uniform_name, sampler_slot)
                elif type == 'vec3' or type == 'float':
                    self.set_uniform(uniform_name, render_engine.get_mapped_value(name, type))
                elif type == 'DirectionalLight':
                    self.set_uniform_dl(uniform_name, render_engine.active_light)
                elif type == 'PointLight':
                    self.set_uniform_pl(uniform_name, render_engine.active_light)
                elif type == 'SpotLight':
                    self.set_uniform_sl(uniform_name, render_engine.active_light)
                else:
                    render_engine.update_uniform_struct(transform, material, self, uniform_name, type)
            elif uniform_name.startswith('T_'):
                if uniform_name == 'T_MVP':
                    self.set_uniform(uniform_name, MVP_matrix)
                elif uniform_name == 'T_model':
                    self.set_uniform(uniform_name, world_matrix)
                else:
                    raise ShaderException('Set invalid transform uniform "{}"'.format(uniform_name))
            elif type == 'sampler2D':
                sampler_slot = render_engine.sampler_slot(uniform_name)
                material.get_mapped_value(uniform_name, 'tex').bind(sampler_slot)
                self.set_uniform(uniform_name, sampler_slot)
            elif uniform_name.startswith('C_'):
                if uniform_name == 'C_eyePosition':
                    self.set_uniform(uniform_name, camera_pos)
                else:
                    raise ShaderException('Set invalid camera uniform "{}"'.format(uniform_name))
            else:
                if type == 'vec3' or type == 'float':
                    self.set_uniform(uniform_name, material.get_mapped_value(uniform_name, type))
                else:
                    raise ShaderException('Set invalid material uniform type"{}" with name "{}"'.format(type, uniform_name))

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
            # attribute_type = attribute_line[:attribute_line.find(' ')].strip()
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
            unif_name_end = len(uniform_line)

            while uniform_line[unif_name_end - 1].isspace() or uniform_line[unif_name_end - 1] == ';':
                unif_name_end -= 1

            unif_name_start = unif_name_end

            while not uniform_line[unif_name_start - 1].isspace():
                unif_name_start -= 1

            unif_type_end = unif_name_start

            while uniform_line[unif_type_end - 1].isspace():
                unif_type_end -= 1

            unif_type_start = 0

            while uniform_line[unif_type_start].isspace():
                unif_type_start += 1

            uniform_type = uniform_line[unif_type_start:unif_type_end]
            uniform_name = uniform_line[unif_name_start:unif_name_end]

            self.resource.uniform_names.update({uniform_name: uniform_name})
            self.resource.uniform_types.update({uniform_name: uniform_type})
            self._add_uniform(uniform_name, uniform_type, structs)

            uniform_start_location = shader_txt.find(Shader.UNIFORM_KEYWORD,
                                                     uniform_start_location + len(Shader.UNIFORM_KEYWORD))

    def _add_uniform(self, uniform_name: str, uniform_type: str, structs: dict):
        add_this = True
        struct_components = structs.get(uniform_type)

        if struct_components is not None:
            add_this = False

            for name in struct_components:
                self._add_uniform(uniform_name + '.' + name, struct_components[name], structs)

        if not add_this:
            return

        uniform_location = gl.glGetUniformLocation(self.resource.program, uniform_name)

        if uniform_location == -1:
            raise UniformAddError('Could not find uniform "{}"'.format(uniform_name))

        self.resource.uniforms.update({uniform_name: uniform_location})

    def _add_vertex_shader(self, text):
        self._add_program(text, gl.GL_VERTEX_SHADER)

    # def _add_geometry_shader(self, text):
    #     self._add_program(text, gl.GL_GEOMETRY_SHADER)

    def _add_fragment_shader(self, text):
        self._add_program(text, gl.GL_FRAGMENT_SHADER)

    def _set_attribute_location(self, attribute_name, location):
        gl.glBindAttribLocation(self.resource.program, location, attribute_name)

    def _compile_shader(self):
        gl.glLinkProgram(self.resource.program)

        if gl.glGetProgramiv(self.resource.program, gl.GL_LINK_STATUS) == 0:
            raise ShaderCompileError(gl.glGetProgramInfoLog(self.resource.program))

        gl.glValidateProgram(self.resource.program)

        if gl.glGetProgramiv(self.resource.program, gl.GL_VALIDATE_STATUS) == 0:
            raise ShaderCompileError(gl.glGetProgramInfoLog(self.resource.program))

    def _add_program(self, text, type):
        shader = gl.glCreateShader(type)

        if shader == 0:
            raise ShaderCreateError('Could not find valid memory location when adding shader')

        gl.glShaderSource(shader, text)
        gl.glCompileShader(shader)

        if gl.glGetShaderiv(shader, gl.GL_COMPILE_STATUS) == 0:
            raise ShaderCreateError(gl.glGetShaderInfoLog(shader))

        gl.glAttachShader(self.resource.program, shader)

    @timer
    def set_uniform(self, uniform, value):
        if uniform in self.resource.uniforms.keys():
            if isinstance(value, int):
                gl.glUniform1i(self.resource.uniforms.get(uniform), value)
            elif isinstance(value, float):
                gl.glUniform1f(self.resource.uniforms.get(uniform), value)
            elif isinstance(value, Vector3):
                gl.glUniform3f(self.resource.uniforms.get(uniform), value.x, value.y, value.z)
            elif isinstance(value, Matrix4):
                gl.glUniformMatrix4fv(self.resource.uniforms.get(uniform), 1, True, value.m.view(numpy.ndarray))
            else:
                raise AttributeError('Uniform "{}" with value "{}" is not an int, float, Vector3 or Matrix'.format(uniform, value))
        else:
            raise AttributeError('Uniform "{}" is not added to the list'.format(uniform))

    @timer
    def set_uniform_bl(self, uniform, value):
        self.set_uniform(uniform + '.base.color', value.color)
        self.set_uniform(uniform + '.base.intensity', value.intensity)

    @timer
    def set_uniform_dl(self, uniform, value):
        self.set_uniform_bl(uniform, value)
        self.set_uniform(uniform + '.direction', value.direction)

    @timer
    def set_uniform_pl(self, uniform, value):
        self.set_uniform_bl(uniform, value)
        self.set_uniform(uniform + '.attenuation.constant', value.constant)
        self.set_uniform(uniform + '.attenuation.linear', value.linear)
        self.set_uniform(uniform + '.attenuation.exponent', value.exponent)
        self.set_uniform(uniform + '.position', value.transform.transformed_position())
        self.set_uniform(uniform + '.range', value.range)

    @timer
    def set_uniform_sl(self, uniform, value):
        self.set_uniform_pl(uniform + '.pointLight', value)
        self.set_uniform(uniform + '.direction', value.direction)
        self.set_uniform(uniform + '.cutoff', value.cutoff)

    @classmethod
    def _load_shader(cls, file_name, type='vertex'):
        file_name = '{file}.glsl{ext}'.format(file=file_name, ext=type[0])
        shader_list = []
        with open(os.path.join(os.path.dirname(__file__), '..', '..', 'res', 'shaders', type, file_name), 'r', 1) as file:
            for line in file:
                line = line.strip()
                if line.startswith(Shader.INCLUDE_DIRECTIVE):
                    dotpos = line.rindex('.')
                    shader_list.append(cls._load_shader(line[len(Shader.INCLUDE_DIRECTIVE) + 2:dotpos], 'headers'))
                elif not line.startswith(Shader.COMMENT_DIRECTIVE):
                    shader_list.append(line)

            file.close()

        return '\n'.join(shader_list)

    @classmethod
    def get_instance(cls):
        if not cls._instance:
            cls._instance = cls()
        return cls._instance

    _is_printed = False

    def __del__(self):
        if self.resource.remove_reference() and self._filename is not None:
            Shader.loaded_shaders.pop(self._filename)

            if not Shader._is_printed:
                Shader._is_printed = True
                print('========SHADER=======================================================================',
                      timer,
                      '=====================================================================================', sep='\n')


class Attenuation(numpy.ndarray):

    def __new__(subtype, constant, linear, exponent):
        data = [constant, linear, exponent]
        dtype=numpy.float32
        buffer=None
        offset=0
        strides=None
        order=None
        obj = numpy.ndarray.__new__(subtype, 3, dtype, buffer, offset, strides,
                                    order)
        obj[:] = data
        return obj

    def __array_finalize__(self, obj):
        if obj is None: return

    @property
    def constant(self):
        return self[0]
    @constant.setter
    def constant(self, value):
        self[0] = value

    @property
    def linear(self):
        return self[1]
    @linear.setter
    def linear(self, value):
        self[1] = value

    @property
    def exponent(self):
        return self[2]
    @exponent.setter
    def exponent(self, value):
        self[2] = value

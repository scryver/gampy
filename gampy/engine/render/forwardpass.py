__author__ = 'michiel'

from gampy.engine.render.shader import Shader

class Ambient(Shader):

    _instance = None

    def __init__(self):
        super(Ambient, self).__init__()

        self.add_vertex_shader_from_file('forward_ambient')
        self.add_fragment_shader_from_file('forward_ambient')

        self.set_attribute_location('position', 0)
        self.set_attribute_location('texCoord', 1)

        self.compile_shader()

        self.add_uniform('MVP')
        self.add_uniform('ambientIntensity')

    def update_uniforms(self, transform, material):
        # if material.texture is not None:
        #     material.texture.bind()
        # else:
        #     Texture.unbind()
        material.get('tex_diffuse').bind()

        world_matrix = transform.get_transformation()
        projected_matrix = self.render_engine.main_camera.view_projection() * world_matrix

        self.set_uniform('MVP', projected_matrix)
        self.set_uniform('ambientIntensity', self.render_engine.active_ambient_light)


class Directional(Shader):

    _instance = None

    def __init__(self):
        super(Directional, self).__init__()

        self.add_vertex_shader_from_file('forward_directional')
        self.add_fragment_shader_from_file('forward_directional')

        self.set_attribute_location('position', 0)
        self.set_attribute_location('texCoord', 1)
        self.set_attribute_location('normal', 2)

        self.compile_shader()

        self.add_uniform('model')
        self.add_uniform('MVP')
        self.add_uniform('cameraPosition')

        self.add_uniform('specularIntensity')
        self.add_uniform('specularExponent')

        self.add_uniform('directionalLight.base.color')
        self.add_uniform('directionalLight.base.intensity')
        self.add_uniform('directionalLight.direction')

    def update_uniforms(self, transform, material):
        # if material.texture is not None:
        #     material.texture.bind()
        # else:
        #     Texture.unbind()
        material.get('tex_diffuse').bind()

        camera = self.render_engine.main_camera
        world_matrix = transform.get_transformation()
        projected_matrix = camera.view_projection() * world_matrix

        self.set_uniform('model', world_matrix)
        self.set_uniform('MVP', projected_matrix)
        self.set_uniform('cameraPosition', camera.transform.transformed_position())

        self.set_uniform('specularIntensity', material.get('specular_intensity'))
        self.set_uniform('specularExponent', material.get('specular_exponent'))

        self.set_uniform_directional_light('directionalLight', self.render_engine.active_light)

    def set_uniform_base_light(self, uniform, value):
        self.set_uniform(uniform + '.base.color', value.color)
        self.set_uniform(uniform + '.base.intensity', float(value.intensity))

    def set_uniform_directional_light(self, uniform, value):
        self.set_uniform_base_light(uniform, value)
        self.set_uniform(uniform + '.direction', value.direction)


class Point(Shader):

    _instance = None

    def __init__(self):
        super(Point, self).__init__()

        self.add_vertex_shader_from_file('forward_point')
        self.add_fragment_shader_from_file('forward_point')

        self.set_attribute_location('position', 0)
        self.set_attribute_location('texCoord', 1)
        self.set_attribute_location('normal', 2)

        self.compile_shader()

        self.add_uniform('model')
        self.add_uniform('MVP')
        self.add_uniform('cameraPosition')

        self.add_uniform('specularIntensity')
        self.add_uniform('specularExponent')
        
        self.add_uniform('pointLight.base.color')
        self.add_uniform('pointLight.base.intensity')
        self.add_uniform('pointLight.attenuation.constant')
        self.add_uniform('pointLight.attenuation.linear')
        self.add_uniform('pointLight.attenuation.exponent')
        self.add_uniform('pointLight.position')
        self.add_uniform('pointLight.range')

    def update_uniforms(self, transform, material):
        # if material.texture is not None:
        #     material.texture.bind()
        # else:
        #     Texture.unbind()
        material.get('tex_diffuse').bind()

        camera = self.render_engine.main_camera
        world_matrix = transform.get_transformation()
        projected_matrix = camera.view_projection() * world_matrix

        self.set_uniform('model', world_matrix)
        self.set_uniform('MVP', projected_matrix)
        self.set_uniform('cameraPosition', camera.transform.transformed_position())

        self.set_uniform('specularIntensity', material.get('specular_intensity'))
        self.set_uniform('specularExponent', material.get('specular_exponent'))

        self.set_uniform_point_light('pointLight', self.render_engine.active_light)

    def set_uniform_base_light(self, uniform, value):
        self.set_uniform(uniform + '.base.color', value.color)
        self.set_uniform(uniform + '.base.intensity', float(value.intensity))

    def set_uniform_point_light(self, uniform, value):
        self.set_uniform_base_light(uniform, value)
        self.set_uniform(uniform + '.attenuation.constant', float(value.constant))
        self.set_uniform(uniform + '.attenuation.linear', float(value.linear))
        self.set_uniform(uniform + '.attenuation.exponent', float(value.exponent))
        self.set_uniform(uniform + '.position', value.transform.transformed_position())
        self.set_uniform(uniform + '.range', float(value.range))


class Spot(Shader):

    _instance = None

    def __init__(self):
        super(Spot, self).__init__()

        self.add_vertex_shader_from_file('forward_spot')
        self.add_fragment_shader_from_file('forward_spot')

        self.set_attribute_location('position', 0)
        self.set_attribute_location('texCoord', 1)
        self.set_attribute_location('normal', 2)

        self.compile_shader()

        self.add_uniform('model')
        self.add_uniform('MVP')
        self.add_uniform('cameraPosition')

        self.add_uniform('specularIntensity')
        self.add_uniform('specularExponent')

        self.add_uniform('spotLight.pointLight.base.color')
        self.add_uniform('spotLight.pointLight.base.intensity')
        self.add_uniform('spotLight.pointLight.attenuation.constant')
        self.add_uniform('spotLight.pointLight.attenuation.linear')
        self.add_uniform('spotLight.pointLight.attenuation.exponent')
        self.add_uniform('spotLight.pointLight.position')
        self.add_uniform('spotLight.pointLight.range')
        self.add_uniform('spotLight.direction')
        self.add_uniform('spotLight.cutoff')

    def update_uniforms(self, transform, material):
        # if material.texture is not None:
        #     material.texture.bind()
        # else:
        #     Texture.unbind()
        material.get('tex_diffuse').bind()

        camera = self.render_engine.main_camera
        world_matrix = transform.get_transformation()
        projected_matrix = camera.view_projection() * world_matrix

        self.set_uniform('model', world_matrix)
        self.set_uniform('MVP', projected_matrix)
        self.set_uniform('cameraPosition', camera.transform.transformed_position())

        self.set_uniform('specularIntensity', material.get('specular_intensity'))
        self.set_uniform('specularExponent', material.get('specular_exponent'))

        self.set_uniform_spot_light('spotLight', self.render_engine.active_light)

    def set_uniform_base_light(self, uniform, value):
        self.set_uniform(uniform + '.base.color', value.color)
        self.set_uniform(uniform + '.base.intensity', float(value.intensity))

    def set_uniform_point_light(self, uniform, value):
        self.set_uniform_base_light(uniform, value)
        self.set_uniform(uniform + '.attenuation.constant', float(value.constant))
        self.set_uniform(uniform + '.attenuation.linear', float(value.linear))
        self.set_uniform(uniform + '.attenuation.exponent', float(value.exponent))
        self.set_uniform(uniform + '.position', value.transform.transformed_position())
        self.set_uniform(uniform + '.range', float(value.range))

    def set_uniform_spot_light(self, uniform, value):
        self.set_uniform_point_light(uniform + '.pointLight', value)
        self.set_uniform(uniform + '.direction', value.direction)
        self.set_uniform(uniform + '.cutoff', float(value.cutoff))

__author__ = 'michiel'

from gampy.engine.render.shader import Shader
import gampy.engine.core.time as timing

timer_am = timing.Timing()
timer_di = timing.Timing()
timer_po = timing.Timing()
timer_sp = timing.Timing()

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

    @timer_am
    def w(self, transform):
        return transform.transformation

    @timer_am
    def pw(self, render_engine, world_matrix):
        return render_engine.main_camera.view_projection() * world_matrix

    @timer_am
    def update_uniforms(self, transform, material, render_engine):
        # if material.texture is not None:
        #     material.texture.bind()
        # else:
        #     Texture.unbind()
        material.get('diffuse', 'texture').bind()

        world_matrix = self.w(transform)
        projected_matrix = self.pw(render_engine, world_matrix)

        self.set_uniform('MVP', projected_matrix)
        self.set_uniform('ambientIntensity', render_engine.active_ambient_light)

    def __del__(self):
        print('========AMBIENT======================================================================',
              timer_am,
              '=====================================================================================', sep='\n')


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

    @timer_di
    def w(self, transform):
        return transform.transformation

    @timer_di
    def pw(self, camera, world_matrix):
        return camera.view_projection() * world_matrix

    @timer_di
    def get_transform_pos(self, object):
        return object.transform.transformed_position()

    @timer_di
    def update_uniforms(self, transform, material, render_engine):
        # if material.texture is not None:
        #     material.texture.bind()
        # else:
        #     Texture.unbind()
        material.get('diffuse', 'texture').bind()

        camera = render_engine.main_camera

        world_matrix = self.w(transform)
        projected_matrix = self.pw(camera, world_matrix)

        self.set_uniform('model', world_matrix)
        self.set_uniform('MVP', projected_matrix)
        self.set_uniform('cameraPosition', self.get_transform_pos(camera))

        self.set_uniform('specularIntensity', material.get('specular_intensity'))
        self.set_uniform('specularExponent', material.get('specular_exponent'))

        self.set_uniform_directional_light('directionalLight', render_engine.active_light)

    def set_uniform_base_light(self, uniform, value):
        self.set_uniform(uniform + '.base.color', value.color)
        self.set_uniform(uniform + '.base.intensity', float(value.intensity))

    def set_uniform_directional_light(self, uniform, value):
        self.set_uniform_base_light(uniform, value)
        self.set_uniform(uniform + '.direction', value.direction)

    def __del__(self):
        print('========DIRECTIONAL==================================================================',
              timer_di,
              '=====================================================================================', sep='\n')


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

    @timer_po
    def w(self, transform):
        return transform.transformation

    @timer_po
    def pw(self, camera, world_matrix):
        return camera.view_projection() * world_matrix

    @timer_po
    def get_transform_pos(self, object):
        return object.transform.transformed_position()

    @timer_po
    def update_uniforms(self, transform, material, render_engine):
        # if material.texture is not None:
        #     material.texture.bind()
        # else:
        #     Texture.unbind()
        material.get('diffuse', 'texture').bind()

        camera = render_engine.main_camera

        world_matrix = self.w(transform)
        projected_matrix = self.pw(camera, world_matrix)

        self.set_uniform('model', world_matrix)
        self.set_uniform('MVP', projected_matrix)
        self.set_uniform('cameraPosition', self.get_transform_pos(camera))

        self.set_uniform('specularIntensity', material.get('specular_intensity'))
        self.set_uniform('specularExponent', material.get('specular_exponent'))

        self.set_uniform_pl('pointLight', render_engine.active_light)

    def set_uniform_bl(self, uniform, value):
        self.set_uniform(uniform + '.base.color', value.color)
        self.set_uniform(uniform + '.base.intensity', float(value.intensity))

    def set_uniform_pl(self, uniform, value):
        self.set_uniform_bl(uniform, value)
        self.set_uniform(uniform + '.attenuation.constant', float(value.constant))
        self.set_uniform(uniform + '.attenuation.linear', float(value.linear))
        self.set_uniform(uniform + '.attenuation.exponent', float(value.exponent))
        self.set_uniform(uniform + '.position', self.get_transform_pos(value))
        self.set_uniform(uniform + '.range', float(value.range))

    def __del__(self):
        print('========POINT LIGHT==================================================================',
              timer_po,
              '=====================================================================================', sep='\n')


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

    @timer_sp
    def w(self, transform):
        return transform.transformation

    @timer_sp
    def pw(self, camera, world_matrix):
        return camera.view_projection() * world_matrix

    @timer_sp
    def get_transform_pos(self, object):
        return object.transform.transformed_position()

    @timer_sp
    def update_uniforms(self, transform, material, render_engine):
        # if material.texture is not None:
        #     material.texture.bind()
        # else:
        #     Texture.unbind()
        material.get('diffuse', 'texture').bind()

        camera = render_engine.main_camera

        world_matrix = self.w(transform)
        projected_matrix = self.pw(camera, world_matrix)

        self.set_uniform('model', world_matrix)
        self.set_uniform('MVP', projected_matrix)
        self.set_uniform('cameraPosition', self.get_transform_pos(camera))

        self.set_uniform('specularIntensity', material.get('specular_intensity'))
        self.set_uniform('specularExponent', material.get('specular_exponent'))

        self.set_uniform_sl('spotLight', render_engine.active_light)

    def set_uniform_bl(self, uniform, value):
        self.set_uniform(uniform + '.base.color', value.color)
        self.set_uniform(uniform + '.base.intensity', float(value.intensity))

    def set_uniform_pl(self, uniform, value):
        self.set_uniform_bl(uniform, value)
        self.set_uniform(uniform + '.attenuation.constant', float(value.constant))
        self.set_uniform(uniform + '.attenuation.linear', float(value.linear))
        self.set_uniform(uniform + '.attenuation.exponent', float(value.exponent))
        self.set_uniform(uniform + '.position', self.get_transform_pos(value))
        self.set_uniform(uniform + '.range', float(value.range))

    def set_uniform_sl(self, uniform, value):
        self.set_uniform_pl(uniform + '.pointLight', value)
        self.set_uniform(uniform + '.direction', value.direction)
        self.set_uniform(uniform + '.cutoff', float(value.cutoff))

    def __del__(self):
        print('========SPOT LIGHT===================================================================',
              timer_sp,
              '=====================================================================================', sep='\n')

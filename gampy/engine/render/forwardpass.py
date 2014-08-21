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
        super(Ambient, self).__init__('forward_ambient')

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
        super(Directional, self).__init__('forward_directional')

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
        super(Point, self).__init__('forward_point')

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
        super(Spot, self).__init__('forward_spot')

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

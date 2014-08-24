__author__ = 'michiel'

from gampy.engine.render.texture import Texture
from gampy.engine.render.resourcemanagement import MappedValue

class Material(MappedValue):

    def __init__(self, diffuse: Texture=None, specular_intensity: float=1., specular_power: float=8.,
                 normal_map: Texture=None,
                 disp_map: Texture=None, disp_map_scale: float=0., disp_map_offset: float=0.):
        super().__init__()
        if diffuse is None:
            diffuse = Texture('white.png')
        if normal_map is None:
            normal_map = Texture('default_normal.jpg')
        if disp_map is None:
            disp_map = Texture('default_disp.png')

        self.add_mapped_value('diffuse', diffuse)
        self.add_mapped_value('specularIntensity', specular_intensity)
        self.add_mapped_value('specularExponent', specular_power)
        self.add_mapped_value('normalMap', normal_map)
        self.add_mapped_value('dispMap', disp_map)

        base_bias = disp_map_scale /  2.
        self.add_mapped_value('dispMapScale', disp_map_scale)   # 0.04 is a nice value
        self.add_mapped_value('dispMapBias', -base_bias + base_bias * disp_map_offset)

    def add_mapped_value(self, name, value):
        if isinstance(value, Texture):
            name = 'tex_' + name
            self._map.update({name: value})
        else:
            super().add_mapped_value(name, value)

    def get_mapped_value(self, name, type=None):
        result = super().get_mapped_value(name, type)
        if result is not None:
            return result

        if type == 'tex':
            return Texture('test.png')
        else:
            return False
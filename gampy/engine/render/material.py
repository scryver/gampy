__author__ = 'michiel'

from gampy.engine.render.texture import Texture
from gampy.engine.render.mapper import MappedValue

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

        self.set_mapped_value('diffuse', diffuse)
        self.set_mapped_value('specularIntensity', specular_intensity)
        self.set_mapped_value('specularExponent', specular_power)
        self.set_mapped_value('normalMap', normal_map)
        self.set_mapped_value('dispMap', disp_map)

        base_bias = disp_map_scale /  2.
        self.set_mapped_value('dispMapScale', disp_map_scale)   # 0.04 is a nice value
        self.set_mapped_value('dispMapBias', -base_bias + base_bias * disp_map_offset)
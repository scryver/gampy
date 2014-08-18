__author__ = 'michiel'

from gampy.engine.components.gamecomponent import GameComponent
from gampy.engine.render.material import Material
from gampy.engine.render.meshes import Mesh

class MeshRenderer(GameComponent):

    def __init__(self, mesh, material):
        super().__init__()
        if not isinstance(mesh, Mesh):
            raise AttributeError('Mesh is not valid')
        if not isinstance(material, Material):
            raise AttributeError('Material is not valid')

        self.mesh = mesh
        self.material = material

    def render(self, shader):
        shader.bind()
        shader.update_uniforms(self.transform, self.material)
        try:
            self.mesh.draw()
        finally:
            shader.unbind()
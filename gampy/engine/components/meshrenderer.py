__author__ = 'michiel'

from gampy.engine.components.gamecomponent import GameComponent


class MeshRenderer(GameComponent):

    def __init__(self, mesh, material):
        super().__init__()

        self.mesh = mesh
        self.material = material

    def render(self, shader, render_engine):
        shader.bind()
        shader.update_uniforms(self.transform, self.material, render_engine)
        try:
            self.mesh.draw()
        finally:
            shader.unbind()
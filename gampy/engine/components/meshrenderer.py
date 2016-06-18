__author__ = 'michiel'

from gampy.engine.components.entitycomponent import EntityComponent



class MeshRenderer(EntityComponent):

    def __init__(self, mesh, material):
        super().__init__()

        self.mesh = mesh
        self.material = material

    def render(self, shader, render_engine, camera_view, camera_pos):
        shader.bind()
        shader.update_uniforms(self.transform, self.material, render_engine, camera_view, camera_pos)
        try:
            self.mesh.draw()
        finally:
            shader.unbind()

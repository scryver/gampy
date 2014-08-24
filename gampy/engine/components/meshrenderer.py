__author__ = 'michiel'

from gampy.engine.components.gamecomponent import GameComponent
import gampy.engine.core.time as timing

# timer = timing.Timing()


class MeshRenderer(GameComponent):

    # _is_printed = False

    # @timer
    def __init__(self, mesh, material):
        super().__init__()

        self.mesh = mesh
        self.material = material

    # @timer
    def render(self, shader, render_engine, camera_view, camera_pos):
        shader.bind()
        shader.update_uniforms(self.transform, self.material, render_engine, camera_view, camera_pos)
        try:
            self.mesh.draw()
        finally:
            shader.unbind()

    # def __del__(self):
    #     if not MeshRenderer._is_printed:
    #         MeshRenderer._is_printed = True
    #         # print('========MESH RENDERER================================================================',
    #         #       timer,
    #         #       '=====================================================================================', sep='\n')
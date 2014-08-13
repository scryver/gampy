__author__ = 'michiel'

import gampy.engine.input.input as gameinput
import gampy.engine.objects.meshes as meshes
import gampy.engine.objects.vectors as vec
import sdl2

class Game:

    def __init__(self):
        self.mesh = meshes.Mesh()

        data = [
            meshes.Vertex(vec.Vector3(1., -1., 0.)),
            meshes.Vertex(vec.Vector3(-1., -1., 0.)),
            meshes.Vertex( vec.Vector3(0., 1., 0.)),
        ]
        self.mesh.add_vertices(data)

    def input(self, inputs):
        mouse_pos = inputs.mouse_position
        if inputs.get_key_down(sdl2.SDLK_DOWN):
            print('We\'ve just pressed key DOWN')
        if inputs.get_key_up(gameinput.KEY_DOWN):
            print('We\'ve just released key DOWN')
        if inputs.get_mouse_down(1):
            print('We\'ve just pressed mouse Left at {}'.format(mouse_pos))
        if inputs.get_mouse_up(1):
            print('We\'ve just released mouse Left at {}'.format(mouse_pos))

    def update(self):
        pass

    def render(self):
        self.mesh.draw()

    def destroy(self):
        pass
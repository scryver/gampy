__author__ = 'michiel'


class EventInterface:
    def input(self, dt):
        raise NotImplementedError('Class "{class}" has no input method defined'.format(self.__class__))
    def update(self, dt):
        raise NotImplementedError('Class "{class}" has no update method defined'.format(self.__class__))
    def render(self, shader, render_engine, camera_view, camera_pos):
        raise NotImplementedError('Class "{class}" has no render method defined'.format(self.__class__))
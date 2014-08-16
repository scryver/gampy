__author__ = 'michiel'


class EventInterface:
    def input(self, *args, **kwargs):
        raise NotImplementedError('Class "{class}" has no input method defined'.format(self.__class__))
    def update(self, *args, **kwargs):
        raise NotImplementedError('Class "{class}" has no update method defined'.format(self.__class__))
    def render(self, *args, **kwargs):
        raise NotImplementedError('Class "{class}" has no render method defined'.format(self.__class__))
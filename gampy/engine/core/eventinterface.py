__author__ = 'michiel'


class EventInterface:
    def input(self):
        raise NotImplementedError('Class "{class}" has no input method defined'.format(self.__class__))
    def update(self):
        raise NotImplementedError('Class "{class}" has no update method defined'.format(self.__class__))
    def render(self):
        raise NotImplementedError('Class "{class}" has no render method defined'.format(self.__class__))
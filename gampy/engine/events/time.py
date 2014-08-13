__author__ = 'michiel'

import time


class Time:

    def __init__(self):
        self._delta = 0.

    @staticmethod
    def get_time():
        return time.monotonic()

    @staticmethod
    def sleep():
        time.sleep(0.001)

    @property
    def delta(self):
        return self._delta

    @delta.setter
    def delta(self, delta):
        self._delta = delta
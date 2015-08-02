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


class Timing:

    startl = '+' + '-' * 22 + '+' + '{name:-^17}' + '+' + '-' * 19 + '+' + \
             '-' * 17 + '+'
    string = """\
| {key:<20} | avg: {avg:>10.3f} | total: {tot:>10.3f} | count: {cnt:>8d} |
""".format
    endl = '+' + '-' * 22 + '+' + '-' * 17 + '+' + '-' * 19 + '+' + '-' * 17 + \
           '+'

    def __init__(self, name):
        self.name = name
        self.timings = {}
        self.col = self.__collector()
        next(self.col)                 # coroutine syntax

    def __collector(self):
        while True:
            (name, t) = (yield)         # coroutine syntax
            if name in self.timings:
                self.timings[name]['timings'].append(t)
                self.timings[name]['count'] += 1
                self.timings[name]['total'] += t
            else:
                self.timings[name] = {}  # if this entry doesn't exist yet
                self.timings[name]['timings'] = [t]
                self.timings[name]['count'] = 1
                self.timings[name]['total'] = t

    def __call__(self, func):
        """Turn the object into a decorator"""
        def wrapper(*arg, **kwargs):
            t1 = time.time()                # start time
            res = func(*arg, **kwargs)      # call the originating function
            t2 = time.time()                # stop time
            t = (t2 - t1) * 1000.0          # time in milliseconds
            data = (func.__name__, t)
            self.col.send(data)             # collect the data
            return res
        return wrapper

    def __str__(self):
        s = self.startl.format(name=self.name) + '\n'
        for key in self.timings.keys():
            count = self.timings[key].get('count', 0)
            if count == 0:
                continue
            total = self.timings[key].get('total', 0)
            if len(key) > 20:
                k = key[:17] + '...'
            else:
                k = key
            s += self.string(key=k, avg=total / count, tot=total, cnt=count)
        s += self.endl
        return s

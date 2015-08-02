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

    string = """\
{key:<30} | avg: {avg:>10.3f} | total: {tot:>10.3f} | count: {cnt:>8d}
""".format
    endl = '-' * (28 + 58)

    def __init__(self):
        self.timings = {}
        self.col = self.__collector()
        next(self.col)                 # coroutine syntax

    def __collector(self):
        while True:
            (name, t) = (yield)         # coroutine syntax
            if name in self.timings:
                self.timings[name]['timings'] += [t]
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
            t = (t2-t1)*1000.0              # time in milliseconds
            data = (func.__name__, t)
            self.col.send(data)             # collect the data
            return res
        return wrapper

    def __str__(self):
        s = 'Timings:\n'
        for key in self.timings.keys():
            # s += '{timingKey:<30} | '.format(timingKey=key)
            # ts = self.timings[key].timings
            count = self.timings[key].get('count', 0)
            if count == 0:
                return
            total = self.timings[key].get('total', 0)
            # s += 'average: {avg:>10.3f} |'.format(avg=total / count)
            # s += ' total: {tot:>10.3f} |'.format(tot=total)
            # s += ' count: {cnt:>8d}'.format(cnt=count)
            s += self.string(key=key, avg=total / count, tot=total, cnt=count)
        s += self.endl
        return s

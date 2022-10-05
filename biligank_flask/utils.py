import json
import time
import timeit


def write_json(data_dict, filename):
    with open('./%s.json' %filename, 'a', encoding='utf-8') as f:
        json.dump(data_dict, f, ensure_ascii=False, indent=4)
        f.write(',')


class Timer:
    __slots__ = ('st', 'et')

    def __enter__(self):
        self.tick()

    def __exit__(self, exc_type, exc_value, exc_tb):
        self.tock()

    def tick(self):
        self.st = timeit.default_timer()

    def tock(self):
        self.et = timeit.default_timer()

    @property
    def result(self):
        return round(self.et - self.st, 3)


def get_date():
    return time.strftime("%Y_%m_%d", time.localtime())

def get_clock():
    return time.strftime("%H:%M:%S", time.localtime())

def ts2date(time_stamp):
    struct_time = time.localtime(time_stamp)
    return time.strftime("%Y-%m-%d %H:%M:%S", struct_time)

def ts2date_2(time_stamp):
    struct_time = time.localtime(time_stamp)
    return time.strftime("%m-%d %H:%M", struct_time)

def ts2clock(time_stamp):
    struct_time = time.localtime(time_stamp)
    return time.strftime("%H:%M:%S", struct_time)

def get_time():
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

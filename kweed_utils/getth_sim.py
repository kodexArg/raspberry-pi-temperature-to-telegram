import time
import numpy as np

#DEFAULTS

def random_temp(t):
    t = t - 1 if t > 25 else t + 1
    t = np.random.normal(t, 2.5, 1)[0].astype(int)
    return t


def random_humi(h):
    h = h - 1 if h > 50 else h + 1
    h = np.random.normal(h, 4, 1)[0].astype(int)
    return h


def get_temp():
    try:
        t
    except NameError:
        t = 25
    t = random_temp(t)
    return t


def get_humi():
    try:
        h
    except NameError:
        h = 50
    h = random_humi(h)
    return h


if __name__ == "__main__":
    print(get_temp())
    print(get_humi())

import pickle
from functools import wraps

from .data import pyoptions, pypaths


def load(func):

    @wraps(func)
    def inner(*args, **kargs):
        f = open(pypaths.sequence_path, 'rb')
        pyoptions.cmd_list = pickle.load(f)
        return func(*args, **kargs)

    return inner

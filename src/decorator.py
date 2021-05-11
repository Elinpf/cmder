from functools import wraps
import pickle

from src.data import pypaths, pyoptions


def load(func):

    @wraps(func)
    def inner(*args, **kargs):
        f = open(pypaths.sequence_path, 'rb')
        pyoptions.cmd_list = pickle.load(f)
        return func(*args, **kargs)

    return inner

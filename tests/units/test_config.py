from cmder.config import Config
import os


def test_load(shared_datadir):
    conf = Config(shared_datadir / 'config.json')
    assert os.path.exists(shared_datadir / 'config.json')


def test_extend_dir(shared_datadir):
    conf = Config(shared_datadir / 'config.json')
    assert conf.extend_dir == ['.git']


def test_history_size(shared_datadir):
    conf = Config(shared_datadir / 'config.json')
    assert conf.history_size == 50


def test_set_history_size(shared_datadir):
    conf = Config(shared_datadir / 'config.json')
    conf.history_size = 100
    assert conf.history_size == 100


def test_set_history_size_to_under_zero(shared_datadir):
    conf = Config(shared_datadir / 'config.json')
    conf.history_size = -1
    assert conf.history_size == 0


def test_global_config(shared_datadir):
    conf = Config(shared_datadir / 'config.json')
    assert conf.global_config == {}


def test_set_global_config(shared_datadir):
    conf = Config(shared_datadir / 'config.json')
    conf.set_global_config(('key', 'value'))
    assert conf.global_config['key'] == 'value'


def test_get_global_config_func(shared_datadir):
    conf = Config(shared_datadir / 'config.json')
    conf.set_global_config(('key', 'value'))
    assert conf.get_global_config('key') == 'value'
    assert conf.get_global_config('None') is None


def test_del_global_config(shared_datadir):
    conf = Config(shared_datadir / 'config.json')
    conf.set_global_config(('key', 'value'))
    assert conf.get_global_config('key') == 'value'
    conf.del_global_config('key')
    assert conf.get_global_config('key') is None


def test_init_global_config(shared_datadir):
    conf = Config(shared_datadir / 'config.json')
    conf.set_global_config(('key', 'value'))
    assert conf.get_global_config('key') == 'value'
    conf.init_global_config()
    assert conf.global_config == {}

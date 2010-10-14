import sys
sys.path.extend(['..', '.'])
from core.config import Config

def test_retrieval():
    config = Config()
    config[1] = 42
    assert config[1] == 42
    config['key'] = 'value'
    assert config['key'] == 'value'

def test_overwrite():
    config = Config()
    config[1] = 1
    config[1] = 2
    assert config[1] == 2

def test_init():
    config = Config({'key1': 'value1', 'key2': 'value2'})
    assert config['key1'] == 'value1'
    assert config['nonexistent_key'] == None

def test_default():
    config = Config()
    config['key'] = 'value'
    config.default('key', 'wrong value')
    config.default(1, 2)
    assert config['key'] == 'value'
    assert config[1] == 2


def test_init_empty_dict():
    config1 = Config()
    config2 = Config()
    config1[1] = 2
    assert config2[1] == None

def test_merge():
    config = Config({'a': 1, 'b': 2})
    config.merge({'b': 3, 'c': 4})
    assert config['b'] == 3
    assert config['a'] == 1
    config.merge({'c': 5, 'd': 6}, False)
    assert config['c'] == 4

def test_merge_overwrite():
    config = Config({1: 1})
    config.merge({1: 2}, False)
    assert config[1] == 1

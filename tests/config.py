import unittest
import sys
import random

sys.path.extend(['..', '.'])
from core.config import Config


class TestConfig(unittest.TestCase):
    def test_retrieval(self):
        config = Config()
        config[1] = 42
        self.assertEquals(config[1], 42)
        config['key'] = 'value'
        self.assertEquals(config['key'], 'value')

    def test_overwrite(self):
        config = Config()
        config[1] = 1
        config[1] = 2
        self.assertEquals(config[1], 2)

    def test_init(self):
        config = Config({'key1': 'value1', 'key2': 'value2'})
        self.assertEquals(config['key1'], 'value1')
        self.assertEquals(config['nonexistent_key'], None)

    def test_default(self):
        config = Config()
        config['key'] = 'value'
        config.default('key', 'wrong value')
        config.default(1, 2)
        self.assertEquals(config['key'], 'value')
        self.assertEquals(config[1], 2)

    def test_init_empty_dict(self):
        config1 = Config()
        config2 = Config()
        config1[1] = 2
        self.assertEquals(config2[1], None)

    def test_merge(self):
        config = Config({'a': 1, 'b': 2})
        config.merge({'b': 3, 'c': 4})
        self.assertEquals(config['b'], 3)
        self.assertEquals(config['a'], 1)
        config.merge({'c': 5, 'd': 6}, False)
        self.assertEquals(config['c'], 4)

    def test_merge_overwrite(self):
        config = Config({1: 1})
        config.merge({1: 2}, False)
        self.assertEquals(config[1], 1)

if __name__ == '__main__':
    unittest.main()


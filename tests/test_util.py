import nose
import sys
sys.path.extend(['..', '.'])
from core.interface import *

def test_slugify():
    assert slugify('asdf') == 'asdf'
    assert slugify('Foo') == 'foo'
    assert slugify('FooBar') == 'foo-bar'
    assert slugify('BarBazBomb') == 'bar-baz-bomb'

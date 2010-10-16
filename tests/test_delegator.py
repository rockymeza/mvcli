import sys
import nose.tools
sys.path.extend(['..', '.'])
from core.delegator import *
from core.exceptions import *
from core.mvcli import Argv
import core.config
from core.introspection import getoptionspec

def test_route():
    assert route(Argv(['controller', 'action', 'param1']), core.config.Config()) == {'action': 'action', 'controller': 'controller', 'parameters': ['param1']}


def test_parse_options_required_flag():
    assert parse_options(getoptionspec(lambda x, y=False: 1), Argv(['-x', 'foo', '-y'])) == Arguments(args=['foo'], kwargs={'y': True})
    assert parse_options(getoptionspec(lambda foo, bar=False: 1), Argv(['--foo', 'Hello', '--bar'])) == Arguments(args=['Hello'], kwargs={'bar': True})

def test_parse_options_with_files():
    assert parse_options(getoptionspec(lambda x, bar=False, *files: 1), Argv(['--bar', '-x', 'foo'])) == Arguments(args=['foo'], kwargs={'bar': True})
    assert parse_options(getoptionspec(lambda x, bar=False, *files: 1), Argv(['--bar', '-x', 'foo', 'baz'])) == Arguments(args=['foo', 'baz'], kwargs={'bar': True})
    assert parse_options(getoptionspec(lambda x, z, f=False: 1), Argv(['-xzf', 'foo', 'bar'])) == Arguments(args=['foo', 'bar'], kwargs={'f': True})
    assert parse_options(getoptionspec(lambda foo, bar='Hello', verbose=False, *files: 1), Argv(['--verbose', 'outoforder_file', '--foo=baz'])) == Arguments(args=['baz', 'outoforder_file'], kwargs={'verbose': True})

@nose.tools.raises(NoFilesError)
def test_parse_options_failure():
    assert parse_options(getoptionspec(lambda foo, bar: 1), Argv(['--bar=1', 'b'])) == Arguments(args=['b'], kwargs={'bar': 1})

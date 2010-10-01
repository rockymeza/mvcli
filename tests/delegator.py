import doctest
import sys

sys.path.extend(['..', '.'])
import core.delegator

doctest.testmod(core.delegator)

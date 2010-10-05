import doctest
import sys

sys.path.extend(['..', '.'])
import core.request

doctest.testmod(core.request)

import doctest
import sys

sys.path.extend(['..', '.'])
import core.config

doctest.testmod(core.config)

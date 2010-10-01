#!/usr/bin/env python

import sys
from core import delegator
from core.config import config

config['default_controller'] = 'main'
config['default_action'] = 'main'
delegator.Delegator(sys.argv)




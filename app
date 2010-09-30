#!/usr/bin/env python

import sys
from core import delegator
from core.config import config

config.set('default_controller', 'main')
config.set('default_action', 'main')
delegator.Delegator(sys.argv)




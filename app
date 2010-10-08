#!/usr/bin/env python

import sys

from core.mvcli import MVCLI
from controller import main

app = MVCLI()
app.config['default_controller'] = 'main'
app.config['default_action'] = 'main'
app.add_controller(main.Main, 'main', 'm')
app.run(sys.argv)


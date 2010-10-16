#!/usr/bin/env python

import sys

from core.mvcli import MVCLI
import controller.main
import controller.help

app = MVCLI()
app.config['default_controller'] = 'main'
app.config['default_action'] = 'main'
app.add_controller(controller.main.Main, 'main', 'm')
app.add_controller(controller.help.Help, 'help', 'h')
app.run(sys.argv)


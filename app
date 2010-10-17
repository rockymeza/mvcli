#!/usr/bin/env python

import sys

from core.mvcli import MVCLI
import controller.main

app = MVCLI()
app.config['default_controller'] = 'main'
app.config['default_action'] = 'main'

app.config['colors.title'] = 'green.blue'
app.config['colors.header'] = 'yellow.red'
app.config['colors.key'] = 'white.green'
app.config['colors.value'] = 'yellow'

app.add_controller(controller.main.Main, 'main', 'm')
app.controllers['main'].metadata('Main Controller', 'This is the awesome main controller')
app.controllers['main'].action('main', 'Prints Hello World')
app.controllers['main'].action('foo', 'foo description', {'bar': 'bar description', 'baz': 'baz description', 'qux': 'qux description', 'quux': 'quux description'})
app.controllers['main'].action('help', 'Display this screen and exit')
app.run(sys.argv)


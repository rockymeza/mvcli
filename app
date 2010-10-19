#!/usr/bin/env python

import sys

from core.mvcli import MVCLI
import controller.main
import core.controllers

app = MVCLI()
app.title = 'Awesome Title App'
app.description = 'This is the awesome example application'

app.config['default_controller'] = 'help'
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

app.add_controller(core.controllers.Help, 'help', 'h')
app.controllers['help'].action('main', 'Prints Help Screen')

app.run(sys.argv)

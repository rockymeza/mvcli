#!/usr/bin/env python

import sys

from core.mvcli import MVCLI
import controller.main
import core.controllers

app = MVCLI()
app.title = 'Awesome Title App'
app.description = 'This is the awesome example application'
app.version = 'Awesome Title App v0.0.1 by Rocky and Gavin'

app.config['default_controller'] = 'help'
app.config['default_action'] = 'help'

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
app.controllers['help'].action('help', 'Prints Help Screen')

app.add_controller(core.controllers.Version, 'version', 'v')
app.controllers['version'].action('help', 'Prints version and exits')

app.run(sys.argv)

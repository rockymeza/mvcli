#!/usr/bin/env python
import copy

class MVCLIMeta(type):
    def __new__(cls, name, bases, dict):
        obj = super(MVCLIMeta, cls).__new__(cls, name, bases, dict)
        obj._mvcli = {
                'methods': [],
                'meta': {},
                }
        for key, value in dict.iteritems():
            if not key.startswith('_'):
                if hasattr(value, '__call__'):
                    obj._mvcli['methods'].append((key, value.__doc__))
                else:
                    obj._mvcli['meta'][key] = value
        return obj

class MVCLIBase(object):
    __metaclass__ = MVCLIMeta
    title = "MVCLI application"

    def run(self, argv):
        argv = self.argv = copy.copy(argv)
        self.program_name = argv.pop(0)
        try:
            command = argv.pop(0)
            print self.__dict__
            self.__dict__[command].call()
        except IndexError:
            self.help()
            
    def help(self):
        meta = self._mvcli['meta']
        for i in ['title', 'description']:
            try:
                if meta[i]:
                    print meta[i]
            except KeyError:
                pass

        methods = self._mvcli['methods']
        if methods:
            print 'Commands:'
            for method, description in methods:
                print '\t', method, '\t',description


class Todo(MVCLIBase):
    title = "todo application"

    def add(self, name, description):
        "Add a task"
        pass

    def remove(self, id):
        "Remove a task"
        pass

    def list(self):
        "List all tasks"
        pass


if __name__ == '__main__':
    import sys

    Todo().run(sys.argv)

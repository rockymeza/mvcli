# ANSI color codes
fgcolors = {
        'black': '30',
        'red': '31',
        'green': '32',
        'yellow': '33',
        'blue': '34',
        'magenta': '35',
        'cyan': '36',
        'white': '37',
        'default': '39',
        }
bgcolors = {
        'black': '40',
        'red': '41',
        'green': '42',
        'yellow': '43',
        'blue': '44',
        'magenta': '45',
        'cyan': '46',
        'white': '47',
        'default': '49',
        }
def color(text, fgcolor = None, bgcolor = None):
    """
    >>> color('Foo', 'red') == '\033[31mFoo\033[0m'
    True
    >>> color('Foo', None, 'red') == '\033[41mFoo\033[0m'
    True
    >>> color('Foo', 'cyan', 'red') == '\033[41m\033[36mFoo\033[0m\033[0m'
    True
    >>> color('Foo', fgcolor = 'red') == '\033[31mFoo\033[0m'
    True
    >>> color('Foo', bgcolor = 'red') == '\033[41mFoo\033[0m'
    True
    >>> color('Foo', fgcolor = 'cyan', bgcolor = 'red') == '\033[41m\033[36mFoo\033[0m\033[0m'
    True
    >>> color('Foo', 'cyan.red') == '\033[41m\033[36mFoo\033[0m\033[0m'
    True
    """
    if fgcolor:
        if fgcolor.find('.') > 0:
            (fgcolor, ignore, bgcolor) = fgcolor.partition('.')
            
        text = surround(text, fgcolors[fgcolor])
    if bgcolor:
        text = surround(text, bgcolors[bgcolor])

    return text

def surround(text, code):
    return '\033[' + code + 'm' + text + '\033[0m'


import doctest
doctest.testmod()

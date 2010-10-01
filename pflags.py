import core.delegator
args = ['--hello=world', '-a=b', '--foo', '-f', 'bar', 'baz']

print args
print core.delegator.parse_flags(args)

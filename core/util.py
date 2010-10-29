import re

def slugify(str):
    """
    camel case string -> slug
    """
    if str.islower():
        return str
    return '-'.join([i.lower() for i in re.compile('[A-Z][a-z]*').findall(str)])


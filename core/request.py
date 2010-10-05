class Request(dict):
    """
    Request Class is a container for the request, it holds all pertinent data
    and should be available to every controller and view
    >>> x = Request()
    >>> x[1] = 2
    >>> x[1]
    2
    >>> x[2] == None
    True
    """
    __getitem__ = dict.get

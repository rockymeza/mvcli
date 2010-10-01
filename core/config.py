class Config:
    """
    Config Class is a container for the configuration settings that the core classes use
    >>> config = Config()
    """
    def __init__(self):
        self.dictionary = {}

    def __getitem__(self, key):
        """
        Returns a value from the config dictionary based on the key
        >>> config['x'] = 1
        >>> config['x']
        1

        If that key does not exist in the dictionary, it will return None
        >>> config[12] == None
        True
        """
        if key in self.dictionary:
            return self.dictionary[key]
        else:
            return None

    def __setitem__(self, key, value):
        """
        Stores a value in the dictionary using a key
        
        If a value for that key already exists, it will be overwritten
        >>> config['y'] = 1
        >>> config['y'] = 2
        >>> config['y']
        2
        """
        self.dictionary[key] = value

config = Config()

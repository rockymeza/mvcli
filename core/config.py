class Config:
    """
    Config Class is a container for the configuration settings that the core classes use
    >>> config = Config()
    """
    def __init__(self, dictionary = None):
        """
        Instantiates an instance of the Config class.

        It can accept a dictionary for the default configurations

        >>> config1 = Config()
        >>> config2 = Config({'key1': 'value1', 'key2': 'value2'})
        >>> config2['key1']
        'value1'
        >>> config2['nonexistent_key'] == None
        True
        >>> config2.default('key1', 'other value')
        >>> config2['key1']
        'value1'
        >>> config2['key2'] = 'new value'
        >>> config2['key2']
        'new value'

        # a tricky one
        >>> config1 = Config()
        >>> config2 = Config()
        >>> config1[1] = 2
        >>> config2[1] == None
        True
        """
        self.dictionary = dictionary or {}

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
        return self.dictionary.get(key)

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

    def default(self, key, value):
        """
        Stores a value in the dictionary using a key
        
        If a value for that key already exists, it will not be overwritten
        >>> config.default('x', 1)
        >>> config['x']
        1
        >>> config['y'] = 2
        >>> config['y']
        2
        >>> config.default('y', 'other value')
        >>> config['y']
        2
        """
        if not key in self.dictionary:
            self.dictionary[key] = value
config = Config()

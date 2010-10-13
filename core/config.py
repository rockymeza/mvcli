class Config:
    """
    Config Class is a container for the configuration settings that the core classes use
    """
    def __init__(self, dictionary = None):
        """
        Instantiates an instance of the Config class.

        It can accept a dictionary for the default configurations
        """
        self.dictionary = dictionary or {}

    def __getitem__(self, key):
        """
        Returns a value from the config dictionary based on the key. If that
        key does not exist in the dictionary, it will return None
        """
        return self.dictionary.get(key)

    def __setitem__(self, key, value):
        """
        Stores a value in the dictionary using a key
        
        If a value for that key already exists, it will be overwritten
        """
        self.dictionary[key] = value

    def default(self, key, value):
        """
        Stores a value in the dictionary using a key
        
        If a value for that key already exists, it will not be overwritten
        """
        if not key in self.dictionary:
            self.dictionary[key] = value

    def merge(self, dictionary, overwrite = True):
        """
        Merges a dictionary into the current dictionary
        You can change the name if you want
     
        Will overwrite by default
        """
        if overwrite:
            self.dictionary.update(dictionary)
        else:
            self.dictioanry = dict(dictionary, **self.dictionary)


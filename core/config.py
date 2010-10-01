class Config:
    """
    Config Class is a container for the configuration settings that the core classes use
    """
    def __init__(self):
        self.dictionary = {}

    def __getitem__(self, key):
        """
        Returns a vlue from the config dictionary based on the key

        If that key does not exist in the dictionary, it will return None
        """
        if key in self.dictionary:
            return self.dictionary[key]
        else:
            return None

    def __setitem__(self, key, value):
        """
        Stores a value in the dictionary using a key
        
        If a value for that key already exists, it will be overwritten
        """
        self.dictionary[key] = value

config = Config()

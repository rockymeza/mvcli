class Request:
    """
    Request Class is a container for the request, it holds all pertinent data
    and should be available to every controller and view
    """
    def __init__(self):
        self.dictionary = {}

    def __getitem__(self, key):
        """
        Returns a value from the request dictionary based on the key
        
        If that key does not exist, it will return None
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
        

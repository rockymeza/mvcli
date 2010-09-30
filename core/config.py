class Config:
    def __init__(self):
        self.configs = {}
    
    def set(self, key, value):
        self.configs['key'] = value

    def get(self, key):
        return self.configs['key']

config = Config()

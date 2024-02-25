

import json
import os

class Settings:
    def __init__(self):
        if not os.path.isfile('settings.json'):
            with open("settings.json", "w") as file:
                json.dump({"Language":"English", "ExtendedSettings": False}, file, indent=4)

        with open('settings.json', 'r') as file:
            self.data = json.load(file)
    
    def write_data(self, key, value):
        self.data[key] = value
        with open('settings.json', 'w') as file:
            json.dump(self.data, file, indent=4)

    def get_data(self, key):
        with open('settings.json', 'r') as file:
            self.data = json.load(file)
        return self.data.get(key)

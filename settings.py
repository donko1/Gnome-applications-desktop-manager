import json
import os

class Settings:
    def __init__(self):
        default_settings = {
            "Language": "English",
            "ExtendedSettings": False,
            "Theme": "dark"
        }

        if not os.path.isfile('settings.json'):
            with open("settings.json", "w") as file:
                json.dump(default_settings, file, indent=4)
        else:
            # Update existing settings file with any missing keys
            with open('settings.json', 'r') as file:
                current_settings = json.load(file)
        
            settings_updated = False
            for key, value in default_settings.items():
                if key not in current_settings:
                    current_settings[key] = value
                    settings_updated = True
        
            if settings_updated:
                with open('settings.json', 'w') as file:
                    json.dump(current_settings, file, indent=4)

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

if __name__ == "__main__":
    settings = Settings()

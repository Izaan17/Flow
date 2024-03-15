import json
from utils.directory_manager import get_app_dir


class Settings:
    def __init__(self, file_path):
        self.file_path = file_path
        self.settings = {}
        self.load_settings()

    def load_settings(self):
        try:
            with open(self.file_path, 'r') as file:
                self.settings = json.load(file)
        except FileNotFoundError:
            # File doesn't exist, initialize with an empty dictionary
            self.settings = {}

    def save_settings(self):
        with open(self.file_path, 'w') as file:
            json.dump(self.settings, file, indent=4)

    def add_setting(self, key, value):
        self.settings[key] = value
        self.save_settings()

    def get_setting(self, key, default=None):
        return self.settings.get(key, default)

    def remove_setting(self, key):
        if key in self.settings:
            del self.settings[key]
            self.save_settings()

    def list_settings(self):
        return self.settings


settings = Settings(f'{get_app_dir()}/settings.json')

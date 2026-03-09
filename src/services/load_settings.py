from json import load, dump
from pathlib import Path


class Settings:
    path = Path(__file__).parents[2] / 'config.json'
    config = None

    def __init__(self):
        with open(self.path, 'r', encoding='utf-8') as f:
            Settings.config = load(f)

    def get(self, setting_name):
        return Settings.config.get(setting_name)
    
    @classmethod
    def save(cls):
        with open(cls.path, 'w', encoding='utf-8') as f:
          dump(cls.config, f, indent=4, ensure_ascii=False)
    
    @classmethod
    def push(cls, *setting_name, changed_setting):
        if len(setting_name) > 1:
            cls.config[setting_name[0]][setting_name[1]] = changed_setting
        else:
             cls.config[setting_name] = changed_setting
        cls.save()

config = Settings()





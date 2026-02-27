from json import load


class Settings:
    def __init__(self, path = 'config.json'):
        self.path = path
        with open(self.path, 'r', encoding='utf-8') as f:
            self.config = load(f)

    def get(self, setting_name):
        setting = self.config[setting_name]
        return setting

config = Settings()




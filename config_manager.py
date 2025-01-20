import json
import os

class ConfigManager:
    def __init__(self):
        self.config_file = "config.json"
        self.default_config = {
            "api_key": "",
            "cx": "",
            "last_keyword": "",
            "start_page": "1",
            "end_page": "1"
        }
        self.config = self.load_config()

    def load_config(self):
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return self.default_config
        return self.default_config

    def save_config(self, config):
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(config, f, ensure_ascii=False, indent=4)

    def get_config(self):
        return self.config

    def update_config(self, **kwargs):
        self.config.update(kwargs)
        self.save_config(self.config) 
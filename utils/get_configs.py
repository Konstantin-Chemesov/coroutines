import yaml
import os
from box import Box
from utils.logger import log


class SettingsFile:

    def __init__(self):
        self.config_path = 'configs/settings.yaml'
        self.get_settings()

    def get_settings(self):
        if os.path.exists(self.config_path):
            with open(self.config_path) as file:
                self.settings = Box(yaml.load(file, Loader=yaml.FullLoader))
        else:
            log.info('There is no settings file')

import xml.etree.ElementTree as ETree
from pathlib import Path
import os


class Config:
    def __init__(self):
        self.base_dir = Path(__file__).resolve().parent.parent
        tree = ETree.parse(self.base_dir / 'config.xml')
        self.root = tree.getroot()

    def get(self, *keys, default=None):
        try:
            element = self.root
            for key in keys:
                element = element.find(key)
                if element is None:
                    return default

            value = element.text
            if value is None or value.strip() == '':
                return default

            if value.startswith('${') and value.endswith('}'):
                env_var = value[2:-1]
                return os.getenv(env_var, default)

            return value
        except AttributeError:
            return default

    def get_bool(self, section, key, default=False) -> bool:
        value = self.get(section, key, default)
        return str(value).lower() in ('true', '1', 't', 'yes')

    def get_int(self, section, key, default=0) -> int:
        value = self.get(section, key, default)
        return int(value)

    def get_float(self, section, key, default=0) -> int:
        value = self.get(section, key, default)
        return float(value)

    def get_list(self, section, key, default=None) -> list:
        value = self.get(section, key)
        return value.split(',') if value else (default or [])


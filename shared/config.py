import xml.etree.ElementTree as ETree
from pathlib import Path
import os

from loguru import logger


class Config:
    def __init__(self):
        self.base_dir = Path(__file__).resolve().parent.parent
        tree = ETree.parse(self.base_dir / 'config.xml')
        self.root = tree.getroot()

    def get(self, *keys, default=None, can_be_defaulted: bool = None):
        element = self.root
        for key in keys:
            element = element.find(key)
            if element is None:
                if not can_be_defaulted:
                    logger.error(f"Отсутствует запись в конфиге: {'.'.join(keys)}")
                    raise AttributeError()
                return default
        value = element.text
        if value is None or value.strip() == '':
            return default
        if value.startswith('${') and value.endswith('}'):
            env_var = os.getenv(value[2:-1], default)
            if not env_var:
                logger.error(f"Отсутствует переменная окружения: {value[2:-1]}")
                raise AttributeError()
            return env_var
        return value

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


import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
TELEGRAM_BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]

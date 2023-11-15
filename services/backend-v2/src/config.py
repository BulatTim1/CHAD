import os
from hashlib import sha256

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN").encode()
TELEGRAM_HASH = sha256(TELEGRAM_TOKEN).digest()
TELEGRAM_BOT_ID = 6667072025

AUTH_EXPIRES_IN = 14400

DB_PROVIDER = os.getenv("DB_PROVIDER")
DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME= os.getenv("DB_NAME")
DB_DEBUG = os.getenv("DB_DEBUG") == "True"

ADMINS = [485498234]
import os
import logging
from logging.handlers import RotatingFileHandler

# Bot Configuration
TG_BOT_TOKEN = os.environ.get("TG_BOT_TOKEN", "")
APP_ID = int(os.environ.get("APP_ID", ""))
API_HASH = os.environ.get("API_HASH", "")

# Database
CHANNEL_ID = int(os.environ.get("CHANNEL_ID", ""))
OWNER_ID = int(os.environ.get("OWNER_ID", ""))
DB_URI = os.environ.get("DATABASE_URL", "")
DB_NAME = os.environ.get("DATABASE_NAME", "Cluster0")

# Settings
PORT = os.environ.get("PORT", "8001")
TG_BOT_WORKERS = int(os.environ.get("TG_BOT_WORKERS", "200"))
PROTECT_CONTENT = True if os.environ.get('PROTECT_CONTENT', "False") == "True" else False

# Updates Channel (User can modify this)
UPDATES_CHANNEL = os.environ.get("UPDATES_CHANNEL", "https://telegram.me/Links4U_Channel")
UPDATES_CHANNEL_NAME = os.environ.get("UPDATES_CHANNEL_NAME", "🧐 Updates Channel")

# Messages
START_MSG = os.environ.get("START_MESSAGE", "Hello {first}!\n\nI am a file store bot. I can store private files and other users can access them from special links.")
HELP_TXT = "This is a file store bot.\n\n• Send me any file to get a shareable link\n• Use /batch for multiple files\n• Use /genlink for single file link"

# Logging
LOG_FILE_NAME = "filesharingbot.txt"
logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s - %(levelname)s] - %(name)s - %(message)s",
    datefmt='%d-%b-%y %H:%M:%S',
    handlers=[
        RotatingFileHandler(LOG_FILE_NAME, maxBytes=50000000, backupCount=10),
        logging.StreamHandler()
    ]
)
logging.getLogger("pyrogram").setLevel(logging.WARNING)

def LOGGER(name: str) -> logging.Logger:
    return logging.getLogger(name)

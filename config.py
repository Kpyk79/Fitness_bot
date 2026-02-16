import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = os.getenv("ADMIN_ID")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")  # Optional - AI features won't work without it

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN is not set in .env file")

if not ADMIN_ID:
    raise ValueError("ADMIN_ID is not set in .env file")

try:
    ADMIN_ID = int(ADMIN_ID)
except ValueError:
    raise ValueError("ADMIN_ID must be an integer")

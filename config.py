from os import getenv

from dotenv import load_dotenv

load_dotenv()

TOKEN = getenv("TOKEN")
API_ID = int(getenv("API_ID")) if getenv("API_ID") is not None else getenv("API_ID")
API_HASH = getenv("API_HASH")
ADMINS =[int(x) for x in (getenv("ADMINS") or "").split(",") if x.isdigit()]
APPLICATIONS_PATH = "applications_data.json"
DB_NAME = "database.db"


if not TOKEN:
    raise ValueError("Bot token is missing")

if not ADMINS:
    raise ValueError("Admins list is missing")

if not API_ID:
    raise ValueError("API ID is missing")

if not API_HASH:
    raise ValueError("API hash is missing")
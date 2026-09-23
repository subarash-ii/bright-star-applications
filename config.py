from os import getenv

from dotenv import load_dotenv

load_dotenv()

TOKEN = getenv("TOKEN")
ADMINS =[int(x) for x in (getenv("ADMINS") or "").split(",") if x.isdigit()]
APPLICATIONS_PATH = "applications_data.json"
DB_NAME = "database.db"

if not TOKEN:
    raise ValueError("Bot token is missing")

if not ADMINS:
    raise ValueError("Admins list is missing")
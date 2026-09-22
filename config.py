from os import getenv

from dotenv import load_dotenv

load_dotenv()

TOKEN = getenv("TOKEN")
ADMINS =[x for x in (getenv("ADMINS") or "").split(",") if x]
APPLICATIONS_PATH = "applications_data.json"


if not TOKEN:
    raise ValueError("Bot token is missing")

if not ADMINS:
    raise ValueError("Admins list is missing")
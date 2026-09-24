from pyrogram import Client

from config import API_ID, API_HASH, TOKEN

app = Client(
    "app_session",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=TOKEN
)
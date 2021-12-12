#!/usr/bin/env python3


### Importing
# Importing External Packages
from pyrogram import (
    Client,
    filters
)
from pyrogram.types import (
    Update,
    Message,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)

# Importing Inbuilt Packages
import logging

# Importing Credentials & Required Data
try:
    from testexp.config import Config
except ModuleNotFoundError:
    from config import Config


### For Displaying Errors&Warnings Better
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
logging.getLogger("pyrogram").setLevel(logging.WARNING)


### Starting Bot
app = Client(
    "ButtonBot",
    bot_token = Config.BOT_TOKEN,
    api_id = Config.APP_ID,
    api_hash = Config.API_HASH
)


### Handlers

# Button adder
@app.on_message(filters.chat(Config.CHANNEL_ID) & filters.document)
async def buttonAdder(bot:Update, msg:Message):
    try:
        await msg.edit_reply_markup(
            InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "👍",
                            callback_data = "like0"
                        ),
                        InlineKeyboardButton(
                            "👎",
                            callback_data = "dislike0"
                        )
                    ]
                ]
            )
        )
    except Exception as e:
        print(e)


app.run()


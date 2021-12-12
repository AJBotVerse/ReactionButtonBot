#!/usr/bin/env python3


### Importing
# Importing External Packages
import re
from pyrogram import (
    Client,
    filters
)
from pyrogram.types import (
    Update,
    Message,
    CallbackQuery,
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
    return await msg.edit_reply_markup(
        InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "👍",
                        callback_data = "👍 0"
                    ),
                    InlineKeyboardButton(
                        "👎",
                        callback_data = "👎 0"
                    )
                ]
            ]
        )
    )

# Button Trigger
@app.on_callback_query()
async def buttonHandler(bot:Update, callback:CallbackQuery):
    reaction, count = callback.data.split(' ')
    count = int(count)
    count += 1
    buttonMarkup = callback.message.reply_markup.inline_keyboard[0]
    reply_markup = []
    for button in buttonMarkup:
        if reaction == button.text.split(' ')[0]:
            data = f"{reaction} {count}"
            reply_markup.append(
                InlineKeyboardButton(
                    data,
                    callback_data = data
                )
            )
        else:
            reactionButton = button.text
            data = button.callback_data
            reply_markup.append(
                InlineKeyboardButton(
                    reactionButton,
                    callback_data = data
                )
            )
    else:
        return await callback.edit_message_reply_markup(
            InlineKeyboardMarkup(
                [
                    reply_markup
                ]
            )
        )


### Running Bot
app.run()


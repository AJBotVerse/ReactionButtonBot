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
    CallbackQuery
)

# Importing Inbuilt Packages
import logging

# Importing developer defined module
from utils import *


### For Displaying Errors&Warnings Better
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)
logging.getLogger(
    "pyrogram"
).setLevel(
    logging.WARNING
)


### Global Variable
taskList = []


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
                        callback_data = "👍"
                    ),
                    InlineKeyboardButton(
                        "👎",
                        callback_data = "👎"
                    )
                ]
            ]
        )
    )

# Button Trigger
@app.on_callback_query()
async def buttonHandler(bot:Update, callback:CallbackQuery):
    task = await ButtonTrigger.create(callback)
    taskList.append(task)
    return


### Running Bot
app.run()


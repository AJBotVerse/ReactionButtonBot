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
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup
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
    cdb = CheckingDB(
        callback.message.message_id,
        str(callback.from_user.id),
        reaction
    )
    result = cdb.start()
    reply_markup = []
    originalButton = callback.message.reply_markup.inline_keyboard[0]
    if result:
        if result == +1:
            count += 1
        else:
            count -= 1
        for button in originalButton:
            newstr = button.text.split(" ")
            if len(newstr) == 1:
                reactionO1 = newstr[0]
                countO1 = 0
            else:
                reactionO1, countO1 = newstr
            if reactionO1 == reaction:
                data1 = f"{reactionO1} {count}"
            else:
                data1 = f"{reactionO1} {countO1}"
            reply_markup.append(
                InlineKeyboardButton(
                    data1,
                    callback_data = data1
                )
            )
    else:
        for buttonOriginal in originalButton:
            reactionO, countO = buttonOriginal.text.split(" ")
            countO = int(countO)
            if reactionO == reaction:
                data = f"{reactionO} {countO+1}"
            else:
                data = f"{reactionO} {countO-1}"
            reply_markup.append(
                InlineKeyboardButton(
                    data,
                    callback_data = data
                )
            )
    return await callback.edit_message_reply_markup(
        InlineKeyboardMarkup(
            [
                reply_markup
            ]
        )
    )


### Running Bot
app.run()


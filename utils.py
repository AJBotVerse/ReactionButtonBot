#!/usr/bin/env python3


### Importing
from pymongo import MongoClient
from pyrogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)
from pyrogram.errors.exceptions import bad_request_400
try:
    from testexp.config import Config
except ModuleNotFoundError:
    from config import Config


### Connecting to mongodb
client = MongoClient(Config.MONGO_STR)
db = client["ReactionButtonBot"]
collection = db[str(Config.CHANNEL_ID)]


### Class
class CheckingDB:

    def __init__(
        self,
        message_id : int,
        userid : str,
        reaction : str
        ):
        self.message_id = message_id
        self.userid = userid
        self.reaction = reaction
    
    def start(self):
        msgQuery = {
            'msgid' : self.message_id
        }
        result = collection.find_one(msgQuery)
        if not result:
            msgQuery['userids'] = {
                self.userid : self.reaction
            }
            collection.insert_one(msgQuery)
            self.returnResult = +1
        else:
            userdic = result['userids']
            if not userdic:
                userdic = {}
            if self.userid in userdic.keys():
                if userdic[self.userid] == self.reaction:
                    del userdic[self.userid]
                    self.returnResult = -1
                else:
                    self.returnResult = +1
                    userdic[self.userid] = self.reaction
            else:
                self.returnResult = +1
                userdic[self.userid] = self.reaction
            collection.update_one(
                {
                    '_id' : result['_id']
                },
                {
                    '$set' : {
                        'userids' : userdic
                    }
                }
            )
        self.likeDislike = collection.find_one(msgQuery)['userids']
        self.like = 0
        self.dislike = 0
        for react in self.likeDislike:
            if self.likeDislike[react] == '👍':
                self.like += 1
            else:
                self.dislike += 1
        return self.like, self.dislike, self.returnResult


class ButtonTrigger:

    def __init__(self,
    callback : CallbackQuery
    ):
        self.callback = callback
    
    @classmethod
    async def create(
        cls,
        callback : CallbackQuery
        ):
        self = ButtonTrigger(callback)
        await self.start()
        return self

    async def start(self):
        self.data = self.callback.data.split(' ')
        if len(self.data) == 2:
            self.reaction, _ = self.data
        else:
            self.reaction = self.data[0]
        self.cdb = CheckingDB(
            self.callback.message.message_id,
            str(self.callback.from_user.id),
            self.reaction
        )
        self.like, self.dislike, self.returnResult = self.cdb.start()
        if self.returnResult == +1:
            await self.callback.answer(
                f"You give {self.reaction}"
            )
        else:
            await self.callback.answer(
                f"You took {self.reaction} back"
            )
        try:
            await self.callback.edit_message_reply_markup(
                InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                f"👍 {self.like}",
                                callback_data = f"👍"
                            ),
                            InlineKeyboardButton(
                                f"👎 {self.dislike}",
                                callback_data = "👎"
                            )
                        ]
                    ]
                )
            )
        except bad_request_400.MessageNotModified:
            pass
        



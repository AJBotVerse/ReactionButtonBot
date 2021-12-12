#!/usr/bin/env python3


### Importing
from pymongo import MongoClient
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
            returnValue = +1
        else:
            userdic = result['userids']
            if not userdic:
                userdic = {}
            if self.userid in userdic.keys():
                if userdic[self.userid] == self.reaction:
                    del userdic[self.userid]
                    returnValue = -1
                else:
                    userdic[self.userid] = self.reaction
                    returnValue = 0
            else:
                userdic[self.userid] = self.reaction
                returnValue = +1
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
        return returnValue

        


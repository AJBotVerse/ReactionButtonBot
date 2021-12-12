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


### Class
class ButtonTrigger:

    def __init__(self):
        pass


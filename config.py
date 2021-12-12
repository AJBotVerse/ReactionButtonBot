#!/usr/bin/env python3


### Importing
from os import environ


### Environment Variables
class Config(object):
    BOT_TOKEN = environ.get("BOT_TOKEN", "")
    
    APP_ID = int(environ.get("API_ID", 12345))
    
    API_HASH = environ.get("API_HASH", "")
    
    CHANNEL_ID = int(environ.get("CHANNEL_ID", None))

    MONGO_STR = environ.get("MONGO_STR", "")


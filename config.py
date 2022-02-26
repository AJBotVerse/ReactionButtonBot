#!/usr/bin/env python3


### Importing
from os import environ


### Environment Variables
class Config(object):
    BOT_TOKEN = environ.get("BOT_TOKEN", "")
    
    APP_ID = int(environ.get("API_ID", 12345))
    
    API_HASH = environ.get("API_HASH", "")
    
    channel_id = environ.get("CHANNEL_ID", None)
    if ',' in auth_channel:
        CHANNEL_ID = list(map(int, list(channel_id.split(','))))
    else:
        CHANNEL_ID = int(channel_id)

    MONGO_STR = environ.get("MONGO_STR", "")


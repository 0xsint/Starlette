import nextcord
from nextcord import *
from nextcord.ui import Button, button, View
from dotenv import load_dotenv
import os
from requests import post, get, patch, delete
import string
from nextcord.ext import application_checks
import threading
from PIL import ImageColor
from datauri import DataURI
from uuid import uuid4
from nextcord.ext.commands import Bot
from nextcord.ext import commands
import nextcord.utils
import nextcord
import pymongo
import random
import requests
import json
import asyncio
from time import perf_counter
import psutil
load_dotenv()
client = Bot("!!/", help_command=None, intents=Intents.all())
mongodb = pymongo.MongoClient(os.getenv("MONGODB"))
db = mongodb.starlight
cogs = []
for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        cogs.append("cogs." + filename[:-3])
if __name__ == '__main__':
    for cog in cogs:
        client.load_extension(cog)
        print (cog)
@client.event
async def on_ready():
    print (f"Client {client.user.id} ready!")
    db.bump_sl.delete_many({})
    col = db.levels_sleep
    col.delete_many({})
    col = db.command_sleep
    col.delete_many({})
    col = db.answered_users
    col.delete_many({})
    col = db.pick_sleep
    col.delete_many({})
client.run(os.getenv("TOKEN"))
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
import nextcord
import asyncio
load_dotenv()
mongodb = pymongo.MongoClient(os.getenv("MONGODB"))
db = mongodb.starlight
fp = open("cogs/CONF", "r").read()
conf = json.loads(fp)
class royalty(commands.Cog):
    def __init__(self, client) -> None:
        self.client = client
    @nextcord.slash_command(name="royalty", description="Purge the current messages")
    @application_checks.has_guild_permissions(administrator=True)
    async def royalty(self,ctx: Interaction):
        res = db.config.find_one({"value":"royalty", "guild": ctx.guild.id})
        if ctx.channel.id ==  res['channel']:
                for result in db.reactions.find({}):
                        messa = await ctx.channel.fetch_message(result['message_id'])
                        if messa:
                                await messa.delete()
                db.reactions.delete_many({})
                await ctx.response.send_message(embed=Embed(title="Server royalty purged", color=0xff00ff), ephemeral=True)
    @royalty.error
    async def royalty_Err(self, ctx: Interaction, error):
        if isinstance(error, application_checks.ApplicationMissingPermissions):
            await ctx.response.send_message(content="You don't have to permission to execute this command.")
        print (error)
def setup(client):
    client.add_cog(royalty(client))

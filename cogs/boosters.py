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
class boosters(commands.Cog):
    def __init__(self, client) -> None:
        self.client = client
    @nextcord.slash_command(name="cr", description="Custom role for boosters")
    async def cr(self,ctx: Interaction, color: str = SlashOption(name="color", description="Color of your role", required=False),role_name: str = SlashOption(name="role_name", description="The name you want your role", required=False)):
        col = db.authorized_users
        if col.find_one({"member_id": ctx.user.id}):
                result = col.find_one({"member_id": ctx.user.id})
                if not result['role_id']:
                        color = ImageColor.getcolor(color, "RGB")
                        role = await ctx.guild.create_role(name=role_name, colour=nextcord.Colour.from_rgb(r=color[0], g=color[1], b=color[2]), hoist=False, mentionable=False)
                        await role.edit(position=len(ctx.guild.roles)-3)
                        await ctx.user.add_roles(role)
                        col.update_one({"member_id": ctx.user.id}, {"$set": {"role_id": role.id}})
                        await ctx.response.send_message(embed=nextcord.Embed(description=f"{role.mention} created and given cutie! from now on you will type /cr", color=0xdea5a4))
                        return
                if result['role_id']:
                        color = ImageColor.getcolor(color, "RGB")
                        role = ctx.guild.get_role(result['role_id'])
                        await role.edit(name=role_name, colour=nextcord.Colour.from_rgb(r=color[0], g=color[1], b=color[2]), hoist=False, position=len(ctx.guild.roles)-3)
                        await ctx.response.send_message(embed=nextcord.Embed(description=f"{role.mention} edited with your given color and name cutie!", color=0xdea5a4))
                        return
    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        col = db.authorized_users
        if not before.premium_since and after.premium_since:
                if col.find_one({"member_id": after.id}):
                        return
                else:
                        col.insert_one({"member_id": after.id, "role_id": None})
def setup(client):
    client.add_cog(boosters(client))
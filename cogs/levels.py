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
class levels(commands.Cog):
    def __init__(self, client) -> None:
        self.client = client
    @nextcord.slash_command(name="level", description="Check a level of a user")
    async def level(self, ctx: Interaction, user: Member = SlashOption(required=False, name="user", description="User to check level of")):
        if not user:
            user = ctx.user
        result = db.levels.find_one({"member": user.id, "guild": ctx.guild.id})
        if not result:
            await ctx.response.send_message(embed=Embed(title="Unable to find level of user.", color=0xdea5a4))
            return
        exp = int(result['exp'])
        level = int(result['level'])
        math =round(exp//100)
        bar = None
        if math < 10:
            bar = "[----------]"
        elif math >= 10:
            bar = "[ღ---------]"
        elif math >= 20:
            bar = "[ღღ--------]"
        elif math >= 30:
            bar = "[ღღღ-------]"
        elif math >= 40:
            bar = "[ღღღღ------]"
        elif math >= 50:
            bar = "[ღღღღღ-----]"
        elif math >= 60:
            bar = "[ღღღღღღ----]"
        elif math >= 70:
            bar = "[ღღღღღღღ---]"
        elif math >= 80:
            bar = "[ღღღღღღღღ--]"
        elif math >= 90:
            bar = "[ღღღღღღღღღ-]"
        elif math >= 100:
            bar = "[ღღღღღღღღღღ]"
        await ctx.response.send_message(embed=nextcord.Embed(description=f"**Hey Cutie! {user.mention}'s level is ``{level}``**\r\n **with a total amount of XP earned: ``{exp}`` XP!**\r\n **They are also ``{math}%`` to their next level! Can't wait!**", color=0xdea5a4).set_footer(text=f"{bar} is the progress bar!"))
    @application_checks.has_guild_permissions(administrator=True)
    @level.subcommand(name="reward", description="Level rewarding")
    async def reward(self, ctx: Interaction, level: int = SlashOption(name="level", description="Level to get reward", required=True), reward: Role = SlashOption(required=True, description="Role to reward")):
        db.levels_reward.insert_one({"role": reward.id, "level": level, "guild": ctx.guild.id})
        await ctx.response.send_message(embed=Embed(title=f"Level Reward for {level}", description=f"Level {level} will now grant the role {role.mention}", color=0xdea5a4))
    @nextcord.slash_command(name="delete", description="Delete function")
    @application_checks.has_guild_permissions(administrator=True)
    async def delete(self, ctx: Interaction):
        pass
    @delete.subcommand(name="reward", description="Delete a level reward")
    @application_checks.has_guild_permissions(administrator=True)
    async def del_reward(self, ctx: Interaction, role: int = SlashOption(name="role_id", description="Role ID to delete", required=True), level: int = SlashOption(name="level", description="Level unlocked", required=False)):
        result = db.levels_reward.find_one_and_delete({"$or" [{"guild": ctx.guild.id, "role": role}, {"guild": ctx.guild.id, "role": role, "level": level}]})
        await ctx.response.send_message(embed=Embed(title=f"Role ID {role}", description=f"Role ID {role} will no longer be unlocked at level {level}", color=0xdea5a4).set_footer(text="DELETE"))
def setup(client):
    client.add_cog(levels(client))
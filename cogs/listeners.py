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
from time import perf_counter
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
fp = open("cogs/CONF", "r").read()
conf = json.loads(fp)
mongodb = pymongo.MongoClient(os.getenv("MONGODB"))
db = mongodb.starlight
class listeners(commands.Cog):
    def __init__(self, client) -> None:
        self.client = client
    @commands.Cog.listener("on_message")
    async def on_message1(self,message):
        if message.author.bot:
            return
        if not message.guild:
            return
        res = db.currency.find_one({})
        currency = res['string']
        sleeps = db.levels_sleep.find_one({"member": message.author.id, "guild": message.guild.id})
        if sleeps:
            return
        result = db.levels.find_one({"member": message.author.id, "guild": message.guild.id})
        if not result:
            return
        level = result['level']
        exp = result['exp']
        new_exp = exp+25
        lvl_end = int(new_exp/100)
        if level < lvl_end:
            level = lvl_end
            db.levels.update_one({"member": message.author.id, "guild": message.guild.id}, {"$set": {"level": level, "exp": 25}})
            for doc in db.levels_reward.find({"guild": message.guild.id}):
                if level >= doc['level']:
                    role = message.guild.get_role(doc['role'])
                    await message.author.add_roles(role)
            res = db.config.find_one({"value": "levels", "guild": message.guild.id})
            chan = self.client.get_channel(res['channel'])
            bal = 0
            for i in range(0, level):
                bal += 50
            requests.patch(f"https://unbelievaboat.com/api/v1/guilds/{message.guild.id}/users/{message.author.id}", headers={"Authorization":os.getenv("UNVB"), "Content-Type": "application/json", "accept": "application/json"}, json={"bank": bal})
            await chan.send(content=message.author.mention, embed=nextcord.Embed(title=f"Level up!", description=f"Congratulations {message.author.mention}!~ You have leveled up to level {level}! :3", color=0xdea5a4).add_field(name="You have also earned", value=f"**{bal}  {currency} from leveling up!! Keep up the good work!**", inline=True))
            return
        db.levels.update_one({"member": message.author.id, "guild": message.guild.id}, {"$inc": {"exp": 25}})
    @commands.Cog.listener("on_message")
    async def on_message2(self, message):
        if message.author.bot:
            return
        if db.levels.find_one({"member": message.author.id, "guild": message.guild.id}):
            return
        db.levels.insert_one({"member": message.author.id, "guild": message.guild.id, "level": 1, "exp": 0})
        db.answered.insert_one({"member": message.author.id, "guild": message.guild.id, "answers": 0})
        return
    @commands.Cog.listener("on_message")
    async def on_message3(self, message):
            
                    if message.author.bot:
                            return
                    if not message.guild:
                            return
                    res = db.config.find_one({"value": "aotd", "guild": message.guild.id})
                    if message.channel.id == res['channel']:
                            db = mongodb.starlight
                            col = db.currency
                            result = col.find_one({})
                            currency = result['string']
                            col = db.answered_users
                            result = col.find_one({"member": message.author.id, "guild": message.guild.id})
                            if result:
                                    return
                            randint = random.randrange(15, 30)
                            col = db.levels
                            new_exp = 100
                            r = requests.patch(f"https://unbelievaboat.com/api/v1/guilds/{message.guild.id}/users/{message.author.id}", headers={"Authorization":os.getenv("UNVB"), "Content-Type": "application/json", "accept": "application/json"}, json={"bank": randint})
                            balance = json.loads(r.text)
                            col.update_one({"member": message.author.id, "guild": message.guild.id}, {"$inc": {"exp": new_exp}})
                            col = db.answered
                            col.update_one({"member": message.author.id, "guild": message.guild.id}, {"$inc": {"answers": 1}})
                            col = db.answered_users
                            col.insert_one({"member": message.author.id, "guild": message.guild.id})
                            msg = await message.reply(embed=nextcord.Embed(title=f"{message.author.name}#{message.author.discriminator}", description=f"Thank you for answering the question of the day cutie! **You have earned {randint} {currency} for answering!**", color=0xdea5a4).add_field(name="Your balance is now", value=f"**{balance['bank']} {currency}**"))
                            await asyncio.sleep(85000)
                            await msg.delete()
                            col.delete_many({"member": message.author.id, "guild": message.guild.id})
    @commands.Cog.listener("on_reaction_add")
    async def on_reaction_add(self, reaction, user):
        if user.bot:
            return
        res = db.config.find_one({"value": "royalty", "guild": reaction.message.guild.id})
        mods = db.config.find_one({"value": "mods", "guild": reaction.message.guild.id})
        if reaction.message.channel.id == res['channel']:
            chan = self.client.get_channel(mods['channel'])
            stri = ""
            if reaction.emoji == "👸":
                stri = "princess"
            if reaction.emoji == "🤴":
                stri = "prince"
            if reaction.emoji == "👑":
                stri = "king"
            if reaction.emoji == "🌹":
                stri = "queen"
            if reaction.emoji == "🔥":
                stri = "themperor"
            if reaction.emoji == "🤹":
                stri = "jester"
            db.reactions.update_one({"member": reaction.message.author.id, "guild": reaction.message.guild.id}, {"$inc":{stri:1}})
            result = db.reactions.find_one({"member": reaction.message.author.id, "guild": reaction.message.guild.id})
            embed = Embed(description=f"**REACTIONS FOR {reaction.message.author.display_name} ({reaction.message.author.name}#{reaction.message.author.discriminator})**\r\n**Princess:** {result['princess']}\r\n**Prince:** {result['prince']}\r\n**King:** {result['king']}\r\n**Queen:** {result['queen']}\r\n**Themperor:** {result['themperor']}\r\n**Jester:** {result['jester']}", color=0xdea5a4).set_footer(text=f"Royalty User ID: {result['ruid']}")
            await chan.send(embed=embed)
    @commands.Cog.listener("on_message")
    async def on_message4(self, message):
        if message.author.bot:
            return
        res = db.config.find_one({"value": "royalty", "guild": message.guild.id})
        if message.channel.id == res['channel']:
            if message.attachments:
                reactions = ["👸", "🤴", "👑", "🌹", "🔥", "🤹"]
                for reaction in reactions:
                    await message.add_reaction(reaction)
                if db.reactions.find_one({"member": message.author.id}):
                    db.reactions.delete_many({"member": message.author.id, "guild": message.guild.id})
                db.reactions.insert_one({"member": message.author.id,"guild": message.guild.id,"message_id": message.id, "princess": 0, "prince": 0, "king": 0, "queen": 0, "themperor": 0, "jester": 0, "ruid": str(uuid4())})
    @commands.Cog.listener("on_reaction_remove")
    async def on_reaction_remove(self, reaction, user):
        if user.bot:
            return
        res = db.config.find_one({"value": "royalty", "guild": reaction.message.guild.id})
        mods = db.config.find_one({"value": "mods", "guild": reaction.message.guild.id})
        if reaction.message.channel.id == res['channel']:
                chan = self.client.get_channel(mods['channel'])
                stri = ""
                if reaction.emoji == "👸":
                        stri = "princess"
                if reaction.emoji == "🤴":
                        stri = "prince"
                if reaction.emoji == "👑":
                        stri = "king"
                if reaction.emoji == "🌹":
                        stri = "queen"
                if reaction.emoji == "🔥":
                        stri = "themperor"
                if reaction.emoji == "🤹":
                        stri = "jester"
                db.reactions.update_one({"member": reaction.message.author.id, "guild": reaction.message.guild.id}, {"$inc":{stri:-1}})
                result = db.reactions.find_one({"member": reaction.message.author.id, "guild": reaction.message.guild.id})
                embed = Embed(description=f"**REACTIONS FOR {reaction.message.author.display_name} ({reaction.message.author.name}#{reaction.message.author.discriminator})**\r\n**Princess:** {result['princess']}\r\n**Prince:** {result['prince']}\r\n**King:** {result['king']}\r\n**Queen:** {result['queen']}\r\n**Themperor:** {result['themperor']}\r\n**Jester:** {result['jester']}", color=0xdea5a4).set_footer(text=f"Royalty User ID: {result['ruid']}")
                await chan.send(embed=embed)
    @commands.Cog.listener("on_message")
    async def on_message5(self, message):
            channels = db.config.find_one({"guild": message.guild.id, "value": "selfies"})
            if message.channel.id in channels['channels']:
                if message.attachments:
                        reactions = ["🤩", "😍", "😅", "🥰", "💗", "💞", "💕", "❣️", "💖", "💝", "❤️", "🧡", "💛", "💚", "💙", "💜", "🤍", "🖤", "😘", "🤎"]
                        rand_react = random.choices(reactions, k=3)
                        print (rand_react)
                        await message.add_reaction(rand_react[0])
                        await message.add_reaction(rand_react[1])
                        await message.add_reaction(rand_react[2])
    @commands.Cog.listener("on_message")
    async def on_message6(self, message):
        res = db.config.find_one({"guild": message.guild.id, "value": "flash"})
        if message.channel.id != res['channel']:
                return
        if message.attachments:
                await asyncio.sleep(300)
                await message.delete()
    @commands.Cog.listener("on_message")
    async def on_message7(self, message):
        if message.author.bot:
                return
        db = mongodb.starlight
        col = db.message_store
        result = col.count_documents({})
        if result < random.randrange(20, 30):
                col.insert_one({"torf": True})
                return
        res = db.config.find_one({"guild": message.guild.id, "value": "pick"})
        chan = self.client.get_channel(res['channel'])
        col = db.currency
        result = col.find_one({"guild_id": f"{message.guild.id}"})
        currency = result['currency']
        col = db.pick_sleep
        if col.find_one({}):
                return
        col = db.balance
        x = 0
        members = []
        messages = []
        if message.channel.id != chan.id:
                return
        print (members)
        def check(m):
                return m.channel.id == message.channel.id and m.content.lower() == ".pick" and m.author.id not in members
        messa = await chan.send(embed=nextcord.Embed(description=f"***Someone dropped a handful of  {currency}!*** ***Type ``.pick`` in order to pick them up!***", color=0xffb6c1))
        db.pick_sleep.insert_one({"torf": True})
        start_time = perf_counter()
        while True:
                try:
                        mess = await self.client.wait_for('message', check=check, timeout=60.0)
                        if mess:
                                end_time = perf_counter()
                                real_time = end_time - start_time

                                result = col.find_one({"member_id": f"{mess.author.id}"})
                                balance = 0
                                await mess.delete()
                                members.append(mess.author.id)
                                i = random.randrange(100, 300)
                                balance += i
                                result = db.picktime.find_one({"member_id": mess.author.id, "guild": message.guild.id})
                                if not result:
                                        db.picktime.insert_one({"member_id": mess.author.id, "guild": message.guild.id, "time": real_time})
                                elif real_time < result['time']:
                                        db.picktime.update_one({"member_id": mess.author.id, "guild": message.guild.id}, {"$set": {"time": real_time}})
                                requests.patch(f"https://unbelievaboat.com/api/v1/guilds/{message.guild.id}/users/{message.author.id}", headers={"Authorization":os.getenv("UNVB"), "Content-Type": "application/json", "accept": "application/json"}, json={"bank": balance})
                                messag = await message.channel.send(embed=nextcord.Embed(description=f"***{mess.author.mention} has picked up {i}  {currency}!\r\nYour total pick time was {real_time:.2f} seconds!!***",color=0xffb6c1))
                                messages.append(messag.id)
                except TimeoutError as e:
                        print (e)
                        for message_id in messages:
                                message_id_over = await message.channel.fetch_message(message_id)
                                await message_id_over.delete()
                        await messa.delete()
                        col = db.pick_sleep
                        await asyncio.sleep(300)
                        col.delete_one({})
                        col = db.message_store
                        col.delete_many({"torf": True})
                
def setup(client):
    client.add_cog(listeners(client))
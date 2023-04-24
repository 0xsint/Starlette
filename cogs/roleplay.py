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
from time import perf_counter
import psutil
class roleplay(commands.Cog):
    def __init__(self, client) -> None:
        self.client = client
    @nextcord.slash_command(name="bite", description="Bite a user")
    async def bite(self,ctx: Interaction, user: Member = SlashOption(name="user", description="User to bite", required=True)):
        r = get("https://static.sorceress.online/sfw/bite/")
        image = json.loads(r.text)
        embed = Embed(color=0xdea5a4,description=f"***{ctx.user.mention} bites {user.mention}! Ouch!***\r\nRoleplay commands brought to you by [Lina](https://static.sorceress.online/docs)").set_image(url=image['path'])
        await ctx.response.send_message(embed=embed)
    @nextcord.slash_command(name="hug", description="Hug a user!")
    async def hug(self,ctx: Interaction, user: Member = SlashOption(name="user", description="User to hug", required=True)):
        r = get("https://static.sorceress.online/sfw/hug/")
        image = json.loads(r.text)
        embed = Embed(color=0xdea5a4,description=f"***{ctx.user.mention} hugs {user.mention} tightly! Awww!***\r\nRoleplay commands brought to you by [Lina](https://static.sorceress.online/docs)").set_image(url=image['path'])
        await ctx.response.send_message(embed=embed)
    @nextcord.slash_command(name="kiss", description="Kiss a user")
    async def kiss(self,ctx: Interaction, user: Member = SlashOption(name="user", description="User to kiss", required=True)):
        r = get("https://static.sorceress.online/sfw/kiss/")
        image = json.loads(r.text)
        embed = Embed(color=0xdea5a4,description=f"***{ctx.user.mention} kisses {user.mention} passionately! hawt***\r\nRoleplay commands brought to you by [Lina](https://static.sorceress.online/docs)").set_image(url=image['path'])
        await ctx.response.send_message(embed=embed)
    @nextcord.slash_command(name="cuddle", description="Cuddle a user tightly")
    async def cuddle(self,ctx: Interaction, user: Member = SlashOption(name="user", description="User to cuddle", required=True)):
        r = get("https://static.sorceress.online/sfw/cuddle/")
        image = json.loads(r.text)
        embed = Embed(color=0xdea5a4,description=f"***{ctx.user.mention} cuddles {user.mention} passionately! Cute!***\r\nRoleplay commands brought to you by [Lina](https://static.sorceress.online/docs)").set_image(url=image['path'])
        await ctx.response.send_message(embed=embed)
    @nextcord.slash_command(name="pet", description="Give a user lots of headpats")
    async def pet(self,ctx: Interaction, user: Member = SlashOption(name="user", description="User to headpat", required=True)):
        r = get("https://static.sorceress.online/sfw/headpat/")
        image = json.loads(r.text)
        embed = Embed(color=0xdea5a4,description=f"***{ctx.user.mention} gives {user.mention} lots of headpats! Cute!***\r\nRoleplay commands brought to you by [Lina](https://static.sorceress.online/docs)").set_image(url=image['path'])
        await ctx.response.send_message(embed=embed)
    @nextcord.slash_command(name="slap", description="Slap a user")
    async def slap(self,ctx: Interaction, user: Member = SlashOption(name="user", description="User to slap", required=True)):
        r = get("https://static.sorceress.online/sfw/slap/")
        image = json.loads(r.text)
        embed = Embed(color=0xdea5a4,description=f"***{ctx.user.mention} slaps {user.mention}! BAKA!***\r\nRoleplay commands brought to you by [Lina](https://static.sorceress.online/docs)").set_image(url=image['path'])
        await ctx.response.send_message(embed=embed)
    @nextcord.slash_command(name="poke", description="Poke a user")
    async def poke(self,ctx: Interaction, user: Member = SlashOption(required=True, description="User to poke")):
        r = get("https://static.sorceress.online/sfw/poke/")
        image = json.loads(r.text)
        embed = Embed(color=0xdea5a4,description=f"***{ctx.user.mention} pokes {user.mention}! Poke Poke***\r\nRoleplay commands brought to you by [Lina](https://static.sorceress.online/docs)").set_image(url=image['path'])
        await ctx.response.send_message(embed=embed)
    @nextcord.slash_command(name="blush", description="Blush cutely")
    async def blush(self,ctx: Interaction):
        r = get("https://static.sorceress.online/sfw/blush/")
        image = json.loads(r.text)
        embed = Embed(color=0xdea5a4,description=f"***{ctx.user.mention} blushes cutely! Awwww!***\r\nRoleplay commands brought to you by [Lina](https://static.sorceress.online/docs)").set_image(url=image['path'])
        await ctx.response.send_message(embed=embed)
    @nextcord.slash_command(name="wag", description="Wag your tail!")
    async def wag(self,ctx: Interaction):
        r = get("https://static.sorceress.online/sfw/wag/")
        image = json.loads(r.text)
        embed = Embed(color=0xdea5a4,description=f"***{ctx.user.mention} wags their tail! They must be excited!***\r\nRoleplay commands brought to you by [Lina](https://static.sorceress.online/docs)").set_image(url=image['path'])
        await ctx.response.send_message(embed=embed)
    @nextcord.slash_command(name="purr", description="Purrrfect!")
    async def purr(self,ctx: Interaction):
        r = get("https://static.sorceress.online/sfw/purr/")
        image = json.loads(r.text)
        embed = Embed(color=0xdea5a4,description=f"***{ctx.user.mention} purrs happily! :3***\r\nRoleplay commands brought to you by [Lina](https://static.sorceress.online/docs)").set_image(url=image['path'])
        await ctx.response.send_message(embed=embed)
    @nextcord.slash_command(name="cry", description="Cry because you're sad! ;-;")
    async def cry(self,ctx: Interaction):
        r = get("https://static.sorceress.online/sfw/cry/")
        image = json.loads(r.text)
        embed = Embed(color=0xdea5a4,description=f"***{ctx.user.mention} cries sadly...I hope they're okay!***\r\nRoleplay commands brought to you by [Lina](https://static.sorceress.online/docs)").set_image(url=image['path'])
        await ctx.response.send_message(embed=embed)
    @nextcord.slash_command(name="pout", description="....Hmph!")
    async def pout(self,ctx: Interaction):
        r = get("https://static.sorceress.online/sfw/pout/")
        image = json.loads(r.text)
        embed = Embed(color=0xdea5a4,description=f"***{ctx.user.mention} pouts! ...Hmph!***\r\nRoleplay commands brought to you by [Lina](https://static.sorceress.online/docs)").set_image(url=image['path'])
        await ctx.response.send_message(embed=embed)
    @nextcord.slash_command(name="boop", description="Boop a user")
    async def boop(self,ctx: Interaction, user: Member = SlashOption(required=True, name="user", description="User to boop")):
        r = get("https://static.sorceress.online/sfw/boop/")
        image = json.loads(r.text)
        embed = Embed(color=0xdea5a4,description=f"***{ctx.user.mention} boops {user.mention}'s snoot! Boop Boop!***\r\nRoleplay commands brought to you by [Lina](https://static.sorceress.online/docs)").set_image(url=image['path'])
        await ctx.response.send_message(embed=embed)
    @nextcord.slash_command(name="tickle", description="Tickle a user")
    async def tickle(self,ctx: Interaction, user: Member = SlashOption(required=True, name="user", description="User to tickle")):
        r = get("https://static.sorceress.online/sfw/tickle/")
        image = json.loads(r.text)
        embed = Embed(color=0xdea5a4,description=f"***{ctx.user.mention} tickles {user.mention}! They can't stop laughing!***\r\nRoleplay commands brought to you by [Lina](https://static.sorceress.online/docs)").set_image(url=image['path'])
        await ctx.response.send_message(embed=embed)
    
def setup(client):
    client.add_cog(roleplay(client))
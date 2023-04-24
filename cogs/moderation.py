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
class moderation(commands.Cog):
    def __init__(self, client) -> None:
        self.client = client
    @application_checks.has_guild_permissions(ban_members=True)
    @nextcord.slash_command(name="warn", description="warn a user")
    async def warn(self,ctx: Interaction, member: Member = SlashOption(required=True, description="User to warn"), message: str = SlashOption(name="reason",required=True, description="Reason for warn")):
        if member == ctx.user:
            await ctx.response.send_message(embed=Embed(description=f"Unable to add a warn to yourself!"))
            return
        if not message:
            message = "No reason specified for this warn"
        docs = db.warns.count_documents({"member": member.id, "guild": ctx.guild.id})
        docs += 1
        db.warns.insert_one({"member": member.id, "guild": ctx.guild.id, "reason": message, "wid":docs})
        text = message
        await ctx.response.send_message(embed=Embed(description=f"{member.mention} has been warned for **{text}**", color=0xff00ff).set_footer(text=f"Warn ID: {docs}"))
    @warn.error
    async def on_warn_err(self,ctx: Interaction, error):
        if isinstance(error, application_checks.ApplicationMissingPermissions):
            print (error)
            await ctx.response.send_message(embed=Embed(description="You don't have permission to execute this command.", color=0xff00ff))
            return
        print (error)        
    @application_checks.has_guild_permissions(ban_members=True)
    @nextcord.slash_command(name="removewarn", description="Remove a warn from a user")
    async def removewarn(self,ctx: Interaction, member: Member = SlashOption(required=True, name="user", description="User to remove warn from"), warn_id: int = SlashOption(required=True, name="warn_id", description="Warning ID to remove")):
        if not warn_id:
            await ctx.response.send_message(embed=Embed(title="Please specify a warning number.", color=0xff00ff))
            return
        if not member:
            await ctx.response.send_message(embed=Embed(title="Please specify a member to remove a warning from.", color=0xff00ff))
        if warn_id.startswith("#"):
            warn_id = warn_id.split("#")[1]
        result = db.warns.find_one({"member": member.id, "wid": int(warn_id), "guild": ctx.guild.id})
        if not result:
            await ctx.response.send_message(embed=Embed(description=f"Unable to find warn ID from {member.mention}.", color=0xff00ff))
            return
        db.warns.delete_one({"wid": int(warn_id), "member": member.id, "guild": ctx.guild.id})
        await ctx.response.send_message(embed=Embed(description=f"Removing warning ID {warn_id} from {member.mention}", color=0xff00ff))
    @removewarn.error
    async def on_remove_warn_err(self,ctx: Interaction, error):
        if isinstance(error, application_checks.ApplicationMissingPermissions):
            await ctx.response.send_message(embed=Embed(description="You don't have permission to execute this command.", color=0xff00ff))
            return
        print (error)
        await ctx.response.send_message(embed=Embed(description="Something went wrong with your command!", color=0xff00ff))
    @nextcord.slash_command(name="warns", description="Check a user's warns!")
    async def warns(self,ctx: Interaction, member: Member = SlashOption(required=False, description="User to check warns for")):
        if not member:
            member = ctx.user
        docs = db.warns.count_documents({"member": member.id, "guild": ctx.guild.id})
        embed=Embed(description=f"{member.mention} has been warned {docs} times!", color=0xff00ff)
        for result in db.warns.find({"member": member.id, "guild": ctx.guild.id}):
            embed.add_field(name=f"Warning #{result['wid']}", value=f"**Reason: {result['reason']}**", inline=True)
        await ctx.response.send_message(embed=embed)
    @application_checks.has_guild_permissions(manage_messages=True)
    @nextcord.slash_command(name="verify", description="Verify a user")
    async def verify(self,ctx: Interaction, member: Member = SlashOption(required=True, description="User to verify")):
            if not member:
                await ctx.response.send_message(embed=Embed(title="Please mention a member.", color=0xff00ff))
                return
            pick = db.config.find_one({"guild": ctx.guild.id, "value": "pick"})
            cross = db.config.find_one({"guild": ctx.guild.id, "value": "verified"})
            unv = db.config.find_one({"guild": ctx.guild.id, "value": "unverified"})
            result = cross['role']
            result2 = unv['role']
            if not result:
                await ctx.response.send_message(embed=Embed(description=f"***!!! NO ROLE FOUND CONTACT ADMINISTRATOR/DEVELOPER !!!***", color=0xff00ff))
                return
            role = ctx.guild.get_role(result)
            r = ctx.guild.get_role(result2)
            if not r:
                print ("err")
                return
            await member.add_roles(role)
            await member.remove_roles(r)
            await ctx.response.send_message(embed=Embed(description=f"""
        Congratulations {member.mention} youve been verified!!""", color=0xff00ff))
    @verify.error
    async def on_verify_err(self,ctx: Interaction, error):
        if isinstance(error, application_checks.ApplicationMissingPermissions):
            await ctx.response.send_message(embed=Embed(title="Uh oh! You don't have permission to use this command!", color=0xff00ff))
            return
        else:
            print (error)
            await ctx.response.send_message(embed=Embed(title="An unexepected error has occurred.", color=0xff00ff))
            return
    @application_checks.has_guild_permissions(manage_messages=True)
    @nextcord.slash_command(name="cross", description="Cross verify a user")
    async def cross(self, ctx: Interaction, member: Member = SlashOption(required=True, description="User to cross verify")):
        if not member:
            await ctx.response.send_message(embed=Embed(title="Please mention a member.", color=0xff00ff))
            return
        pick = db.config.find_one({"guild": ctx.guild.id, "value": "pick"})
        cross = db.config.find_one({"guild": ctx.guild.id, "value": "cross verified"})
        unv = db.config.find_one({"guild": ctx.guild.id, "value": "unverified"})
        chan = self.client.get_channel(pick['channel'])
        result = cross['role']
        result2 = unv['role']
        if not result:
            await ctx.response.send_message(embed=Embed(description=f"***!!! NO ROLE FOUND CONTACT ADMINISTRATOR/DEVELOPER !!!***", color=0xff00ff))
            return
        role = ctx.guild.get_role(result)
        r = ctx.guild.get_role(result2)
        if not r:
            print ("err")
            return
        await member.add_roles(role)
        await member.remove_roles(r)
        await ctx.response.send_message(embed=Embed(description=f"""
    Congratulations {member.mention} you've been cross verified!
    Once youve done those, come chat with us in {chan.mention}!""", color=0xff00ff))
    @cross.error
    async def on_verify_err(self,ctx: Interaction, error):
        if isinstance(error, application_checks.ApplicationMissingPermissions):
            await ctx.response.send_message(embed=Embed(title="Uh oh! You don't have permission to use this command!", color=0xff00ff))
            return
        else:
            print (error)
            await ctx.response.send_message(embed=Embed(title="An unexepected error has occurred.", color=0xff00ff))
            return
    @nextcord.slash_command(name="module", description="Module function")
    async def module(self, ctx: Interaction):
        pass
    @module.subcommand(name="update", description="Set a module")
    @application_checks.has_guild_permissions(administrator=True)
    async def set_module(self, ctx: Interaction, value: Literal["channel", "verify", "cross verify", "unverified", "selfies", "royalty", "aotd", "flash", "mods", "levels", "pick"] = SlashOption(name="key", description="Key to change", required=True), role: Role = SlashOption(required=False, description="role to set"), channel: TextChannel = SlashOption(description="Channel to set to", required=False)):
        if value == "selfies":
            result = db.config.find_one({"guild": ctx.guild.id, "value": "selfies"})
            if result:
                channels = []
                channels.append(result['channels'])
                channels.append(channel.id)
                db.config.update_one({"guild": ctx.guild.id, "value": "selfies"}, {"$set": {"channels": channels}})
            else:
                channels = []
                channels.append(channel.id)
                db.config.insert_one({"channels": channels, "value": "selfies", "guild": ctx.guild.id})
            await ctx.response.send_message(embed=Embed(title="Selfies list values updated successfully", color=0xdea5a4))
            return
        if role:
            if db.config.find_one({"guild": ctx.guild.id, "value": value}):
                
                db.config.update_one({"guild": ctx.guild.id, "value": value}, {"$set": {"role": role.id}})
            else:
                db.config.insert_one({"guild": ctx.guild.id, "value": value, "role": role.id})
        elif channel:
            if db.config.find_one({"guild": ctx.guild.id, "value": value}):
                
                db.config.update_one({"guild": ctx.guild.id, "value": value}, {"$set": {"channel": channel.id}})
            else:
                db.config.insert_one({"guild": ctx.guild.id, "value": value, "channel": channel.id})
        await ctx.response.send_message(embed=Embed(title="Value updated successfully", color=0xdea5a4))
    @module.subcommand(name="delete")
    @application_checks.has_guild_permissions(administrator=True)
    async def delete_module(self, ctx: Interaction, value: Literal["channel", "verify", "cross verify", "unverified", "selfies", "royalty", "aotd", "flash", "mods", "levels", "pick"] = SlashOption(name="key", description="Key to delete", required=True)):
        db.config.delete_one({"guild": ctx.guild.id, "value": value})
        await ctx.response.send_message(embed=Embed(title="Value deleted successfully", color=0xdea5a4))
def setup(client):
    client.add_cog(moderation(client))
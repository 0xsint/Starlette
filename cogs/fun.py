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
class fun(commands.Cog):
    def __init__(self, client) -> None:
        self.client = client
    @nextcord.slash_command(name="tinyname", description="Put little letters on your nickname!")
    async def tinyname(self, ctx: Interaction, text: str = SlashOption(name="name", description="Characters to put", required=True)):
            string = [{"a":"ᵃ"},{"b":"ᵇ"},{"c": "ᶜ"},{"d": "ᵈ"},{"e":"ᵉ"},{"f":"ᶠ"},{"g":"ᵍ"},{"h":"ʰ"},{"i":"ⁱ"},{"j":"ʲ"},{"k":"ᵏ"},{"l":"ˡ"},{"m":"ᵐ"},{"n":"ⁿ"},{"o":"ᵒ"},{"p":"ᵖ"},{"q":"ᑫ"},{"r":"ʳ"},{"s":"ˢ"},{"t": "ᵗ"},{"u":"ᵘ"},{"v":"ᵛ"},{"w":"ʷ"},{"x":"ˣ"},{"y":"ʸ"},{"z":"ᶻ"},{" ":" "}]
            orig = ""
            text = text.lower()
            for word in text:
                for stri in string:
                        for k, v in stri.items():
                                if k == word:
                                        orig += v
            try:
                print (orig)
                await ctx.user.edit(nick=f"{ctx.user.name} "+orig)
                await ctx.response.send_message(embed=nextcord.Embed(title="Your nick name has been added!", color=0xdea5a4))
            except Exception as e:
                print(e)
                await ctx.response.send_message(embed=nextcord.Embed(description=f"***Uh oh unable to set your nick name! Please make sure due to discord limits, Your nickname is 32 characters in length or that you're not the server owner.***", color=0xffb6c1))
    @nextcord.slash_command(name="flip", description="Flip a coin to see if you win!")
    async def flip(self, ctx: Interaction, amount: str = SlashOption(name="amount", description="Amount to bet", required=True)):
            result = db.bet_sleeps.find_one({"member": ctx.user.id, "type": "flip"})
            if result:
                await ctx.response.send_message(embed=Embed(title="Cooldown", color=0xdea5a4, description=f"Uh oh you're on cooldown! Please wait ``{result['seconds']} seconds``!"))
                return
            curr = db.currency.find_one({})
            currency = curr['string']
            bet = 0
            if "-" in str(amount):
                await ctx.response.send_message(embed=Embed(title="Uh oh! You can't bet negatives!", color=0xdea5a4))
                return
            if "." in str(amount):
                await ctx.response.send_message(embed=Embed(title="Uh oh! You can't bet decimals!", color=0xdea5a4))
                return
            elif "+" in str(amount):
                await ctx.response.send_message(embed=Embed(title="Uh oh! You can't use this character to bet!", color=0xdea5a4))
                return
            elif int(amount) > 2000:
                await ctx.response.send_message(embed=Embed(title="Uh oh! You can only bet 2000 maximum!", color=0xdea5a4))
                return
            elif int(amount) == 0:
                await ctx.response.send_message(embed=Embed(title="Uh oh! You can't bet 0!", color=0xdea5a4))
                return
            else:
                bet += int(amount)
            r = requests.get(f"https://unbelievaboat.com/api/v1/guilds/{ctx.guild.id}/users/{ctx.user.id}", headers={"Authorization": os.getenv("UNVB"), "accept": "application/json"})
            balance = json.loads(r.text)
            if balance['bank'] < bet:
                await ctx.response.send_message(embed=Embed(title="Uh oh! You don't have enough to bet! ;-;", color=0xdea5a4))
                return
            winorlose = random.randrange(1, 100)
            if winorlose > 65:
                balance['bank'] -= bet
                req = requests.put(f"https://unbelievaboat.com/api/v1/guilds/{ctx.guild.id}/users/{ctx.user.id}", headers={"Authorization": os.getenv("UNVB"), "accept": "application/json", "content-type": "application/json"}, json={"bank": balance['bank'], "reason": "Starlette Update On Balance"})
                await ctx.response.send_message(embed=Embed(description=f"Uh oh cutie! You lost! {bet}  {currency} has been deducted from your bank! Your balance is now **{balance['bank']} ** {currency}", color=0xdea5a4))
            elif winorlose <= 65:
                balance['bank'] += bet
                req = requests.put(f"https://unbelievaboat.com/api/v1/guilds/{ctx.guild.id}/users/{ctx.user.id}", headers={"Authorization": os.getenv("UNVB"), "accept": "application/json", "content-type": "application/json"}, json={"bank": balance['bank'], "reason": "Starlette Update On Balance"})
                await ctx.response.send_message(embed=Embed(description=f"Congratulations cutie! You won! {bet}  {currency} has been added to your bank! Your balance is now **{balance['bank']} ** {currency}", color=0xdea5a4))
            else:
                await ctx.response.send_message(embed=Embed(description="Uh oh! It seems we've ran into an error! Don't worry it's not your fault cutie!", color=0xdea5a4))
            db.bet_sleeps.insert_one({"member": ctx.user.id, "type": "flip", "seconds": 10})
            num = 10
            while True:
                 await asyncio.sleep(1)
                 num -= 1
                 db.bet_sleeps.update_one({"member": ctx.user.id, "type": "flip"}, {"$set": {"seconds": num}})
                 if num == 0:
                     db.bet_sleeps.delete_many({"member": ctx.user.id, "type": "flip"})
                     break
    @nextcord.slash_command(name="slots", description="Play slots to see if you win!")
    async def slots(self, ctx: Interaction, amount: int = SlashOption(name="amount", description="Amount to bet", required=True)):
            result = db.bet_sleeps.find_one({"member": ctx.user.id, "type": "slots"})
            if result:
                await ctx.response.send_message(embed=Embed(title="Cooldown", color=0xdea5a4, description=f"Uh oh you're on cooldown! Please wait ``{result['seconds']} seconds``!"))
                return
            curr = db.currency.find_one({})
            currency = curr['string']
            bet = 0
            if "-" in str(amount):
                await ctx.response.send_message(embed=Embed(title="Uh oh! You can't play slots with negatives!", color=0xdea5a4))
                return
            if "." in str(amount):
                await ctx.response.send_message(embed=Embed(title="Uh oh! You can't play slots with decimals!", color=0xdea5a4))
                return
            if "+" in str(amount):
                await ctx.response.send_message(embed=Embed(title="Uh oh! You can't have this character when playing slots!", color=0xdea5a4))
                return
            elif int(amount) < 50:
                await ctx.response.send_message(embed=Embed(title="Uh oh! The minimum you can bet play slots with is 50!", color=0xdea5a4))
                return
            if int(amount) == int(0):
                await ctx.response.send_message(embed=Embed(title="Uh oh! You can't play slots with only the amount of 0!", color=0xdea5a4))
                return
            else:
                bet += int(amount)
            balance = 0
            winorlose = ["❌","✅"]
            choi = random.choices(winorlose, k=3)
            win = 0
            lose = 0
            string = ""
            for res in choi:
                if res == "✅":
                    string += res
                    win += 1
                elif res == "❌":
                    string += res
            msg = await ctx.response.send_message(f"***You play slots and land on...***\r\n\r\n{string}")
            embed = Embed(description=f"***Slots to earn  {currency}***", color=0xdea5a4)
            if win == 0:
                balance -= bet
                r = requests.patch(f"https://unbelievaboat.com/api/v1/guilds/{ctx.guild.id}/users/{ctx.user.id}", headers={"Authorization":os.getenv("UNVB"), "Content-Type": "application/json", "accept": "application/json"}, json={"bank": balance, "reason": "Starlette Slots Update on balance"})
                js = json.loads(r.text)
                print (js)
                embed.add_field(name="You lost!", value=f"{bet}  {currency} has been deducted from your bank!", inline=False).set_footer(text=f"Your bank balance is now {js['bank']}")
            if win == 1:
                balance -= bet
                r = requests.patch(f"https://unbelievaboat.com/api/v1/guilds/{ctx.guild.id}/users/{ctx.user.id}", headers={"Authorization":os.getenv("UNVB"), "Content-Type": "application/json", "accept": "application/json"}, json={"bank": balance, "reason": "Starlette Slots Update on balance"})
                js = json.loads(r.text)
                print (js)
                embed.add_field(name="You lost!", value=f"{bet}  {currency} has been deducted from your bank!", inline=False).set_footer(text=f"Your bank balance is now {js['bank']}")
            if win == 2:
                balance += bet
                r = requests.patch(f"https://unbelievaboat.com/api/v1/guilds/{ctx.guild.id}/users/{ctx.user.id}", headers={"Authorization":os.getenv("UNVB"), "Content-Type": "application/json", "accept": "application/json"}, json={"bank": balance, "reason": "Starlette Slots Update on balance"})
                js = json.loads(r.text)
                print (js)
                embed.add_field(name="You won!", value=f"{bet}  {currency} has been added to your bank!", inline=False).set_footer(text=f"Your bank balance is now {js['bank']}")
            if win == 3:
                balance += bet+100
                r = requests.patch(f"https://unbelievaboat.com/api/v1/guilds/{ctx.guild.id}/users/{ctx.user.id}", headers={"Authorization":os.getenv("UNVB"), "Content-Type": "application/json", "accept": "application/json"}, json={"bank": balance, "reason": "Starlette Slots Update on balance"})
                js = json.loads(r.text)
                print (js)
                embed.add_field(name="You won double!", value=f"{bet}  {currency} has been added to your bank plus 100 {currency}!", inline=False).set_footer(text=f"Your bank balance is now {js['bank']}")
            await msg.edit(embed=embed)
            db.bet_sleeps.insert_one({"member": ctx.user.id, "type": "slots", "seconds": 10})
            num = 10
            while num != 0:
                await asyncio.sleep(1)
                num -= 1
                db.bet_sleeps.update_one({"member": ctx.user.id, "type": "slots"}, {"$set": {"seconds": num}})
            if num == 0:
                db.bet_sleeps.delete_many({"member": ctx.user.id, "type": "slots"})
    @nextcord.slash_command(name="8ball", description="Ask the wise 8ball a question")
    async def eightball(self,ctx: Interaction, question: str = SlashOption(required=True, description="Question to ask")):
        choices = ["It is certain.", "It is decidedly so.", " Without a doubt.", "Yes definitely.", "You may rely on it.", "As I see it, yes.", "Most likely.", "Outlook good.", "Yes.", "Signs point to yes.", "Reply hazy, try again.", "Ask again later.", "Better not tell you now.", "Cannot predict now.", "Concentrate and ask again.", "Don't count on it.", "My reply is no.", "My sources say no.", "Outlook not so good.", "Very doubtful."]
        choice = random.choice(choices)
        if choice:
                await ctx.response.send_message(embed=Embed(title=f"{choice}", color=0xdea5a4))
    
def setup(client):
    client.add_cog(fun(client))
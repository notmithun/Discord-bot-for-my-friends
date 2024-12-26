from logging import Logger
from pathlib import Path
import discord
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv
import os
from sys import exit
from random import randint, choice
import json
import helper

load_dotenv(Path("./.env"))

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

@bot.event
async def on_ready():
    print(f"{bot.user} has connected to Discord!")
    try:
        print("Syncing commands...")
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} commands")
        print("Fetching commands...")
        commands = await bot.tree.fetch_commands()
        print(f"Loaded {len(commands)} commands")
    except Exception as e:
        print("Something went wrong :(")
        print(e)
        exit(1)

@bot.tree.command(name="quote", description="Replies with a random quote")
async def random_quote(user: discord.Interaction):
    qn = randint(0, 50)
    with open("quotes.json", "r") as f:
        quotes = json.load(f)
    await user.response.send_message("**"+quotes[str(qn)]+"**")
@bot.tree.command(name="help", description="Replies with a list of commands")
async def help(user: discord.Interaction):
    await user.response.send_message("""
# List of commands
## Random commands
**/clickonme_link** - Replies with a link to click on me
**/quote** - Replies with a random quote
**/funfact** - Replies with a fun fact

## Money commands
`/register` - Registers you to the money system
`/leaderboard` - Replies with the leaderboard
`/coinflip [amount] [heads/tails]` - Flips a coin with the amount of money you give
""")
@bot.tree.command(name="clickonme_link", description="Replies with a link to click on me")
async def memes(user: discord.Interaction):
    await user.response.send_message("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
@bot.tree.command(name="amisigma", description="You'll never know if ur the sigma...")
async def amisigma(user: discord.Interaction):
    if user.user.id == 1123219629066682452 or user.user.id == 925636508877209601:
        await user.response.send_message("**Yes, you are a sigma...**")
    elif user.user.id == 1122865740589047900:
        await user.response.send_message("Ofc not ur a freaking monkey 🐒 <@1122865740589047900>")
    else:
        await user.response.send_message(f"<@{user.user.id}> no, ur not a sigma :(")
@bot.tree.command(name="funfact", description="Replies with a fun fact")
async def funfact(user: discord.Interaction):
    ff = {
        "1": "Did u know people are human? 🤯🤯🤯",
        "2": "Did u know I'm bot? 🤯🤯🤯",
        "3": "Did u know I was created by <@925636508877209601>? 🤯🤯🤯",
        "4": "Did u know Im sigma? 🤯🤯🤯"
    }
    await user.response.send_message(f"**{ff[choice(["1", "2", "3", "4"])]}**")
@bot.tree.command(name="register", description="Registers you to the money system")
async def register(user: discord.Integration):
    id = user.user.id
    if helper.check(id):
        await user.response.send_message("❌ You are already registered.")
    
    else:
        with open("money.json", "r") as f:
            d = json.load(f)
        d[str(id)] = 500
        with open("money.json", "w") as f:
            json.dump(d, f)
        await user.response.send_message("✅ You have been registered to the money system.")
@bot.tree.command(name="coinflip", description="Flip a coin with how much money you give")
async def coinflip(user: discord.Integration, bet: int, headsortails: str):
    try:
        id = user.user.id
        m: int = 0
        with open("money.json", "r") as f:
            d = json.load(f)
            try:
                m = d[str(id)]
            except KeyError:
                await user.response.send_message("❌ Please run the register command before using the `coinflip` command")
        if bet == 0:
            await user.response.send_message("❌ You can't bet 0 coins")
        elif bet < 0:
            await user.response.send_message("❌ You can't bet negative coins")
        elif m == 0:
            await user.response.send_message("❌ You're broke. Please run regain to get some money")
        elif bet > m:
            await user.response.send_message("❌ You don't have enough money")
        else:
            flip = choice(["heads", "tails"])
            if flip == headsortails:
                m += bet
                d[str(id)] = m
                with open("money.json", "w") as f:
                    json.dump(d, f)
                await user.response.send_message(f"😊 You won! You now have {m} coins")
            else:
                m -= bet
                d[str(id)] = m
                with open("money.json", "w") as f:
                    json.dump(d, f)
                await user.response.send_message(f"🙁 You lost! You now have {m} coins")
    except Exception as e:
        print(e)
        await user.response.send_message("❌ Something went wrong 🙁.\n\nError code:\n```" + str(e) + "```")
@bot.tree.command(name="money", description="Tells you how much money you have")
async def money(user: discord.Integration):
    with open("money.json", "r") as f:
        d = json.load(f)
        try:
            m = d[str(user.user.id)]
            await user.response.send_message(f"You have {m} coins")
        except KeyError:
            await user.response.send_message("Please run the register command before using the `money` command")
@bot.tree.command(name="regain", description="Gives you some money. Only works if you have 0 coins")
async def regain(user: discord.Integration):
    with open("money.json", "r") as f:
        d = json.load(f)
        try:
            m = d[str(user.user.id)]
            if m == 0:
                d[str(user.user.id)] = 100
                with open("money.json", "w") as f:
                    json.dump(d, f)
                await user.response.send_message("You have been given 100 coins")
            else:
                await user.response.send_message("You already have money")
        except KeyError:
            await user.response.send_message("Please run the register command to get your starter money")

@bot.tree.command(name="leaderboard", description="Replies with the leaderboard")
async def leaderboard(user: discord.Integration):
    with open("money.json", "r") as f:
        d = json.load(f)
        l = sorted(d.items(), key=lambda x: x[1], reverse=True)
        s = ""
        for i in l:
            s += f"<@{i[0]}> - {i[1]}\n"
        await user.response.send_message(f"```{s}```")
@bot.tree.command(name="slotmachine", description="A slot machine. If you win you get double the money you bet.")
async def slotmachine(user: discord.Integration, bet: int):
    s1 = ["🍎", "🍊", "🍇"]
    s2 = ["🍊", "🍎", "🍇"]
    s3 = ["🍇", "🍎", "🍊"]
    s = [s1, s2, s3]
    m = 0
    with open("money.json", "r") as f:
        d = json.load(f)
        try:
            m = d[str(user.user.id)]
        except KeyError:
            await user.response.send_message("❌ Please run the register command before using the `slotmachine` command")
    if bet == 0:
        await user.response.send_message("❌ You can't bet 0 coins")
    elif bet < 0:
        await user.response.send_message("❌ You can't bet negative coins")
    elif m == 0:
        await user.response.send_message("❌ You're broke. Please run `regain` to get some money")
    elif bet > m:
        await user.response.send_message("❌ You don't have enough money")
    else:
        c =  choice(s)[0]
        c2 = choice(s)[1]
        c3 = choice(s)[2]
        if c == c2 == c3:
           m += bet * 2
           d[str(user.user.id)] = m
           with open("money.json", "w") as f:
               json.dump(d, f)
           await user.response.send_message(f"Combination: {c}, {c2}, {c3}\n\n😊 You won! You now have {m} coins")
        else:
           m -= bet
           d[str(user.user.id)] = m
           with open("money.json", "w") as f:
               json.dump(d, f)
           await user.response.send_message(f"Combination: {c}, {c2}, {c3}\n\n🙁 You lost! You now have {m} coins")
@bot.tree.command(name="buyrole", description="Buy a role. Specify the role id")
async def buyrole(user: discord.Integration, role_id: int, confirm: bool=True):
    if not confirm:
        await user.response.send_message("❌ Are you sure you want to buy this role? Type `True` to confirm")
        return
    cost = 0
    if role_id == 1:
        cost = 100000
        role = discord.utils.get(user.guild.roles, id=1321375239745175563)
    elif role_id == 2:
        cost = 75000
        role = discord.utils.get(user.guild.roles, id=1321375708894724136)
    elif role_id == 3:
        cost = 50000
        role = discord.utils.get(user.guild.roles, id=1321375144677081108)
    elif role_id == 4:
        cost = 25000
        role = discord.utils.get(user.guild.roles, id=1321373891746332702)
    elif role_id == 5:
        cost = 10000
        role = discord.utils.get(user.guild.roles, id=1321372566987866152)
    elif role_id == 6:
        cost = 4500
        role = discord.utils.get(user.guild.roles, id=1321374037750054913)
    with open("money.json", "r") as f:
        d = json.load(f)
        try:
            m = d[str(user.user.id)]
        except KeyError:
            await user.response.send_message("❌ Please run the register command before using the `buyrole` command")
    if m < cost:
        await user.response.send_message("❌ You don't have enough money to buy this role")
    else:
        d[str(user.user.id)] -= cost
        await user.user.add_roles(role)
        await user.response.send_message(f"✅ You have successfully bought the role!\n\nNow you have a {d[str(user.user.id)]} coins left")
        with open("money.json", "w") as f:
            json.dump(d, f)
@bot.tree.command(name="roleinfo", description="Replies with information about a role")
async def roleinfo(user: discord.Integration):
    await user.response.send_message("""
## Role information
### <@&1321375239745175563>
- **Cost:** 100,000 coins
- **Role ID (asked when buying):** 1
### <@&1321375708894724136>
- **Cost:** 75,000 coins
- **Role ID (asked when buying):** 2
### <@&1321375144677081108>
- **Cost:** 50,000 coins
- **Role ID (asked when buying):** 3
### <@&1321373891746332702>
- **Cost:** 25,000 coins
- **Role ID (asked when buying):** 4
### <@&1321372566987866152>
- **Cost:** 10,000 coins
- **Role ID (asked when buying):** 5
### <@&1321374037750054913>
- **Cost:** 4,500 coins
- **Role ID (asked when buying):** 6
""")

bot.run(os.getenv("DISCORD_TOKEN"))
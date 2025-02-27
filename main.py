import os

import nextcord
from dotenv import load_dotenv
from nextcord.ext import commands

load_dotenv()
bot = commands.Bot(intents=nextcord.Intents.all())

bot.load_extension("cogs.responses")
print("Loaded cogs.responses")
bot.load_extension("cogs.gemini")
print("Loaded cogs.gemini")
bot.load_extension("cogs.roll")
print("Loaded cogs.roll")
bot.load_extension("cogs.phubcomment")
print("Loaded cogs.phcomment")
bot.load_extension("cogs.achievement")
print("Loaded cogs.achievement")
bot.load_extension("cogs.snipe")
print("Loaded cogs.snipe")

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")
    await bot.change_presence(activity=nextcord.Activity(type=nextcord.ActivityType.watching, name="pamak"))

bot.run(os.getenv("TOKEN"))
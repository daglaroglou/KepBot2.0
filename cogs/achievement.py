import requests
import nextcord
from nextcord.ext import commands
import io
import os
import random

class Achievemnt(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(name="achievement", description="Generate a Minecraft achievement image.")
    async def achievement(self, ctx: nextcord.Interaction, text: str):
        await ctx.response.defer()
        
        url = f"https://minecraftskinstealer.com/achievement/{random.randint(1, 39)}/Achievement%20Get!/{text}"
        headers = {
            "Content-Type": "application/json"
        }
        
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            image_data = io.BytesIO(response.content)
            await ctx.followup.send(file=nextcord.File(image_data, "achievement.png"))
        else:
            await ctx.followup.send("Erh... Something went wrong.")

def setup(bot):
    bot.add_cog(Achievemnt(bot))
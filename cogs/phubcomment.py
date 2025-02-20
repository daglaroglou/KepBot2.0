import requests
import nextcord
from nextcord.ext import commands
import io
import os

class PHComment(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(name="phcomment", description="Generate a PH comment image.")
    async def phcomment(self, ctx: nextcord.Interaction, user: nextcord.Member, text: str):
        await ctx.response.defer()
        
        image_url = user.avatar.url.replace(".webp", ".png")
        username = user.name
        
        url = f"https://nekobot.xyz/api/imagegen?type=phcomment&image={image_url}&text={text}&username={username}&raw=1"
        headers = {
            "Content-Type": "application/json"
        }
        
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            image_data = io.BytesIO(response.content)
            await ctx.followup.send(file=nextcord.File(image_data, "phcomment.png"))
        else:
            await ctx.followup.send("Erh... Something went wrong lil horny.")

def setup(bot):
    bot.add_cog(PHComment(bot))
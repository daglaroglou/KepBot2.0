import nextcord
from nextcord.ext import commands

import random

class Roll(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(name="roll", description="Roll a die.")
    async def roll(self, ctx: nextcord.Interaction, sides: int):
        if sides < 0:
            await ctx.response.send_message("Impossible die.", ephemeral=True)
        else:
            die = random.randrange(sides) + 1
            await ctx.response.send_message(f"Rolled {die}!")
        

def setup(bot):
    bot.add_cog(Roll(bot))
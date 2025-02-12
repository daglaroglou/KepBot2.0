import nextcord
from nextcord.ext import commands

class Responses(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.dynamic_responses = {}

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return
        if message.content.lower() in self.dynamic_responses:
            await message.reply(self.dynamic_responses[message.content.lower()])
        await self.bot.process_commands(message)

    @nextcord.slash_command(name="responses", description="Vale neo response.")
    async def responses(self, ctx: nextcord.Interaction, text: str, response: str):
        self.dynamic_responses[text.lower()] = response
        await ctx.response.send_message(f"Prostethike: '{text}' -> '{response}'")

def setup(bot):
    bot.add_cog(Responses(bot))
import os
import aiosqlite
import nextcord
from nextcord.ext import commands

class Responses(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db_path = os.path.join(os.path.dirname(__file__), "responses.db")

    async def cog_load(self):
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(
                "CREATE TABLE IF NOT EXISTS responses (text TEXT PRIMARY KEY, response TEXT)"
            )
            await db.commit()

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return
        if "sex" in message.content.lower():
            await message.reply("https://cdn.discordapp.com/attachments/712293922872754196/1282410030427013282/VID_40020710_172718_406.mp4?ex=67ae3c69&is=67aceae9&hm=fdd4546e295c31901d697ea952fbab442ed5afd629a3673492fe114a483eac6e")
        async with aiosqlite.connect(self.db_path) as db:
            async with db.execute("SELECT response FROM responses WHERE text = ?", (message.content.lower(),)) as cursor:
                row = await cursor.fetchone()
                if row:
                    await message.reply(row[0])
        await self.bot.process_commands(message)

    @nextcord.slash_command(name="responses", description="Add a new response.")
    async def responses(self, ctx: nextcord.Interaction, text: str, response: str):
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute("INSERT OR REPLACE INTO responses (text, response) VALUES (?, ?)", (text.lower(), response))
            await db.commit()
        await ctx.response.send_message(f":white_check_mark: Prostethike: '{text}' -> '{response}'", ephemeral=True)

    @commands.Cog.listener()
    async def on_ready(self):
        await self.cog_load()

def setup(bot):
    bot.add_cog(Responses(bot))
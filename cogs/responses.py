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

    @nextcord.slash_command(name="addresponse", description="Prosthikh neou response.")
    async def responses(self, ctx: nextcord.Interaction, text: str, response: str):
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute("INSERT OR REPLACE INTO responses (text, response) VALUES (?, ?)", (text.lower(), response))
            await db.commit()
        await ctx.response.send_message(f":white_check_mark: Prostethike: '{text}' -> '{response}'", ephemeral=True)

    @nextcord.slash_command(name="removeresponse", description="Afairesh response.")
    async def remove_response(self, ctx: nextcord.Interaction, text: str):
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute("DELETE FROM responses WHERE text = ?", (text.lower(),))
            await db.commit()
        await ctx.response.send_message(f":white_check_mark: Afairethike: '{text}'", ephemeral=True)

    @nextcord.slash_command(name="listresponses", description="Emfanish olwn twn responses.")
    async def list_responses(self, ctx: nextcord.Interaction):
        async with aiosqlite.connect(self.db_path) as db:
            async with db.execute("SELECT text, response FROM responses") as cursor:
                rows = await cursor.fetchall()
                if rows:
                    response_list = "\n".join([f"'{row[0]}' -> '{row[1]}'" for row in rows])
                    embed = nextcord.Embed(title="Responses", description=response_list)
                    embed.set_footer(text="KepBot V2")
                    embed.color = nextcord.Color.yellow()
                    await ctx.response.send_message(embed=embed, ephemeral=True)
                else:
                    await ctx.response.send_message("Den vrethikan responses.", ephemeral=True)

    @commands.Cog.listener()
    async def on_ready(self):
        await self.cog_load()

def setup(bot):
    bot.add_cog(Responses(bot))
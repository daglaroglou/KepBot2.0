import nextcord
from nextcord.ext import commands
from datetime import datetime

class Snipe(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.deleted_message = None
        self.deleted_author = None
        self.deleted_channel = None
        self.deleted_icon = None
        self.deleted_time = None
        self.message_time = None
        self.deleted_attachments = None

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        self.deleted_message = message.content
        self.deleted_author = str(message.author)
        self.deleted_channel = message.channel.name
        self.deleted_icon = message.author.avatar.url if message.author.avatar else None
        self.deleted_time = datetime.utcnow()
        self.message_time = message.created_at
        self.deleted_attachments = message.attachments

    @nextcord.slash_command(name="snipe", description="Snipe the last deleted message.")
    async def snipe(self, interaction: nextcord.Interaction):
        if self.deleted_message or self.deleted_attachments:
            embed = nextcord.Embed(title="Message Sniped", color=nextcord.Color.green())
            embed.set_author(name=self.deleted_author, icon_url=self.deleted_icon)
            embed.add_field(name="Message", value=self.deleted_message or "Image", inline=False)
            embed.add_field(name="Sent At", value=f"<t:{int(self.message_time.timestamp())}>", inline=True)
            embed.add_field(name="Deleted At", value=f"<t:{int(self.deleted_time.timestamp())}>", inline=True)
            embed.set_footer(text=f"In #{self.deleted_channel}")
            
            if self.deleted_attachments:
                for attachment in self.deleted_attachments:
                    embed.add_field(name="Attachment", value=attachment.url, inline=False)
            
            await interaction.response.send_message(embed=embed)
        else:
            embed = nextcord.Embed(title="*Cricket Noises*", description="There's nothing to snipe here...", color=nextcord.Color.red())
            await interaction.response.send_message(embed=embed)

def setup(bot):
    bot.add_cog(Snipe(bot))
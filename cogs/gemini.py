from google import genai
import nextcord
from nextcord.ext import commands
import os
from PIL import Image
import io
import asyncio

class Gemini(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(name="gemini", description="Gemini AI.")
    async def gemini(self, ctx: nextcord.Interaction, prompt: str, image: nextcord.Attachment = None):
        await ctx.response.defer()
        client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
        try:
            if not prompt:
                await ctx.followup.send("Prompt is required.", ephemeral=True)
                return
            if image:
                image_bytes = await image.read()
                pil_image = Image.open(io.BytesIO(image_bytes))
                response = client.models.generate_content(model="gemini-2.0-flash", contents=[prompt, pil_image])
            else:
                response = client.models.generate_content(model="gemini-2.0-flash", contents=[prompt])
        except Exception as e:
            await ctx.followup.send(f"Error: {e}", ephemeral=True)
            return

        response_text = response.text
        chunk_size = 2000
        chunks = [response_text[i:i + chunk_size] for i in range(0, len(response_text), chunk_size)]
        
        await ctx.followup.send(chunks[0])

        for chunk in chunks[1:]:
            await ctx.channel.send(chunk)

def setup(bot):
    bot.add_cog(Gemini(bot))
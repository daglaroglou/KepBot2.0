from google import genai
import nextcord
from nextcord.ext import commands
import os
from PIL import Image
import io

class Gemini(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(name="gemini", description="Gemini AI.")
    async def gemini(self, ctx: nextcord.Interaction, prompt: str, image: nextcord.Attachment = None):
        client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
        try:
            if not prompt:
                await ctx.response.send_message("Prompt is required.", ephemeral=True)
            if image:
                image_bytes = await image.read()
                pil_image = Image.open(io.BytesIO(image_bytes))
                response = client.models.generate_content(model="gemini-2.0-flash", contents=[prompt, pil_image])
            else:
                response = client.models.generate_content(model="gemini-2.0-flash", contents=prompt)
        except Exception as e:
            await ctx.response.send_message(f"Error: {e}", ephemeral=True)
        await ctx.response.send_message(response.text)

def setup(bot):
    bot.add_cog(Gemini(bot))
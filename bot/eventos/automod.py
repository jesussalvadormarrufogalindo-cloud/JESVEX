import discord
from discord.ext import commands
from collections import defaultdict
import time
PALABRAS = ["puto","pendejo","verga","mierda"]
spam = defaultdict(list)
class AutoMod(commands.Cog):
    def __init__(self, bot): self.bot = bot
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot: return
        if message.guild is None: return
        contenido = message.content.lower()
        for p in PALABRAS:
            if p in contenido:
                try:
                    await message.delete()
                    await message.channel.send(f"{message.author.mention} no digas groserias.", delete_after=5)
                except Exception: pass
                return
        ahora = time.time()
        spam[message.author.id].append(ahora)
        spam[message.author.id] = [t for t in spam[message.author.id] if ahora - t < 5]
        if len(spam[message.author.id]) >= 6:
            try:
                await message.channel.send(f"{message.author.mention} deja de hacer spam.", delete_after=5)
                spam[message.author.id] = []
            except Exception: pass
async def setup(bot): await bot.add_cog(AutoMod(bot))

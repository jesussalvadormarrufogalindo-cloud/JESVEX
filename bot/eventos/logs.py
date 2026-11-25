import discord
from discord.ext import commands
class Logs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if message.author.bot:
            return
        if message.guild is None:
            return
        canal = discord.utils.get(message.guild.text_channels, name="logs")
        if canal:
            embed = discord.Embed(title="Mensaje eliminado", description=f"Autor: {message.author.mention}\nCanal: {message.channel.mention}\nContenido: {message.content}", color=discord.Color.red())
            await canal.send(embed=embed)
    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if before.author.bot:
            return
        if before.guild is None:
            return
        if before.content == after.content:
            return
        canal = discord.utils.get(before.guild.text_channels, name="logs")
        if canal:
            embed = discord.Embed(title="Mensaje editado", description=f"Autor: {before.author.mention}\nCanal: {before.channel.mention}\nAntes: {before.content}\nAhora: {after.content}", color=discord.Color.orange())
            await canal.send(embed=embed)
async def setup(bot):
    await bot.add_cog(Logs(bot))

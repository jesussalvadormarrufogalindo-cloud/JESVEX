import discord
from discord import app_commands
from discord.ext import commands
class Anuncios(commands.Cog):
    def __init__(self, bot): self.bot = bot
    @app_commands.command(name="anuncio", description="Manda un anuncio")
    @app_commands.default_permissions(manage_messages=True)
    async def anuncio(self, interaction: discord.Interaction, canal: discord.TextChannel, texto: str):
        embed = discord.Embed(title="Anuncio", description=texto, color=discord.Color.gold())
        await canal.send(embed=embed)
        await interaction.response.send_message("Anuncio enviado.", ephemeral=True)
async def setup(bot): await bot.add_cog(Anuncios(bot))

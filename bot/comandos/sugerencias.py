import discord
from discord import app_commands
from discord.ext import commands
class Sugerencias(commands.Cog):
    def __init__(self, bot): self.bot = bot
    @app_commands.command(name="sugerencia", description="Manda una sugerencia")
    async def sugerencia(self, interaction: discord.Interaction, texto: str):
        canal = discord.utils.get(interaction.guild.text_channels, name="sugerencias") or interaction.channel
        embed = discord.Embed(title=f"Sugerencia de {interaction.user.display_name}", description=texto, color=discord.Color.green())
        await canal.send(embed=embed)
        await interaction.response.send_message("Sugerencia enviada!", ephemeral=True)
async def setup(bot): await bot.add_cog(Sugerencias(bot))

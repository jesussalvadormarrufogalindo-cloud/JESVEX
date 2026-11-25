import discord
from discord import app_commands
from discord.ext import commands
class Encuestas(commands.Cog):
    def __init__(self, bot): self.bot = bot
    @app_commands.command(name="encuesta", description="Crea una encuesta")
    async def encuesta(self, interaction: discord.Interaction, pregunta: str, opcion1: str, opcion2: str):
        embed = discord.Embed(title="Encuesta", description=pregunta, color=discord.Color.purple())
        embed.add_field(name="1", value=opcion1); embed.add_field(name="2", value=opcion2)
        await interaction.response.send_message(embed=embed)
        msg = await interaction.original_response()
        await msg.add_reaction("1️⃣"); await msg.add_reaction("2️⃣")
async def setup(bot): await bot.add_cog(Encuestas(bot))

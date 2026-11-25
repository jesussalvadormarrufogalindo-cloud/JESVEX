import discord
from discord import app_commands
from discord.ext import commands
class Info(commands.Cog):
    def __init__(self, bot): self.bot = bot
    @app_commands.command(name="serverinfo", description="Info del servidor")
    async def serverinfo(self, interaction: discord.Interaction):
        g = interaction.guild
        embed = discord.Embed(title=g.name, color=discord.Color.blue())
        embed.add_field(name="Miembros", value=str(g.member_count)); embed.add_field(name="Canales", value=str(len(g.channels))); embed.add_field(name="Creado", value=g.created_at.strftime("%d/%m/%Y"))
        if g.icon: embed.set_thumbnail(url=g.icon.url)
        await interaction.response.send_message(embed=embed)
    @app_commands.command(name="userinfo", description="Info de un usuario")
    async def userinfo(self, interaction: discord.Interaction, usuario: discord.Member = None):
        u = usuario or interaction.user
        embed = discord.Embed(title=u.display_name, color=discord.Color.blue()); embed.set_thumbnail(url=u.display_avatar.url); embed.add_field(name="ID", value=str(u.id)); embed.add_field(name="Se unio", value=u.joined_at.strftime("%d/%m/%Y") if u.joined_at else "N/A")
        await interaction.response.send_message(embed=embed)
    @app_commands.command(name="avatar", description="Ver avatar en grande")
    async def avatar(self, interaction: discord.Interaction, usuario: discord.Member = None):
        u = usuario or interaction.user
        embed = discord.Embed(title=f"Avatar de {u.display_name}"); embed.set_image(url=u.display_avatar.url)
        await interaction.response.send_message(embed=embed)
async def setup(bot): await bot.add_cog(Info(bot))

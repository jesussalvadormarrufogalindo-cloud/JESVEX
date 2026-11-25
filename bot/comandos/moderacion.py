import discord
from discord import app_commands
from discord.ext import commands
class Moderacion(commands.Cog):
    def __init__(self, bot): self.bot = bot
    @app_commands.command(name="expulsar", description="Expulsa a un usuario")
    @app_commands.default_permissions(kick_members=True)
    async def expulsar(self, interaction: discord.Interaction, usuario: discord.Member, motivo: str = "Sin motivo"):
        try: await usuario.kick(reason=motivo); await interaction.response.send_message(f"Se expulso a {usuario.mention}. Motivo: {motivo}")
        except Exception as e: await interaction.response.send_message(f"Error: {e}", ephemeral=True)
    @app_commands.command(name="banear", description="Banea a un usuario")
    @app_commands.default_permissions(ban_members=True)
    async def banear(self, interaction: discord.Interaction, usuario: discord.Member, motivo: str = "Sin motivo"):
        try: await usuario.ban(reason=motivo); await interaction.response.send_message(f"Se baneo a {usuario.mention}. Motivo: {motivo}")
        except Exception as e: await interaction.response.send_message(f"Error: {e}", ephemeral=True)
    @app_commands.command(name="desbanear", description="Desbanea por ID")
    @app_commands.default_permissions(ban_members=True)
    async def desbanear(self, interaction: discord.Interaction, user_id: str):
        try:
            u = await self.bot.fetch_user(int(user_id)); await interaction.guild.unban(u); await interaction.response.send_message(f"Se desbaneo a {u.mention}")
        except Exception as e: await interaction.response.send_message(f"Error: {e}", ephemeral=True)
    @app_commands.command(name="limpiar", description="Borra mensajes")
    @app_commands.default_permissions(manage_messages=True)
    async def limpiar(self, interaction: discord.Interaction, cantidad: int):
        if cantidad < 1 or cantidad > 100: await interaction.response.send_message("1 a 100", ephemeral=True); return
        await interaction.response.defer(ephemeral=True)
        b = await interaction.channel.purge(limit=cantidad)
        await interaction.followup.send(f"Se borraron {len(b)} mensajes.", ephemeral=True)
    @app_commands.command(name="silenciar", description="Silencia a un usuario")
    @app_commands.default_permissions(moderate_members=True)
    async def silenciar(self, interaction: discord.Interaction, usuario: discord.Member, minutos: int = 10):
        try:
            import datetime; await usuario.timeout(datetime.timedelta(minutes=minutos)); await interaction.response.send_message(f"{usuario.mention} silenciado {minutos} min.")
        except Exception as e: await interaction.response.send_message(f"Error: {e}", ephemeral=True)
    @app_commands.command(name="desilenciar", description="Quita el silencio")
    @app_commands.default_permissions(moderate_members=True)
    async def desilenciar(self, interaction: discord.Interaction, usuario: discord.Member):
        try:
            import datetime; await usuario.timeout(None); await interaction.response.send_message(f"{usuario.mention} ya puede hablar.")
        except Exception as e: await interaction.response.send_message(f"Error: {e}", ephemeral=True)
    @app_commands.command(name="advertir", description="Advierte a un usuario")
    @app_commands.default_permissions(kick_members=True)
    async def advertir(self, interaction: discord.Interaction, usuario: discord.Member, motivo: str = "Sin motivo"):
        await interaction.response.send_message(f"{usuario.mention} fue advertido. Motivo: {motivo}")
async def setup(bot): await bot.add_cog(Moderacion(bot))

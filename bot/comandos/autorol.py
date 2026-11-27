import discord
from discord.ext import commands
from discord import app_commands
import json
import os
import asyncio

if os.path.exists("/data"):
    RUTA = "/data/autorol.json"
else:
    RUTA = os.path.join(os.path.dirname(__file__), "autorol.json")

def cargar():
    if os.path.exists(RUTA):
        try:
            with open(RUTA, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return {}
    return {}

def guardar(datos):
    os.makedirs(os.path.dirname(RUTA), exist_ok=True)
    with open(RUTA, "w", encoding="utf-8") as f:
        json.dump(datos, f)

class Autorol(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="autorol", description="Pone que rol se les da al entrar: uno para usuarios y otro para bots")
    @app_commands.describe(rol_usuarios="OBLIGATORIO: Rol para los usuarios que entren", rol_bots="OBLIGATORIO: Rol para los bots que entren")
    async def autorol(self, interaction: discord.Interaction, rol_usuarios: discord.Role, rol_bots: discord.Role):
        if not interaction.user.guild_permissions.manage_roles:
            await interaction.response.send_message("No tienes permiso para usar esto.", ephemeral=True)
            return
        if rol_usuarios >= interaction.guild.me.top_role:
            await interaction.response.send_message(f"No puedo dar {rol_usuarios.mention}, esta mas arriba que mi rol.", ephemeral=True)
            return
        if rol_bots >= interaction.guild.me.top_role:
            await interaction.response.send_message(f"No puedo dar {rol_bots.mention}, esta mas arriba que mi rol.", ephemeral=True)
            return
        datos = cargar()
        datos[str(interaction.guild.id)] = {"usuarios": rol_usuarios.id, "bots": rol_bots.id}
        guardar(datos)
        await interaction.response.send_message(f"Listo, autorol guardado:\nUsuarios que entren: {rol_usuarios.mention}\nBots que entren: {rol_bots.mention}")

    @app_commands.command(name="dar-rol-a-todos", description="Le da un rol a todos los que ya estan en el servidor")
    @app_commands.describe(rol="Selecciona el rol que quieres dar", para="A quien se lo doy: usuarios, bots o todos")
    @app_commands.choices(para=[
        app_commands.Choice(name="Solo usuarios", value="usuarios"),
        app_commands.Choice(name="Solo bots", value="bots"),
        app_commands.Choice(name="Todos", value="todos"),
    ])
    async def dar_rol_a_todos(self, interaction: discord.Interaction, rol: discord.Role, para: app_commands.Choice[str]):
        if not interaction.user.guild_permissions.manage_roles:
            await interaction.response.send_message("No tienes permiso para usar esto.", ephemeral=True)
            return
        if rol >= interaction.guild.me.top_role:
            await interaction.response.send_message("No puedo dar ese rol, esta mas arriba que mi rol.", ephemeral=True)
            return
        await interaction.response.defer(ephemeral=True)
        dados = 0
        fallaron = 0
        for member in interaction.guild.members:
            if para.value == "usuarios" and member.bot:
                continue
            if para.value == "bots" and not member.bot:
                continue
            if rol in member.roles:
                continue
            try:
                await member.add_roles(rol)
                dados += 1
                await asyncio.sleep(0.5)
            except:
                fallaron += 1
        await interaction.followup.send(f"Listo, le di {rol.mention} a {dados} miembros. Fallaron {fallaron}.", ephemeral=True)

    @app_commands.command(name="quitar-autorol", description="Quita el autorol al entrar")
    async def quitar_autorol(self, interaction: discord.Interaction):
        if not interaction.user.guild_permissions.manage_roles:
            await interaction.response.send_message("No tienes permiso para usar esto.", ephemeral=True)
            return
        datos = cargar()
        if str(interaction.guild.id) in datos:
            del datos[str(interaction.guild.id)]
            guardar(datos)
            await interaction.response.send_message("Listo, ya quite el autorol al entrar.")
        else:
            await interaction.response.send_message("No habia ningun autorol puesto.", ephemeral=True)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        datos = cargar()
        config = datos.get(str(member.guild.id), {})
        if not config:
            return
        if member.bot:
            rol_id = config.get("bots")
        else:
            rol_id = config.get("usuarios")
        if not rol_id:
            return
        rol = member.guild.get_role(rol_id)
        if not rol:
            return
        try:
            await member.add_roles(rol)
        except:
            pass

async def setup(bot):
    await bot.add_cog(Autorol(bot))

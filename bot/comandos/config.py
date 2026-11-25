
import discord
from discord.ext import commands
from discord import app_commands
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from sistemas.db import get_config, save_config, get_niveles, save_niveles

def solo_admin(interaction):
    return interaction.user.guild_permissions.administrator or interaction.user.id == interaction.guild.owner_id

class Config(commands.Cog):
    def __init__(self, bot): self.bot = bot

    @app_commands.command(name="config-autorol", description="Elige que rol se da al entrar, sin pagina")
    @app_commands.describe(rol="El rol que se da, ej. JUGADOR")
    async def config_autorol(self, interaction, rol: discord.Role):
        if not solo_admin(interaction):
            await interaction.response.send_message("❌ Solo admins.", ephemeral=True); return
        c = get_config(); c["autorol_role"] = rol.name; c["autorol_role_id"] = str(rol.id); save_config(c)
        await interaction.response.send_message(f"✅ AutoRol guardado: {rol.mention} se dará al entrar.", ephemeral=True)

    @app_commands.command(name="config-logs", description="Elige el canal de logs, sin pagina")
    @app_commands.describe(canal="Donde llegan expulsiones, bans, etc")
    async def config_logs(self, interaction, canal: discord.TextChannel):
        if not solo_admin(interaction):
            await interaction.response.send_message("❌ Solo admins.", ephemeral=True); return
        c = get_config(); c["logs_channel_id"] = str(canal.id); save_config(c)
        await interaction.response.send_message(f"✅ Logs guardados en {canal.mention}", ephemeral=True)

    @app_commands.command(name="config-niveles-canal", description="Elige el canal donde avisa cuando subes de nivel")
    @app_commands.describe(canal="Canal de subidas de nivel")
    async def config_niveles_canal(self, interaction, canal: discord.TextChannel):
        if not solo_admin(interaction):
            await interaction.response.send_message("❌ Solo admins.", ephemeral=True); return
        c = get_config(); c["levels_channel_id"] = str(canal.id); save_config(c)
        await interaction.response.send_message(f"✅ Canal de niveles guardado en {canal.mention}", ephemeral=True)

    @app_commands.command(name="nivel-agregar", description="Agrega un rol para un nivel, uno por uno, sin pagina. Ej. nivel 5 -> rol X")
    @app_commands.describe(nivel="Cualquier nivel, ej. 5, 10, 15, 27", rol="Que rol se da al llegar a ese nivel")
    async def nivel_agregar(self, interaction, nivel: int, rol: discord.Role):
        if not solo_admin(interaction):
            await interaction.response.send_message("❌ Solo admins.", ephemeral=True); return
        n = get_niveles(); n.setdefault("level_roles", {})[str(nivel)] = rol.name; save_niveles(n)
        await interaction.response.send_message(f"✅ Nivel {nivel} -> {rol.mention} guardado.", ephemeral=True)

    @app_commands.command(name="nivel-quitar", description="Quita el rol de un nivel")
    @app_commands.describe(nivel="Que nivel quitas")
    async def nivel_quitar(self, interaction, nivel: int):
        if not solo_admin(interaction):
            await interaction.response.send_message("❌ Solo admins.", ephemeral=True); return
        n = get_niveles(); n.setdefault("level_roles", {}).pop(str(nivel), None); save_niveles(n)
        await interaction.response.send_message(f"✅ Nivel {nivel} quitado.", ephemeral=True)

    @app_commands.command(name="nivel-lista", description="Ver todos los roles por nivel que tienes guardados")
    async def nivel_lista(self, interaction):
        n = get_niveles(); roles = n.get("level_roles", {})
        if not roles:
            await interaction.response.send_message("Aún no hay roles por nivel. Usa /nivel-agregar", ephemeral=True); return
        txt = "\n".join([f"⭐ Nivel {k} -> {v}" for k,v in sorted(roles.items(), key=lambda x: int(x[0]))])
        await interaction.response.send_message(embed=discord.Embed(title="⭐ Roles por nivel", description=txt, color=0xFEE75C), ephemeral=True)

    @app_commands.command(name="config-tickets", description="Elige como sale el panel de tickets: botones o menu")
    @app_commands.describe(tipo="Botones como en tu foto, o menu desplegable")
    @app_commands.choices(tipo=[app_commands.Choice(name="Botones", value="botones"), app_commands.Choice(name="Menu desplegable", value="menu")])
    async def config_tickets(self, interaction, tipo: app_commands.Choice[str]):
        if not solo_admin(interaction):
            await interaction.response.send_message("❌ Solo admins.", ephemeral=True); return
        c = get_config(); t = c.get("tickets") or {}; t["mode"] = tipo.value; c["tickets"] = t; save_config(c)
        await interaction.response.send_message(f"✅ Tickets guardados en modo: {tipo.name}. Ahora usa /ticket-panel en el canal donde lo quieras.", ephemeral=True)

    @app_commands.command(name="config-ver", description="Ver toda tu configuracion actual")
    async def config_ver(self, interaction):
        if not solo_admin(interaction):
            await interaction.response.send_message("❌ Solo admins.", ephemeral=True); return
        c = get_config(); n = get_niveles()
        e = discord.Embed(title="⚙️ Configuración JESVEX", color=0x5865F2)
        e.add_field(name="AutoRol", value=c.get("autorol_role","⛏️ JUGADOR"), inline=False)
        e.add_field(name="Logs", value=f"<#{c.get('logs_channel_id')}>" if c.get("logs_channel_id") else "No puesto", inline=False)
        e.add_field(name="Canal niveles", value=f"<#{c.get('levels_channel_id')}>" if c.get("levels_channel_id") else "No puesto", inline=False)
        e.add_field(name="Tickets", value=(c.get("tickets") or {}).get("mode","botones"), inline=False)
        e.add_field(name="Roles por nivel", value=str(n.get("level_roles",{})) or "Ninguno", inline=False)
        await interaction.response.send_message(embed=e, ephemeral=True)

async def setup(bot): await bot.add_cog(Config(bot))

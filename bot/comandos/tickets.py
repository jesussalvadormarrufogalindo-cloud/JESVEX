import discord
from discord.ext import commands
from discord import app_commands
import json, os

# lee lo que guardaste en el panel
def cargar_config(gid):
    try:
        ruta = os.path.join(os.path.dirname(__file__), "..", "..", "dashboard", "config.json")
        if os.path.exists(ruta):
            with open(ruta, encoding="utf-8") as f:
                datos = json.load(f)
                return datos.get(str(gid), {})
    except:
        pass
    return {}

class tickets(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # esto es lo que faltaba: escuchar el menu del panel
    @commands.Cog.listener()
    async def on_interaction(self, interaction: discord.Interaction):
        try:
            data = interaction.data or {}
            custom = data.get("custom_id", "")
            # el panel manda este id
            if custom != "jesvex_ticket_select":
                return
            # responder rapido para que no salga "no ha respondido a tiempo"
            await interaction.response.defer(ephemeral=True)

            guild = interaction.guild
            usuario = interaction.user
            valores = data.get("values", [])
            elegido = valores[0] if valores else "opcion_1"

            # buscar el nombre bonito de la opcion en el panel
            cfg = cargar_config(guild.id)
            mapa = {
                "opcion_1": cfg.get("tickets_opcion1", "Soporte general") or "Soporte general",
                "opcion_2": cfg.get("tickets_opcion2", "Reportar usuario") or "Reportar usuario",
                "opcion_3": cfg.get("tickets_opcion3", "Apelar sancion") or "Apelar sancion",
            }
            nombre_opcion = mapa.get(elegido, "Soporte general")

            # no crear 2 tickets del mismo usuario
            for ch in guild.text_channels:
                if ch.name == f"ticket-{usuario.name.lower()}":
                    await interaction.followup.send(f"ya tienes un ticket abierto: {ch.mention}", ephemeral=True)
                    return

            # categoria que elegiste en el panel
            categoria = None
            cat_id = cfg.get("tickets_categoria", "")
            if cat_id:
                categoria = discord.utils.get(guild.categories, id=int(cat_id))

            # permisos: solo tu y soporte ven el canal
            overwrites = {
                guild.default_role: discord.PermissionOverwrite(view_channel=False),
                usuario: discord.PermissionOverwrite(view_channel=True, send_messages=True, read_message_history=True),
                guild.me: discord.PermissionOverwrite(view_channel=True, send_messages=True, manage_channels=True),
            }
            rol_soporte = cfg.get("tickets_rol_soporte", "")
            if rol_soporte:
                rol = guild.get_role(int(rol_soporte))
                if rol:
                    overwrites[rol] = discord.PermissionOverwrite(view_channel=True, send_messages=True, read_message_history=True)

            canal = await guild.create_text_channel(
                name=f"ticket-{usuario.name.lower()}",
                category=categoria,
                overwrites=overwrites,
                reason=f"Ticket de {usuario} - {nombre_opcion}"
            )

            embed = discord.Embed(title=f"Ticket - {nombre_opcion}", description=f"hola {usuario.mention}\ncuéntanos tu problema, el equipo te atiende pronto.\n\n**categoría:** {nombre_opcion}\n\npara cerrar escribe `/cerrar`", color=0x5865f2)
            await canal.send(embed=embed)
            await interaction.followup.send(f"tu ticket se creó aquí: {canal.mention}", ephemeral=True)
        except Exception as e:
            try:
                await interaction.followup.send(f"no pude crear el ticket: {e}", ephemeral=True)
            except:
                pass

    @app_commands.command(name="ticket", description="Crea un ticket")
    async def ticket(self, interaction: discord.Interaction):
        await interaction.response.send_message("usa el menú del panel de tickets para crear tu ticket.", ephemeral=True)

    @app_commands.command(name="cerrar", description="Cierra este ticket")
    async def cerrar(self, interaction: discord.Interaction):
        if interaction.channel.name.startswith("ticket-"):
            await interaction.response.send_message("cerrando ticket en 3 segundos...")
            import asyncio
            await asyncio.sleep(3)
            await interaction.channel.delete(reason="Ticket cerrado")
        else:
            await interaction.response.send_message("esto no es un canal de ticket.", ephemeral=True)

async def setup(bot):
    await bot.add_cog(tickets(bot))


import discord, traceback
from discord.ext import commands
class Errores(commands.Cog):
    def __init__(self, bot): self.bot = bot
    @commands.Cog.listener()
    async def on_app_command_error(self, interaction, error):
        # que ningun comando se quede en "la interaccion fallo" sin decir por que
        try:
            msg = str(error)
            if "Missing Permissions" in msg or "403" in msg:
                txt = "❌ A JESVEX le falta permiso en Discord. Revisa que el rol JESVEX esté arriba y tenga los permisos de ese comando."
            elif "Unknown Member" in msg or "10007" in msg:
                txt = "❌ Esa persona ya no está en el servidor."
            elif "timeout" in msg.lower():
                txt = "❌ Tardé mucho, inténtalo otra vez."
            else:
                txt = f"❌ Algo falló: {msg[:400]}"
            if interaction.response.is_done():
                await interaction.followup.send(txt, ephemeral=True)
            else:
                await interaction.response.send_message(txt, ephemeral=True)
        except: pass
        print("ERROR COMANDO:", traceback.format_exc())
async def setup(bot): await bot.add_cog(Errores(bot))

import discord
from discord import app_commands
from discord.ext import commands
class Reaccion(commands.Cog):
    def __init__(self, bot): self.bot = bot
    @app_commands.command(name="reaccion", description="Crea mensaje de reaction roles")
    @app_commands.default_permissions(manage_roles=True)
    async def reaccion(self, interaction: discord.Interaction, rol: discord.Role, emoji: str):
        embed = discord.Embed(title="Elige tu rol", description=f"Reacciona con {emoji} para obtener el rol {rol.mention}", color=discord.Color.teal())
        await interaction.response.send_message(embed=embed)
        msg = await interaction.original_response(); await msg.add_reaction(emoji)
        self.bot.add_listener(self.on_reaction_add)
    async def on_reaction_add(self, reaction, user):
        if user.bot: return
        if reaction.message.embeds and "Elige tu rol" in reaction.message.embeds[0].title:
            nombre = reaction.message.embeds[0].description.split("rol ")[-1]
            rol = discord.utils.get(reaction.message.guild.roles, name=nombre.replace("@","").strip()) if False else None
            # Simplificado: busca rol por mencion en el embed
            import re
            m = re.search(r"<@&(\d+)>", reaction.message.embeds[0].description)
            if m:
                rol = reaction.message.guild.get_role(int(m.group(1)))
                if rol:
                    try: await user.add_roles(rol)
                    except Exception: pass
async def setup(bot): await bot.add_cog(Reaccion(bot))

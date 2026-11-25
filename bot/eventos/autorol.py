import discord
from discord.ext import commands

class AutoRol(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        rol = discord.utils.get(member.guild.roles, name="Miembro")
        if rol is None:
            try:
                rol = await member.guild.create_role(name="Miembro", colour=discord.Colour.blue(), reason="AutoRol JESVEX")
            except Exception:
                return
        try:
            await member.add_roles(rol, reason="AutoRol JESVEX")
            print(f"AutoRol: {member} recibio el rol Miembro en {member.guild.name}")
        except Exception:
            print(f"No pude dar rol a {member}")

async def setup(bot):
    await bot.add_cog(AutoRol(bot))

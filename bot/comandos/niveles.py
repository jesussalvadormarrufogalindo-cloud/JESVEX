import discord, sqlite3, os
from discord import app_commands
from discord.ext import commands
DB = "database/jesvex.db"
def db():
    os.makedirs("database", exist_ok=True)
    c = sqlite3.connect(DB); c.execute("CREATE TABLE IF NOT EXISTS xp (guild_id TEXT, user_id TEXT, xp INTEGER, nivel INTEGER, PRIMARY KEY (guild_id, user_id))"); c.commit(); return c
class Niveles(commands.Cog):
    def __init__(self, bot): self.bot = bot
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot or message.guild is None: return
        if message.content.startswith("/"): return
        con = db(); cur = con.cursor()
        cur.execute("SELECT xp, nivel FROM xp WHERE guild_id=? AND user_id=?", (str(message.guild.id), str(message.author.id)))
        r = cur.fetchone()
        if r is None: xp, nivel = 10, 1; cur.execute("INSERT INTO xp VALUES (?,?,?,?)", (str(message.guild.id), str(message.author.id), xp, nivel))
        else:
            xp, nivel = r[0]+10, r[1]
            if xp >= nivel*100:
                nivel += 1; xp = 0
                try: await message.channel.send(f"Felicidades {message.author.mention} subiste a nivel {nivel}!")
                except Exception: pass
            cur.execute("UPDATE xp SET xp=?, nivel=? WHERE guild_id=? AND user_id=?", (xp, nivel, str(message.guild.id), str(message.author.id)))
        con.commit(); con.close()
    @app_commands.command(name="nivel", description="Ver tu nivel")
    async def nivel(self, interaction: discord.Interaction):
        con = db(); cur = con.cursor(); cur.execute("SELECT xp, nivel FROM xp WHERE guild_id=? AND user_id=?", (str(interaction.guild.id), str(interaction.user.id))); r = cur.fetchone(); con.close()
        if r is None: await interaction.response.send_message("Aun no tienes XP. Habla un poco."); return
        await interaction.response.send_message(f"{interaction.user.mention} eres nivel {r[1]} con {r[0]} XP.")
    @app_commands.command(name="clasificacion", description="Top 10 de niveles")
    async def clasificacion(self, interaction: discord.Interaction):
        con = db(); cur = con.cursor(); cur.execute("SELECT user_id, nivel, xp FROM xp WHERE guild_id=? ORDER BY nivel DESC, xp DESC LIMIT 10", (str(interaction.guild.id),)); rows = cur.fetchall(); con.close()
        txt = "\n".join([f"{i+1}. <@{uid}> - Nivel {niv} ({xp} XP)" for i,(uid,niv,xp) in enumerate(rows)]) or "Nadie tiene XP aun."
        await interaction.response.send_message(f"**Top Niveles**\n{txt}")
    @app_commands.command(name="perfil", description="Ver perfil de un usuario")
    async def perfil(self, interaction: discord.Interaction, usuario: discord.Member = None):
        u = usuario or interaction.user
        con = db(); cur = con.cursor(); cur.execute("SELECT xp, nivel FROM xp WHERE guild_id=? AND user_id=?", (str(interaction.guild.id), str(u.id))); r = cur.fetchone(); con.close()
        xp, niv = r if r else (0,1)
        embed = discord.Embed(title=f"Perfil de {u.display_name}", color=discord.Color.blue()); embed.set_thumbnail(url=u.display_avatar.url); embed.add_field(name="Nivel", value=str(niv)); embed.add_field(name="XP", value=str(xp)); embed.add_field(name="Se unio", value=u.joined_at.strftime("%d/%m/%Y") if u.joined_at else "N/A")
        await interaction.response.send_message(embed=embed)
async def setup(bot): await bot.add_cog(Niveles(bot))

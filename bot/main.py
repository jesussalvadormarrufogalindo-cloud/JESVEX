import discord
from discord.ext import commands
import os
import asyncio
from dotenv import load_dotenv
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)
@bot.event
async def on_ready():
    print(f"JESVEX conectado como {bot.user}")
    try:
        for guild in bot.guilds:
            await bot.tree.sync(guild=guild)
            print(f"Comandos sincronizados en: {guild.name}")
        synced = await bot.tree.sync()
        print(f"{len(synced)} comandos slash sincronizados")
    except Exception as e:
        print(f"Error al sincronizar: {e}")
@bot.tree.command(name="ayuda", description="Muestra toda la ayuda de JESVEX")
async def ayuda(interaction: discord.Interaction):
    embed = discord.Embed(title="JESVEX - Ayuda Completa", description="Todos los comandos de JESVEX", color=discord.Color.blue())
    embed.add_field(name="Moderacion", value="/expulsar /banear /desbanear /limpiar /silenciar /desilenciar /advertir", inline=False)
    embed.add_field(name="Otros", value="/encuesta /anuncio /reaccion", inline=False)
    await interaction.response.send_message(embed=embed)
@bot.tree.command(name="ping", description="Revisa si JESVEX esta activo")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message("Pong! Estoy activo")
async def main():
    async with bot:
     extensiones = ["eventos.logs", "eventos.automod", "comandos.moderacion", "comandos.encuestas", "comandos.anuncios", "comandos.reaccion"]
     for ext in extensiones:
            try:
                await bot.load_extension(ext)
                print(f"{ext} cargado")
            except Exception as e:
                print(f"No se pudo cargar {ext}: {e}")
        await bot.start(TOKEN)
if __name__ == "__main__":
    asyncio.run(main())

import discord
import os
from discord import app_commands
from discord.ext import commands

class InfoCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="ping", description="Muestra la latencia del bot")
    async def ping(self, interaction: discord.Interaction):
        latency = round(self.bot.latency * 1000)
        await interaction.response.send_message(f"Pong! Latencia: {latency} ms")

async def setup(bot: commands.Bot):
    await bot.add_cog(InfoCommands(bot))
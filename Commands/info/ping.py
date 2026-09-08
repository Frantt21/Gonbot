import discord
import os
from discord import app_commands
from discord.ext import commands

class PingCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # registra el comando para ambas interacciones
    @commands.hybrid_command(name="ping", description="Muestra la latencia del bot")

    async def ping(self, ctx: commands.Context):
        latency = round(self.bot.latency * 1000)
        await ctx.send(f"Pong! :b\nLatencia: `{latency}ms`")

async def setup(bot: commands.Bot):
    await bot.add_cog(PingCommands(bot))
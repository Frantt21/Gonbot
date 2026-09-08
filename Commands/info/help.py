import discord
import os
from discord import app_commands
from discord.ext import commands

class HelpCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # registra el comando para ambas interacciones
    @commands.hybrid_command(name="help", description="Muestra la ayuda del bot")

    async def help(self, ctx: commands.Context):
        embed = discord.Embed(
            title="Gonbot - Comandos",
            description="Prefix: `-`\nLista de comandos disponibles:",
            color=discord.Color.from_rgb(255, 0, 0)
        )
        embed.add_field(name="/ping", value="Muestra la latencia del bot", inline=False)
        embed.add_field(name="/help", value="Muestra la ayuda del bot", inline=False)
        embed.set_footer(text="Gonbot - Desarrollado por Fran")
        await ctx.send(embed=embed)

async def setup(bot: commands.Bot):
    await bot.add_cog(HelpCommands(bot)) 
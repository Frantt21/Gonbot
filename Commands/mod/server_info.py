import discord
import os
from discord import app_commands
from discord.ext import commands

class ServerInfoCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # registra el comando para ambas interacciones
    @commands.hybrid_command(name="server", description="Muestra información del servidor")

    async def server_info(self, ctx: commands.Context):
        guild = ctx.guild
        if guild is None:
            await ctx.send("Este comando solo puede ser usado en un servidor.")
            return

        embed = discord.Embed(
            title=f"Información del Servidor: {guild.name}",
            color=discord.Color.from_rgb(255, 0, 0)
        )
        embed.set_thumbnail(url=guild.icon.url if guild.icon else discord.Embed.Empty)
        embed.add_field(name="Nombre del Servidor", value=guild.name, inline=False)
        embed.add_field(name="ID del Servidor", value=guild.id, inline=False)
        embed.add_field(name="Miembros", value=guild.member_count, inline=False)
        embed.set_footer(text="Gonbot - Desarrollado por Fran")
        await ctx.send(embed=embed)

async def setup(bot: commands.Bot):
    await bot.add_cog(ServerInfoCommands(bot))

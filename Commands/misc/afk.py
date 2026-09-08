import discord
import os
from discord.ext import commands
from discord import app_commands

class AFKCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.afk_users = {}  # Diccionario para almacenar los usuarios AFK y sus razones

    @commands.hybrid_command(name="afk", description="Establece tu estado como AFK con una razón opcional")
    async def afk(self, ctx: commands.Context, *, reason: str = "No especificada"):
        """Establece el estado del usuario como AFK con una razón opcional."""
        self.afk_users[ctx.author.id] = reason
        await ctx.send(f"{ctx.author.mention} ahora estás AFK: {reason}")

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return  # Ignorar mensajes de bots

        # Verificar si el autor del mensaje está en la lista de AFK
        if message.author.id in self.afk_users:
            del self.afk_users[message.author.id]
            await message.channel.send(f"Bienvenido de nuevo {message.author.mention}, ya no estás AFK.")

        # Verificar si alguien menciona a un usuario que está AFK
        for user_id in self.afk_users:
            if user_id in [user.id for user in message.mentions]:
                reason = self.afk_users[user_id]
                mentioned_user = self.bot.get_user(user_id)
                await message.channel.send(f"{mentioned_user.mention} está actualmente AFK: {reason}")

async def setup(bot: commands.Bot):
    await bot.add_cog(AFKCommands(bot))
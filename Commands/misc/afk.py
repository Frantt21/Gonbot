import sqlite3
import time
import discord
import os
from discord.ext import commands
from discord import app_commands

class AFKCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db_path = "afk.db"
        self._init_db()

    def _init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS afk_users (
                    user_id INTEGER PRIMARY KEY,
                    reason TEXT,
                    timestamp REAL
                )
            """)
            conn.commit()

    def _format_duration(self, seconds: float) -> str:
        hrs, remainder = divmod(int(seconds), 3600)
        mins, secs = divmod(remainder, 60)
        return f"{hrs}h {mins}m {secs}s" if hrs else f"{mins}m {secs}s" if mins else f"{secs}s"

    @commands.hybrid_command(name="afk", description="Establece tu estado como AFK con una razón opcional")

    async def afk(self, ctx: commands.Context, *, reason: str = "No especificada"):
        current_time = time.time()

        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT OR REPLACE INTO afk_users (user_id, reason, timestamp) VALUES (?, ?, ?)", (ctx.author.id, reason, current_time))
            conn.commit()

        embed = discord.Embed(
            title="Estado AFK Activado",
            description=f"{ctx.author.mention} ahora está AFK.\nRazón: {reason}",
            color=discord.Color.from_rgb(255, 0, 0)
        )

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot or not message.guild:
            return  # Ignorar mensajes de bots

        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT timestamp FROM afk_users WHERE user_id = ?",
                           (message.author.id,)
            )
            afk_data = cursor.fetchone()

            if afk_data:
                start_time = afk_data[0]
                elapsed_seconds = time.time() - start_time
                duration_str = self._format_duration(elapsed_seconds)
                cursor.execute("DELETE FROM afk_users WHERE user_id = ?", (message.author.id,))
                conn.commit()

            embed = discord.Embed(
                title="Estado AFK Desactivado",
                color=discord.Color.from_rgb(255, 0, 0)
            )
            embed.add_field(name="Tiempo AFK", value={duration_str})
            await message.channel.send(embed=embed)

async def setup(bot: commands.Bot):
    await bot.add_cog(AFKCommands(bot))
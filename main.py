import discord
import os
from discord import app_commands
from dotenv import load_dotenv
from discord.ext import commands
import asyncio

load_dotenv()
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')

# configuración de intents para recibir eventos de mensajes
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

tree = app_commands.CommandTree(client)

if not DISCORD_TOKEN:
    raise RuntimeError('DISCORD_TOKEN no está definido en el entorno ni en el archivo .env')

# clase principal
class GonbotClient(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="!", intents=intents)

    async def setup_hook(self):
        for root, dirs, file in os.walk("./Commands"):
            for file in file:
                if file.endswith(".py") and file != "__init__.py":
                    relative_path = os.path.relpath(os.path.join(root, file))
                    if relative_path.endswith(".py"):
                        relative_path = relative_path[:-3]

                    extension_name = relative_path.replace(os.path.sep, ".")
                    try:
                        await self.load_extension(extension_name)
                        print(f"Loaded extension: {extension_name}")
                    except Exception as e:
                        print(f"Failed to load extension {extension_name}: {e}")
                        
    # ciclo de vida del bot
    async def on_ready(self):

        await self.change_presence(activity=discord.Game(name="foranly.space"), status=discord.Status.idle)

        print(f'Logged in as {self.user} (ID: {self.user.id})')
        print('------')

        # sincronizar los comandos del bot con Discord
        try:
            synced = await self.tree.sync()
            print(f'Synced {len(synced)} command(s)')
        except Exception as e:
            print(f'Error syncing commands: {e}')

# token de discord
client = GonbotClient()
client.run(DISCORD_TOKEN)